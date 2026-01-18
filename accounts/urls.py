# accounts/urls.py

from django.urls import path
from . import views
from . import admin_participants as admin_part

urlpatterns = [
    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/',    views.login_view,    name='login'),
    path('logout/',   views.logout_view,   name='logout'),

    # Draws (public / user)
    path('draws/', views.all_draws, name='all_draws'),
    path('draws/<int:pk>/', views.draw_detail, name='draw_detail'),
    path('draws/<int:draw_id>/join/', views.join_draw, name='join_draw'),

    # Admin participant management (staff-only views provided by admin_participants.py)
    path('draws/<int:draw_id>/participants/', admin_part.draw_participants, name='draw_participants'),
    path('draws/<int:draw_id>/participants/export/', admin_part.export_participants_csv, name='export_participants_csv'),
    path('entries/<int:entry_id>/toggle_active/', admin_part.toggle_entry_active, name='toggle_entry_active'),
    path('entries/<int:entry_id>/verify/', admin_part.verify_entry, name='verify_entry'),

    # Profile
    path('profile/',  views.profile_view,  name='profile'),

    # Dashboards
# urls.py (cleaned)
path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
path('dashboard/user/',  views.user_dashboard,  name='user_dashboard'),

# participants
path('draws/<int:draw_id>/participants/', views.draw_participants, name='draw_participants'),

  path('draws/<int:draw_id>/winner-selection/', views.winner_selection_page, name='winner_selection_page'),
    path('select-winners/<int:draw_id>/', views.select_winners, name='select_winners'),
    path('winner-selection-dashboard/', views.winner_selection_dashboard, name='winner_selection_dashboard'),

]
