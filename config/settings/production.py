from .base import *

DEBUG = False
ALLOWED_HOSTS = ['votredomaine.com']

# Paramètres de sécurité
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_PRELOAD = True

# Configuration de Tailwind en production
TAILWIND_DEV_MODE = False