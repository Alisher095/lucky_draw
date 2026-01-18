from datetime import date
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db import models, transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from django.db.models import Exists, OuterRef
from .forms import UserProfileForm, DrawForm
from .models import Profile, Draw, Entry, Winner
from .admin_participants import draw_participants, export_participants_csv, toggle_entry_active, verify_entry
import secrets

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.db import transaction
from django.utils import timezone
from django.db import OperationalError
from datetime import date
import random
import secrets
from .models import Draw, Entry, Winner, Profile

def _run_selection_algorithm(draw, winners_needed, seed=None, allow_multiple_wins=False):
    """Run the selection algorithm to pick winners"""
    try:
        eligible_qs = Entry.objects.filter(draw_id=draw.id, is_active=1, is_verified=1).select_related('user')
        eligible = list(eligible_qs)
        if not eligible:
            return []

        rng = random.Random(seed) if seed else secrets.SystemRandom()
        # map user -> entries
        user_map = {}
        for e in eligible:
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
                    entry = rng.choice(eligible)
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
    # simple admin guard
    try:
        if request.user.profile.role != 'admin':
            messages.error(request, "Access denied.")
            return redirect('user_dashboard')
    except Profile.DoesNotExist:
        messages.error(request, "Profile missing. Access denied.")
        return redirect('user_dashboard')

    draws_qs = Draw.objects.all().order_by('-created_at')
    draw_ids = list(draws_qs.values_list('id', flat=True))
    
    # Safe winners query
    try:
        winners_qs = Winner.objects.filter(draw_id__in=draw_ids).select_related('user').order_by('draw_id', 'position')
        winners_map = {}
        for w in winners_qs:
            winners_map.setdefault(w.draw_id, []).append(w)
    except OperationalError as e:
        winners_map = {}
        messages.warning(request, "Warning: Could not load winners due to database schema issue. Please run migrations.")

    recent_draws = []
    for d in draws_qs[:25]:
        d.draw_winners = winners_map.get(d.id, [])
        d.winners_selected = bool(d.draw_winners)
        recent_draws.append(d)

    focus_draw = recent_draws[0] if recent_draws else None

    stats = {
        'total_draws': Draw.objects.count(),
        'total_entries': Entry.objects.count(),
        'total_winners': Winner.objects.count() if 'winners_qs' in locals() else 0,
    }

    context = {
        'recent_draws': recent_draws,
        'today': date.today(),
        'focus_draw': focus_draw,
        'stats': stats,
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
def winner_selection_page(request, draw_id):
    """Main winner selection page with form handling"""
    draw = get_object_or_404(Draw, id=draw_id)
    
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
            # Get parameters
            if request.method == 'POST':
                winners_needed = int(request.POST.get('count', default_count))
                seed = request.POST.get('seed') or None
                force = request.POST.get('force') == '1'
            else:  # GET with run=1
                winners_needed = default_count
                seed = None
                force = False
            
            # Check for existing winners
            existing_winners = False
            try:
                existing_winners = Winner.objects.filter(draw_id=draw.id).exists()
            except OperationalError:
                pass

            if existing_winners and not force:
                messages.info(request, "Winners already exist. Use 'Force replace winners' to replace them.")
            else:
                # Run selection algorithm
                selection_preview = _run_selection_algorithm(draw, winners_needed, seed, allow_multiple)
                if not selection_preview:
                    messages.error(request, "No eligible participants found for this draw.")
                else:
                    # Save winners to database
                    now = timezone.now()
                    try:
                        with transaction.atomic():
                            if force and existing_winners:
                                Winner.objects.filter(draw_id=draw.id).delete()
                            
                            for pos, entry in selection_preview:
                                Winner.objects.create(
                                    position=pos, 
                                    won_at=now, 
                                    draw_id=draw.id, 
                                    user_id=entry.user_id
                                )
                            
                            # Update draw status
                            draw.winners_selected = True
                            if hasattr(draw, 'result_date'):
                                draw.result_date = now.date()
                            draw.save()
                        
                        ran = True
                        messages.success(request, f"Successfully selected {len(selection_preview)} winner(s)!")
                        
                        # Refresh winners list
                        try:
                            winners = Winner.objects.filter(draw=draw).select_related('user').order_by('position')
                        except OperationalError:
                            winners = []
                            
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

    # Find eligible entries
    try:
        eligible_qs = Entry.objects.filter(draw_id=draw.id, is_active=1, is_verified=1).select_related('user')
        eligible = list(eligible_qs)
        if not eligible:
            return JsonResponse({'error': 'No eligible participants.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Error fetching participants: {str(e)}'}, status=500)

    # Run algorithm
    selected = _run_selection_algorithm(draw, winners_needed, seed, allow_multiple)

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
                    won_at=now, 
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
                'won_at': w.won_at.strftime("%Y-%m-%d %H:%M:%S")
            } for w in winners
        ]
    except OperationalError:
        winners_data = []

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'winners': winners_data})
    
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
    # map user->entries
    user_map = {}
    for e in eligible:
        user_map.setdefault(e.user_id, []).append(e)
    distinct_user_ids = list(user_map.keys())
    allow_multiple_wins = (getattr(draw, 'draw_type', '').lower() == 'multi')
    rng = secrets.SystemRandom()
    final_selected = []

    if len(distinct_user_ids) >= winners_needed:
        chosen_user_ids = rng.sample(distinct_user_ids, winners_needed)
        for pos, uid in enumerate(chosen_user_ids, start=1):
            entry = rng.choice(user_map[uid])
            final_selected.append((pos, entry))
    else:
        if allow_multiple_wins:
            for pos in range(1, winners_needed + 1):
                entry = rng.choice(eligible)
                final_selected.append((pos, entry))
        else:
            for pos, uid in enumerate(distinct_user_ids, start=1):
                entry = rng.choice(user_map[uid])
                final_selected.append((pos, entry))
            messages.warning(request, f"Only {len(final_selected)} distinct participants available; selected those.")

    now = timezone.now()
    try:
        with transaction.atomic():
            for pos, entry in final_selected:
                Winner.objects.create(
                    position=pos,
                    won_at=now,
                    draw_id=draw.id,
                    user_id=entry.user_id
                )
            if hasattr(draw, 'winners_selected'):
                draw.winners_selected = True
                if hasattr(draw, 'result_date'):
                    draw.result_date = now.date()
                draw.save()
    except Exception:
        messages.error(request, "Error saving winners; operation rolled back.")
        return redirect('admin_dashboard')

    messages.success(request, f"{len(final_selected)} winner(s) selected.")
    return redirect('admin_dashboard')

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
    draws = Draw.objects.order_by('-end_date').select_related('created_by')
    return render(request, 'draw_list.html', {'draws': draws, 'today': date.today()})


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


@login_required
def admin_dashboard(request):
    if not _is_admin(request.user):
        return redirect('home')
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
    total_users = User.objects.count()
    total_draws = Draw.objects.count()
    total_entries = Entry.objects.count()
    total_winners = Winner.objects.count()
    total_admins = Profile.objects.filter(role='admin').count()
    total_regulars = Profile.objects.filter(role='user').count()
    recent_users = User.objects.select_related('profile').order_by('-date_joined')[:5]
    recent_draws = Draw.objects.select_related('created_by').order_by('-id')[:5]
    context = {
        'draw_form': draw_form,
        'stats': {
            'total_users': total_users,
            'total_admins': total_admins,
            'total_regulars': total_regulars,
            'total_draws': total_draws,
            'total_entries': total_entries,
            'total_winners': total_winners,
        },
        'recent_users': recent_users,
        'recent_draws': recent_draws,
        'today': date.today(),
        'now': timezone.now(),
    }
    return render(request, 'admin_dashboard.html', context)


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
    already = Entry.objects.filter(user=request.user, draw=OuterRef('pk'))
    available_draws_qs = Draw.objects.filter(end_date__gte=date.today()).annotate(already_joined=Exists(already)).order_by('-start_date')[:50]
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
    joined_draws = Draw.objects.filter(entries__user=request.user).distinct()
    recent_wins = Winner.objects.select_related('draw', 'user').order_by('-selected_at')[:20]
    return render(request, 'user_dashboard.html', {
        'available_draws': available_draws,
        'joined_draws': joined_draws,
        'results': recent_wins,
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
    if draw.end_date and draw.end_date < date.today():
        messages.error(request, 'This draw is already closed.')
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
    is_closed = bool(draw.end_date and draw.end_date < date.today())
    is_open = not is_closed and (not draw.start_date or draw.start_date <= date.today())
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
