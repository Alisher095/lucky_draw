import os
import sys
from pathlib import Path
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

USERS = [
    {
        "email": "user3@gmail.com",
        "username": "user3",
        "first_name": "user",
        "last_name": "3",
        "password": "11111111",
        "role": "user",
    },
    {
        "email": "admin3@gmail.com",
        "username": "admin3",
        "first_name": "admin",
        "last_name": "3",
        "password": "11111111",
        "role": "admin",
    },
    {
        "email": "admin4@gmail.com",
        "username": "admin4",
        "first_name": "admin",
        "last_name": "4",
        "password": "11111111",
        "role": "admin",
    },
]

User = get_user_model()
for candidate in USERS:
    user, created = User.objects.get_or_create(
        email=candidate["email"],
        defaults={
            "username": candidate["username"],
            "first_name": candidate["first_name"],
            "last_name": candidate["last_name"],
        },
    )
    if created:
        user.set_password(candidate["password"])
        user.save()
        Profile.objects.create(user=user, role=candidate["role"])
    print(f"{candidate['email']} created={created}")
