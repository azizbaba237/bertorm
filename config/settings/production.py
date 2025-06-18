from .base import *

DEBUG = False
ALLOWED_HOSTS = ['Azizbaba237.pythonanywhere.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Fichiers statiques pour production
STATIC_URL = '/static/'
STATIC_ROOT = '/home/votrenom/monprojet/static'  # Chemin absolu sur PA

# Fichiers média pour production
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/votrenom/monprojet/media'

# Paramètres de sécurité
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Configuration de Tailwind en production
TAILWIND_DEV_MODE = False