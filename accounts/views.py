from datetime import date
import random
import secrets
import csv

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db import models, OperationalError, transaction
from django.db.models import Exists, OuterRef
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import UserProfileForm, DrawForm
from .models import Profile, Draw, Entry, Winner
from .admin_participants import draw_participants, export_participants_csv, toggle_entry_active, verify_entry

def _get_eligible_entries(draw):
    """Fetch entries that can participate in the selection process."""
    verified_qs = Entry.objects.filter(draw_id=draw.id, is_active=True, is_verified=True).select_related('user')
    verified_entries = list(verified_qs)
    if verified_entries:
        return verified_entries, True

    fallback_qs = Entry.objects.filter(draw_id=draw.id, is_active=True).select_related('user')
    fallback_entries = list(fallback_qs)
    return fallback_entries, False


def _run_selection_algorithm(eligible_entries, winners_needed, seed=None, allow_multiple_wins=False):
    """Run the selection algorithm to pick winners from filtered entries."""
    if not eligible_entries:
        return []

    try:
        rng = random.Random(seed) if seed else secrets.SystemRandom()
        user_map = {}
        for e in eligible_entries:
            user_map.setdefault(e.user_id, []).append(e)
        distinct_user_ids = list(user_map.keys())

        selected = []
        if len(distinct_user_ids) >= winners_needed:
            chosen_user_ids = rng.sample(distinct_user_ids, winners_needed)
            for pos, uid in enumerate(chosen_user_ids, start=1):
                entry = rng.choice(user_map[uid])
                selected.append((pos, entry))
        else:
            if allow_multiple_wins:
                for pos in range(1, winners_needed + 1):
                    entry = rng.choice(eligible_entries)
                    selected.append((pos, entry))
            else:
                for pos, uid in enumerate(distinct_user_ids, start=1):
                    entry = rng.choice(user_map[uid])
                    selected.append((pos, entry))
        return selected
    except Exception as e:
        print(f"Selection algorithm error: {e}")
        return []

@login_required
def admin_dashboard(request):
    try:
        if request.user.profile.role != 'admin':
            messages.error(request, "Access denied.")
            return redirect('user_dashboard')
    except Profile.DoesNotExist:
        messages.error(request, "Profile missing. Access denied.")
        return redirect('user_dashboard')

    if request.method == 'POST' and 'create_draw' in request.POST:
        draw_form = DrawForm(request.POST)
        if draw_form.is_valid():
            new_draw = draw_form.save(commit=False)
            new_draw.created_by = request.user
            new_draw.save()
            messages.success(request, 'New draw created successfully.')
            return redirect('admin_dashboard')
    else:
        draw_form = DrawForm()

    draws_qs = Draw.objects.all().order_by('-created_at').annotate(participant_count=models.Count('entries'))
    draw_list = list(draws_qs)
    draw_ids = [d.id for d in draw_list]

    try:
        winners_qs = Winner.objects.filter(draw_id__in=draw_ids).select_related('user').order_by('draw_id', 'position')
        winners_map = {}
        for w in winners_qs:
            winners_map.setdefault(w.draw_id, []).append(w)
    except OperationalError:
        winners_map = {}
        messages.warning(request, "Warning: Could not load winners due to database schema issue. Please run migrations.")

    for d in draw_list:
        d.draw_winners = winners_map.get(d.id, [])
        d.winners_selected = bool(d.draw_winners)
    recent_draws = draw_list[:25]

    focus_draw = recent_draws[0] if recent_draws else None

    stats = {
        'total_draws': Draw.objects.count(),
        'total_entries': Entry.objects.count(),
        'total_winners': Winner.objects.count(),
        'total_users': User.objects.count(),
        'total_admins': Profile.objects.filter(role='admin').count(),
        'total_regulars': Profile.objects.filter(role='user').count(),
    }

    open_draws = sum(1 for d in draw_list if not d.winners_selected)
    closed_draws = sum(1 for d in draw_list if d.winners_selected)
    verified_entries = Entry.objects.filter(is_verified=True).count()
    total_entries = stats['total_entries'] or 0
    total_draws = stats['total_draws'] or 0
    verification_rate = round((verified_entries / total_entries) * 100, 1) if total_entries else 0
    avg_entries_per_draw = round(total_entries / total_draws, 1) if total_draws else 0

    draws_overview = draw_list[:60]
    top_draws = sorted(draw_list, key=lambda d: getattr(d, 'participant_count', 0), reverse=True)[:5]
    recent_draws_report = draw_list[:10]

    try:
        recent_winners = Winner.objects.select_related('draw', 'user').order_by('-selected_at')[:10]
    except OperationalError:
        recent_winners = []
        messages.warning(request, "Warning: Could not load recent winners due to database schema issue.")

    context = {
        'recent_draws': recent_draws,
        'today': date.today(),
        'now': timezone.now(),
        'focus_draw': focus_draw,
        'stats': stats,
        'draw_form': draw_form,
        'recent_winners': recent_winners,
        'open_draws': open_draws,
        'closed_draws': closed_draws,
        'verification_rate': verification_rate,
        'avg_entries_per_draw': avg_entries_per_draw,
        'verified_entries': verified_entries,
        'draws_overview': draws_overview,
        'top_draws': top_draws,
        'recent_draws_report': recent_draws_report,
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
def download_draw_winners(request, draw_id):
    try:
        if request.user.profile.role != 'admin':
            messages.error(request, 'Access denied.')
            return redirect('admin_dashboard')
    except Profile.DoesNotExist:
        messages.error(request, 'Access denied.')
        return redirect('admin_dashboard')

    draw = get_object_or_404(Draw, id=draw_id)
    winners = Winner.objects.filter(draw=draw).select_related('user').order_by('position')
    if not winners:
        messages.warning(request, 'No winners found for this draw.')
        return redirect('admin_dashboard')

    response = HttpResponse(content_type='text/csv')
    filename = f"draw_{draw.id}_winners.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    writer = csv.writer(response)
    writer.writerow(['Position', 'Username', 'Email', 'Prize', 'Selected At'])

    for winner in winners:
        writer.writerow([
            winner.position,
            winner.user.username,
            winner.user.email,
            winner.draw.prize_name,
            winner.selected_at.isoformat() if winner.selected_at else ''
        ])
    return response

@login_required
def winner_selection_page(request, draw_id):
    """Main winner selection page with form handling"""
    draw = get_object_or_404(Draw, id=draw_id)
    available_draws = Draw.objects.order_by('-created_at')[:30]
    
    # Initialize variables
    ran = False
    selection_preview = []
    allow_multiple = getattr(draw, 'draw_type', '').lower() == 'multi'
    default_count = getattr(draw, 'winners_count', 1) or 1
    
    # Safe winners query
    try:
        winners = Winner.objects.filter(draw=draw).select_related('user').order_by('position')
    except OperationalError as e:
        winners = []
        messages.warning(request, "Warning: Could not load existing winners due to database schema issue.")
    
    # Safe participant count
    try:
        participant_count = Entry.objects.filter(draw=draw).count()
    except:
        participant_count = 0

    # Handle form submission
    if request.method == 'POST' or request.GET.get('run') == '1':
        try:
            if request.method == 'POST':
                winners_needed = int(request.POST.get('count', default_count))
                seed = request.POST.get('seed') or None
                force = request.POST.get('force') == '1'
            else:  # GET with run=1
                winners_needed = default_count
                seed = None
                force = False

            existing_winners = False
            try:
                existing_winners = Winner.objects.filter(draw_id=draw.id).exists()
            except OperationalError:
                pass

            if existing_winners and not force:
                messages.info(request, "Winners already exist. Use 'Force replace winners' to replace them.")
            else:
                eligible_entries, has_verified_entries = _get_eligible_entries(draw)
                if not eligible_entries:
                    messages.error(request, "No eligible participants found for this draw.")
                else:
                    selection_preview = _run_selection_algorithm(eligible_entries, winners_needed, seed, allow_multiple)
                    if not selection_preview:
                        messages.error(request, "No eligible participants found for this draw.")
                    else:
                        now = timezone.now()
                        try:
                            with transaction.atomic():
                                if force and existing_winners:
                                    Winner.objects.filter(draw_id=draw.id).delete()
                                for pos, entry in selection_preview:
                                    Winner.objects.create(
                                        position=pos,
                                        selected_at=now,
                                        draw_id=draw.id,
                                        user_id=entry.user_id
                                    )

                                draw.winners_selected = True
                                if hasattr(draw, 'result_date'):
                                    draw.result_date = now.date()
                                draw.save()

                            ran = True
                            messages.success(request, f"Successfully selected {len(selection_preview)} winner(s)!")
                            try:
                                winners = Winner.objects.filter(draw=draw).select_related('user').order_by('position')
                            except OperationalError:
                                winners = []

                            if not has_verified_entries:
                                messages.info(request, "Selection included participants that were not marked as verified.")

                        except Exception as e:
                            messages.error(request, f"Error saving winners: {str(e)}")
        except Exception as e:
            messages.error(request, f"Error during winner selection: {str(e)}")

    context = {
        'draw': draw,
        'winners': winners,
        'participant_count': participant_count,
        'default_count': default_count,
        'ran': ran,
        'selection_preview': selection_preview,
        'allow_multiple': allow_multiple,
        'today': date.today(),
        'available_draws': available_draws,
    }
    
    return render(request, 'winner_selection.html', context)

@login_required
def select_winners(request, draw_id):
    """AJAX/POST endpoint for winner selection"""
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method.")
    
    try:
        draw = get_object_or_404(Draw, id=draw_id)
    except Exception:
        return JsonResponse({'error': 'Draw not found.'}, status=404)

    try:
        winners_needed = int(request.POST.get('count') or getattr(draw, 'winners_count', 0) or 1)
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid winners count.'}, status=400)

    seed = request.POST.get('seed') or None
    force = bool(request.POST.get('force'))
    allow_multiple = (getattr(draw, 'draw_type', '').lower() == 'multi')

    eligible_entries, has_verified_entries = _get_eligible_entries(draw)
    if not eligible_entries:
        return JsonResponse({'error': 'No eligible participants.'}, status=400)

    # Run algorithm
    selected = _run_selection_algorithm(eligible_entries, winners_needed, seed, allow_multiple)

    if not selected:
        return JsonResponse({'error': 'No selection produced.'}, status=400)

    # Save to database
    now = timezone.now()
    try:
        with transaction.atomic():
            if force:
                Winner.objects.filter(draw_id=draw.id).delete()
            
            for pos, entry in selected:
                Winner.objects.create(
                    position=pos,
                    selected_at=now,
                    draw_id=draw.id,
                    user_id=entry.user_id
                )
            
            draw.winners_selected = True
            if hasattr(draw, 'result_date'):
                draw.result_date = now.date()
            draw.save()
            
    except Exception as e:
        return JsonResponse({'error': f'Error saving winners: {str(e)}'}, status=500)

    # Return winners data
    try:
        winners = Winner.objects.filter(draw_id=draw.id).select_related('user').order_by('position')
        winners_data = [
            {
                'position': w.position,
                'username': w.user.username,
                'selected_at': w.selected_at.strftime("%Y-%m-%d %H:%M:%S") if w.selected_at else ''
            } for w in winners
        ]
    except OperationalError:
        winners_data = []

    payload = {'success': True, 'winners': winners_data}
    if not has_verified_entries:
        payload['warning'] = 'Selection included participants that were not marked as verified.'

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(payload)

    if not has_verified_entries:
        messages.info(request, payload['warning'])

    messages.success(request, f"Selected {len(selected)} winner(s) successfully!")
    return redirect('winner_selection_page', draw_id=draw_id)

@login_required
def winner_selection_dashboard(request):
    """Dashboard to select which draw to run winner selection for"""
    try:
        if request.user.profile.role != 'admin':
            messages.error(request, "Access denied.")
            return redirect('user_dashboard')
    except Profile.DoesNotExist:
        messages.error(request, "Profile missing. Access denied.")
        return redirect('user_dashboard')
    
    draws = Draw.objects.all().order_by('-created_at')
    
    # Add participant counts and winner status
    for draw in draws:
        try:
            draw.participant_count = Entry.objects.filter(draw=draw).count()
            draw.has_winners = Winner.objects.filter(draw=draw).exists()
        except OperationalError:
            draw.participant_count = 0
            draw.has_winners = False
    
    context = {
        'draws': draws,
    }
    return render(request, 'winner_selection_dashboard.html', context)

def staff_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and hasattr(u, 'profile') and getattr(u.profile, 'role', '') == 'admin'
    )(view_func)


def _is_admin(user):
    try:
        return user.is_authenticated and user.profile.role == 'admin'
    except Profile.DoesNotExist:
        return False


@transaction.atomic
def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('registerEmail')
        password = request.POST.get('registerPassword')
        confirm_password = request.POST.get('confirmPassword')
        role = request.POST.get('role') or 'user'
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')
        if User.objects.filter(username=email).exists():
            messages.error(request, 'Email is already registered.')
            return render(request, 'register.html')
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        Profile.objects.create(user=user, role=role)
        messages.success(request, 'Registration successful. You can now sign in.')
        return redirect('login')
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        email_or_username = (request.POST.get('loginEmail') or '').strip()
        password = request.POST.get('loginPassword')
        role = request.POST.get('role')
        user = authenticate(request, username=email_or_username, password=password)
        if not user and email_or_username:
            try:
                matched = User.objects.get(email__iexact=email_or_username)
                user = authenticate(request, username=matched.username, password=password)
            except User.DoesNotExist:
                user = None
        if not user:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'login.html')
        try:
            if user.profile.role != role:
                messages.error(request, 'Role mismatch.')
                return render(request, 'login.html')
        except Profile.DoesNotExist:
            if role in {'admin', 'user'}:
                Profile.objects.create(user=user, role=role)
            else:
                messages.error(request, 'No role assigned.')
                return render(request, 'login.html')
        login(request, user)
        return redirect('admin_dashboard' if role == 'admin' else 'user_dashboard')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def all_draws(request):
    draws = Draw.objects.order_by('-end_date').select_related('created_by').annotate(
        participants_count=models.Count('entries'),
    )
    open_draws_count = draws.filter(winners_selected=False).count()
    recent_winners = Winner.objects.select_related('draw', 'user').order_by('-selected_at')[:5]
    return render(request, 'draw_list.html', {
        'draws': draws,
        'today': date.today(),
        'open_draws_count': open_draws_count,
        'recent_winners': recent_winners,
    })


@login_required
def profile_view(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user, role='user')
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'accounts/profile.html', {'form': form})




@staff_required
def run_select_winners(request, draw_id):
    if request.method != 'POST':
        return redirect('draw_participants', draw_id=draw_id)
    draw = get_object_or_404(Draw, id=draw_id)
    count = request.POST.get('count')
    seed = request.POST.get('seed') or None
    force = request.POST.get('force') == '1'
    try:
        winners_count = int(count) if count else int(getattr(draw, 'winners_count', 1))
        if winners_count < 1:
            messages.error(request, 'Winners count must be at least 1.')
            return redirect('draw_participants', draw_id=draw_id)
    except (TypeError, ValueError):
        winners_count = int(getattr(draw, 'winners_count', 1))
    existing = list(Winner.objects.filter(draw=draw).order_by('position'))
    if existing and not force:
        messages.warning(request, f'This draw already has {len(existing)} winner(s). Use the force option to reselect.')
        return redirect('draw_participants', draw_id=draw_id)
    qs = Entry.objects.filter(draw=draw, is_active=True).order_by('entry_time')
    if getattr(draw, 'result_date', None):
        qs = qs.filter(entry_time__lte=draw.result_date)
    entry_ids = list(qs.values_list('id', flat=True))
    if not entry_ids:
        messages.error(request, 'No eligible entries found for this draw.')
        return redirect('draw_participants', draw_id=draw_id)
    if seed is None:
        import hashlib
        base = f'draw-{draw.id}-{timezone.now().isoformat()}'
        seed = hashlib.sha256(base.encode('utf-8')).hexdigest()
    import random
    rng = random.Random(seed)
    rng.shuffle(entry_ids)
    selected_ids = entry_ids[:winners_count] if winners_count <= len(entry_ids) else entry_ids
    with transaction.atomic():
        Winner.objects.filter(draw=draw).delete()
        ts = timezone.now()
        created = []
        for pos, eid in enumerate(selected_ids, start=1):
            entry = Entry.objects.select_related('user').get(pk=eid)
            w = Winner.objects.create(
                draw=draw,
                entry=entry,
                user=entry.user,
                position=pos,
                selected_at=ts,
                method='random_seeded',
                seed=seed,
                audit_note=f'Selected via admin UI by {request.user.username} at {ts.isoformat()}'
            )
            created.append(w)
        if hasattr(draw, 'winners_selected'):
            Draw.objects.filter(id=draw.id).update(winners_selected=True)
    messages.success(request, f'Selected {len(created)} winner(s). Seed: {seed[:10]}...')
    return redirect('draw_participants', draw_id=draw_id)


@login_required
def user_dashboard(request):
    try:
        if request.user.profile.role != 'user':
            return redirect('home')
    except Profile.DoesNotExist:
        return redirect('home')
    user_entry_count = Entry.objects.filter(user=request.user).count()
    already = Entry.objects.filter(user=request.user, draw=OuterRef('pk'))
    available_draws_qs = Draw.objects.filter(winners_selected=False).annotate(already_joined=Exists(already)).order_by('-created_at')[:50]
    draw_ids = list(available_draws_qs.values_list('id', flat=True))
    counts = Entry.objects.filter(draw_id__in=draw_ids).values('draw_id').order_by().annotate(count=models.Count('id'))
    counts_map = {c['draw_id']: c['count'] for c in counts}
    user_entries = Entry.objects.filter(user=request.user, draw_id__in=draw_ids).select_related('draw')
    user_entry_map = {e.draw_id: e for e in user_entries}
    winners_qs = Winner.objects.filter(draw_id__in=draw_ids).select_related('entry', 'user').order_by('position')
    winners_map = {}
    for w in winners_qs:
        winners_map.setdefault(w.draw_id, []).append(w)
    available_draws = []
    for d in available_draws_qs:
        d.entries_count = counts_map.get(d.id, 0)
        entry = user_entry_map.get(d.id)
        d.already_joined = bool(entry)
        d.user_entry = entry
        dw = winners_map.get(d.id, [])
        d.draw_winners = dw
        uw = None
        for w in dw:
            if w.user_id == request.user.id or (w.entry and w.entry.user_id == request.user.id):
                uw = w
                break
        d.user_won = bool(uw)
        d.user_win_position = uw.position if uw else None
        available_draws.append(d)
    joined_draws_qs = Draw.objects.filter(entries__user=request.user).distinct()
    user_wins = Winner.objects.filter(user=request.user).select_related('draw').order_by('-selected_at')
    user_wins_map = {w.draw_id: w for w in user_wins}
    joined_draws = []
    for d in joined_draws_qs:
        uw = user_wins_map.get(d.id)
        d.user_won = bool(uw)
        d.user_win_position = uw.position if uw else None
        joined_draws.append(d)
    recent_entries = Entry.objects.filter(user=request.user).select_related('draw').order_by('-entry_time')[:12]
    draw_history = []
    for entry in recent_entries:
        draw = entry.draw
        win = user_wins_map.get(draw.id)
        if win:
            status = 'Winner'
            status_class = 'winner'
        elif draw.winners_selected:
            status = 'Closed'
            status_class = 'closed'
        else:
            status = 'Open'
            status_class = 'open'
        draw_history.append({
            'draw': draw,
            'entry': entry,
            'status': status,
            'status_class': status_class,
            'position': win.position if win else None,
        })

    notifications = []
    for win in user_wins[:5]:
        notifications.append({
            'title': f"You won {win.draw.title}",
            'detail': f"Position #{win.position}",
            'time': win.selected_at,
            'type': 'win',
        })
    for entry in recent_entries[:5]:
        notifications.append({
            'title': f"Joined {entry.draw.title}",
            'detail': f"Prize: {entry.draw.prize_name}",
            'time': entry.entry_time,
            'type': 'entry',
        })
    notifications = sorted(notifications, key=lambda n: n['time'], reverse=True)[:8]

    user_recent_wins = []
    for w in list(user_wins[:10]):
        user_recent_wins.append({
            'draw': w.draw,
            'position': w.position,
            'selected_at': w.selected_at,
            'claim_status': 'Awaiting claim',
        })

    recent_wins = Winner.objects.select_related('draw', 'user').order_by('-selected_at')[:20]
    return render(request, 'user_dashboard.html', {
        'available_draws': available_draws,
        'joined_draws': joined_draws,
        'recent_winners': recent_wins,
        'user_recent_wins': user_recent_wins,
        'draw_history': draw_history,
        'notifications': notifications,
        'user_entry_count': user_entry_count,
        'today': date.today(),
        'now': timezone.now(),
        'user_wins': user_wins,
    })


@login_required
def my_wins(request):
    try:
        if request.user.profile.role != 'user':
            return redirect('home')
    except Profile.DoesNotExist:
        return redirect('home')

    wins = Winner.objects.filter(user=request.user).select_related('draw').order_by('-selected_at')

    return render(request, 'my_wins.html', {
        'wins': wins,
        'today': date.today(),
        'now': timezone.now(),
    })


@login_required
def join_draw(request, draw_id):
    try:
        if request.user.profile.role != 'user':
            return redirect('home')
    except Profile.DoesNotExist:
        return redirect('home')
    if request.method != 'POST':
        return redirect('draw_detail', pk=draw_id)
    draw = get_object_or_404(Draw, id=draw_id)
    if draw.winners_selected:
        messages.error(request, 'This draw is closed and no longer accepting entries.')
        return redirect('draw_detail', pk=draw_id)
    with transaction.atomic():
        max_participants = getattr(draw, 'max_participants', None)
        if max_participants:
            current_count = Entry.objects.filter(draw=draw).count()
            if current_count >= max_participants:
                messages.error(request, 'This draw has reached the maximum number of participants.')
                return redirect('draw_detail', pk=draw_id)
        entry, created = Entry.objects.get_or_create(user=request.user, draw=draw, defaults={'is_active': True})
        if created:
            messages.success(request, 'You have successfully joined the draw.')
        else:
            messages.info(request, 'You are already participating in this draw.')
    return redirect('draw_detail', pk=draw_id)


@login_required
def draw_detail(request, pk):
    try:
        _ = request.user.profile
    except Profile.DoesNotExist:
        return redirect('home')
    draw = get_object_or_404(Draw.objects.select_related('created_by'), pk=pk)
    entries_qs = Entry.objects.filter(draw=draw).select_related('user').order_by('-entry_time')
    entries_count = entries_qs.count()
    user_joined = entries_qs.filter(user=request.user).exists()
    winners = Winner.objects.filter(draw=draw).select_related('user', 'entry').order_by('position')
    is_closed = bool(draw.winners_selected)
    is_open = not is_closed
    context = {
        'draw': draw,
        'entries': entries_qs[:100],
        'entries_count': entries_count,
        'user_joined': user_joined,
        'winners': list(winners),
        'is_closed': is_closed,
        'is_open': is_open,
        'today': date.today(),
        'now': timezone.now(),
    }
    return render(request, 'draw_detail.html', context)
