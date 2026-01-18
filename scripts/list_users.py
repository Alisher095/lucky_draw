import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lucky_draw.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
from accounts.models import Profile
User = get_user_model()
for u in User.objects.all():
    profile = Profile.objects.filter(user=u).first()
    print(u.id, u.email, u.username, u.is_staff, profile.role if profile else 'no-profile')
