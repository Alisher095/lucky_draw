# accounts/admin_participants.py
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.template import Template, Context
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.utils import timezone
import csv

# import core models
from .models import Draw, Entry

# EntryAdminAction is optional; import if present
try:
    from .models import EntryAdminAction
except Exception:
    EntryAdminAction = None

# ---------------------------
# small helpers / staff check
# ---------------------------
def staff_check(user):
    return user.is_active and user.is_staff

def staff_required(view_func):
    return login_required(user_passes_test(staff_check)(view_func))

# ---------------------------
# Embedded template (HTML)
# ---------------------------
TEMPLATE_STR = """
{% load static %}
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Participants — {{ draw.title }}</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body { background: #f8f9fa; }
    .card-top { box-shadow: 0 2px 6px rgba(0,0,0,0.04); }
    .small-muted { font-size: .85rem; color: #6c757d; }
    .action-form { display:inline-block; margin-left:6px; }
  </style>
</head>
<body>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container">
      <a class="navbar-brand" href="#">{{ site_name }}</a>
      <div class="collapse navbar-collapse">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item"><a class="nav-link" href="{{ dashboard_url }}">Dashboard</a></li>
        </ul>
      </div>
    </div>
  </nav>

  <main class="container my-4">
    <div class="card card-top">
      <div class="card-body d-flex justify-content-between align-items-start">
        <div>
          <h4 class="mb-1">Participants for: {{ draw.title|escape }}</h4>
          <p class="small-muted mb-0">Draw ID: {{ draw.id }} • Ends: {{ draw.end_date }}</p>
        </div>
        <div class="text-end">
          <a href="{{ export_url }}" class="btn btn-outline-secondary btn-sm">Export CSV</a>
          <a href="{{ all_draws_url }}" class="btn btn-outline-primary btn-sm ms-2">All Draws</a>
        </div>
      </div>
    </div>

    <div class="card mt-3">
      <div class="card-body">
        <form class="row g-2 mb-3" method="get" action="">
          <div class="col-auto">
            <input type="text" name="q" class="form-control" placeholder="Search username or email" value="{{ q|default:'' }}">
          </div>
          <div class="col-auto">
            <button class="btn btn-primary">Search</button>
          </div>
        </form>

        <div class="table-responsive">
          <table class="table table-hover align-middle">
            <thead class="table-light">
              <tr>
                <th>#</th>
                <th>User</th>
                <th>Email</th>
                <th>Time</th>
                <th>Verified</th>
                <th>Active</th>
                <th>Note</th>
                <th class="text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              {% for e in entries %}
              <tr>
                <td>{{ e.id }}</td>
                <td>
                  <div class="fw-semibold">{{ e.user.get_full_name|default:e.user.username }}</div>
                  <div class="small-muted">{{ e.user.username }}</div>
                </td>
                <td>{{ e.user.email|default:"—" }}</td>
                <td>{{ e.entry_time }}</td>
                <td>
                  {% if e.is_verified %}<span class="badge bg-success">Yes</span>{% else %}<span class="badge bg-secondary">No</span>{% endif %}
                </td>
                <td>
                  {% if e.is_active %}<span class="badge bg-success">Active</span>{% else %}<span class="badge bg-secondary">Disabled</span>{% endif %}
                </td>
                <td>{{ e.note|default:"" }}</td>
                <td class="text-end">
                  <form method="post" action="{{ toggle_url_base }}{{ e.id }}/" class="action-form">
                    <input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}">
                    <button class="btn btn-sm btn-outline-danger" type="submit">{% if e.is_active %}Deactivate{% else %}Reactivate{% endif %}</button>
                  </form>

                  {% if not e.is_verified %}
                  <form method="post" action="{{ verify_url_base }}{{ e.id }}/" class="action-form">
                    <input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}">
                    <button class="btn btn-sm btn-outline-success" type="submit">Verify</button>
                  </form>
                  {% endif %}
                </td>
              </tr>
              {% empty %}
              <tr><td colspan="8" class="text-center small-muted">No participants found.</td></tr>
              {% endfor %}
            </tbody>
          </table>
        </div>

        {% if has_more %}
          <div class="text-center mt-3">
            <a href="?q={{ q|urlencode }}&page={{ next_page }}" class="btn btn-outline-primary btn-sm">Load more</a>
          </div>
        {% endif %}
      </div>
    </div>

  </main>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# ---------------------------
# Views
# ---------------------------

@staff_required
def draw_participants(request, draw_id):
    """
    List participants for a draw (staff only). Embeds template string so no file required.
    GET params:
      - q: search username or email (simple contains)
      - page: optional pagination (simple slicing)
    """
    draw = get_object_or_404(Draw, id=draw_id)
    qs = draw.entries.select_related('user').order_by('-entry_time')

    # simple search using Q for correctness
    q = request.GET.get('q', '').strip()
    if q:
        from django.db.models import Q
        qs = qs.filter(Q(user__username__icontains=q) | Q(user__email__icontains=q))

    # simple pagination (optional)
    page = int(request.GET.get('page', '1') or 1)
    per_page = 100
    start = (page - 1) * per_page
    end = start + per_page
    entries_page = list(qs[start:end])
    has_more = qs.count() > end

    # csrf token for forms rendered manually
    from django.middleware.csrf import get_token
    csrf_token = get_token(request)

    # Build context
    ctx = {
        'site_name': 'LuckyDraw Admin',
        'draw': draw,
        'entries': entries_page,
        'q': q,
        'csrf_token': csrf_token,
        'export_url': reverse('export_participants_csv', args=[draw.id]),
        'all_draws_url': reverse('all_draws') if 'all_draws' in [u.name for u in request.resolver_match.app_names] else reverse('user_dashboard'),
        'dashboard_url': reverse('user_dashboard'),
        'toggle_url_base': reverse('toggle_entry_active', args=[0]).rsplit('0', 1)[0],  # base to append id
        'verify_url_base': reverse('verify_entry', args=[0]).rsplit('0', 1)[0],
        'has_more': has_more,
        'next_page': page + 1,
    }

    t = Template(TEMPLATE_STR)
    html = t.render(Context(ctx))
    return HttpResponse(html)


@staff_required
@csrf_protect
def toggle_entry_active(request, entry_id):
    """Toggle entry.is_active and optionally log admin action"""
    if request.method != 'POST':
        return HttpResponseForbidden("Invalid method")

    entry = get_object_or_404(Entry, id=entry_id)
    entry.is_active = not entry.is_active
    entry.save()

    if EntryAdminAction is not None:
        try:
            EntryAdminAction.objects.create(admin=request.user, entry=entry, action=('reactivated' if entry.is_active else 'deactivated'))
        except Exception:
            pass

    return redirect('draw_participants', draw_id=entry.draw.id)


@staff_required
@csrf_protect
def verify_entry(request, entry_id):
    """Mark entry as verified and optionally log"""
    if request.method != 'POST':
        return HttpResponseForbidden("Invalid method")

    entry = get_object_or_404(Entry, id=entry_id)
    entry.is_verified = True
    entry.save()

    if EntryAdminAction is not None:
        try:
            EntryAdminAction.objects.create(admin=request.user, entry=entry, action='verified')
        except Exception:
            pass

    return redirect('draw_participants', draw_id=entry.draw.id)


@staff_required
def export_participants_csv(request, draw_id):
    draw = get_object_or_404(Draw, id=draw_id)
    qs = draw.entries.select_related('user').order_by('-entry_time')

    # CSV response
    response = HttpResponse(content_type='text/csv')
    filename = f"draw_{draw.id}_participants_{timezone.now().date()}.csv"
    response['Content-Disposition'] = f'attachment; filename=\"{filename}\"'

    writer = csv.writer(response)
    writer.writerow(['entry_id', 'user_id', 'username', 'email', 'entry_time', 'is_active', 'is_verified', 'note'])
    for e in qs:
        writer.writerow([
            e.id,
            e.user.id,
            e.user.username,
            getattr(e.user, 'email', ''),
            e.entry_time,
            getattr(e, 'is_active', ''),
            getattr(e, 'is_verified', ''),
            getattr(e, 'note', '')
        ])

    return response
