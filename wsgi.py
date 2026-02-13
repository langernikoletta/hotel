"""
WSGI config for hotel project.
"""

import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application

base_dir = Path(__file__).resolve().parent
project_root = base_dir.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel.settings')

application = get_wsgi_application()
