from django.conf import settings
from django.db import models
from django.utils import timezone

# ---------------- PROFILE MODEL ----------------
class Profile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# ---------------- DRAW MODEL ----------------
class Draw(models.Model):
    DRAW_TYPE_CHOICES = (
        ('single', 'Single Winner'),
        ('multi',  'Multiple Winners'),
    )

    title          = models.CharField(max_length=255, default='Untitled Draw')
    draw_type      = models.CharField(max_length=10, choices=DRAW_TYPE_CHOICES, default='single')
    description    = models.TextField(default='No description provided')
    prize_name     = models.CharField(max_length=200, default='Prize')
    prize_value    = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    winners_count  = models.PositiveIntegerField(default=1)
    start_date     = models.DateField(null=True, blank=True)
    end_date       = models.DateField(null=True, blank=True)
    result_date    = models.DateField(null=True, blank=True)
    winners_selected = models.BooleanField(default=False)

    created_by     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_draws')
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.get_draw_type_display()})"

    # helpers used in views
    def eligible_entries_qs(self):
        return Entry.objects.filter(draw_id=self.id, is_active=True, is_verified=True).select_related('user')

    def winners_exist(self):
        return Winner.objects.filter(draw_id=self.id).exists()

    def winners_count_int(self):
        return int(self.winners_count or 0)


# ---------------- ENTRY MODEL ----------------
class Entry(models.Model):
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='entries')
    draw       = models.ForeignKey(Draw, on_delete=models.CASCADE, related_name='entries')
    entry_time = models.DateTimeField(auto_now_add=True)

    # admin/management flags
    is_active   = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    note        = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'draw')
        ordering = ['-entry_time']

    def __str__(self):
        return f"{self.user.username} → {self.draw.title}"



class Winner(models.Model):
    
    draw       = models.ForeignKey('Draw', on_delete=models.CASCADE, related_name='winners')
    entry      = models.ForeignKey('Entry', on_delete=models.SET_NULL, related_name='winning_record', null=True, blank=True)
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wins')
    position   = models.PositiveSmallIntegerField(default=1)
    selected_at = models.DateTimeField(default=timezone.now)
    method     = models.CharField(max_length=100, default='random_sample')
    seed       = models.CharField(max_length=128, blank=True, null=True)
    audit_note = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('draw', 'position')
        ordering = ['draw', 'position']

    def __str__(self):
        return f"{self.user.username} won {self.draw.title} (#{self.position})"

    def __str__(self):
        return f"{self.user.username} won {self.draw.title} (#{self.position})"


# ---------------- ENTRY ADMIN ACTION / AUDIT ----------------
class EntryAdminAction(models.Model):
    admin      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='entry_admin_actions')
    entry      = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='admin_actions')
    action     = models.CharField(max_length=50)   # e.g., 'deactivated','verified','note_added','reactivated'
    reason     = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.action} by {self.admin} on entry {self.entry_id} at {self.created_at}"
