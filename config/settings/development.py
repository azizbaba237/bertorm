from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Base de données
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Fichiers statiques
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = BASE_DIR / 'staticfiles'
# URLs pour les médias
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Paramètres de développement spécifiques
INTERNAL_IPS = ['127.0.0.1']

# Configuration de Tailwind en mode développement
TAILWIND_DEV_MODE = True