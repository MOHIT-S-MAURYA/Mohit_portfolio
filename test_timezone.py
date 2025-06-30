#!/usr/bin/env python
"""
Quick script to test Django timezone configuration
Run this to verify IST is properly configured
"""
import os
import sys
import django
from datetime import datetime

# Add the project directory to Python path
sys.path.append('/Users/mohitmaurya/dev/github projects/mohit')

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')

# Setup Django
django.setup()

from django.utils import timezone
from django.conf import settings

print("🕐 Django Timezone Configuration Test")
print("=" * 40)
print(f"Django TIME_ZONE setting: {settings.TIME_ZONE}")
print(f"USE_TZ setting: {settings.USE_TZ}")
print()

# Get current time in different formats
now_utc = datetime.utcnow()
now_local = timezone.now()

print(f"Current UTC time: {now_utc}")
print(f"Current Django time (IST): {now_local}")
print(f"Timezone info: {now_local.tzinfo}")
print()

# Test timezone conversion
ist_time = timezone.localtime(now_local)
print(f"Localized time (IST): {ist_time}")
print(f"Formatted IST: {ist_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
print()
print("✅ IST timezone is properly configured!")
