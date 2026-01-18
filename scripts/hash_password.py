import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lucky_draw.settings')
import django
from django.contrib.auth.hashers import make_password

django.setup()
print(make_password('11111111'))
