import os
from pathlib import Path

# Chemin de base du projet
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Clé secrète (à modifier en production)
SECRET_KEY = 'votre-cle-secrete'

# Applications installées
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Applications tierces
    'tailwind',
    'django_browser_reload',
    
    # Applications locales
    'core',
    'theme',  # App Tailwind
    
    'crispy_forms',  # pour les formulaires stylisés
    'crispy_tailwind',  # pour Tailwind
]

# Ajoutez aussi ces lignes
LOGIN_URL = 'core:login'
LOGIN_REDIRECT_URL = 'core:accueil'
LOGOUT_REDIRECT_URL = 'core:accueil'


# App Tailwind
TAILWIND_APP_NAME = 'theme'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
    #'core.middleware.LoginRequiredMiddleware',  # Middleware personnalisé
    'core.middleware.UserActivityMiddleware',   # Pour suivre l'activité
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Base de données
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Validation du mot de passe
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalisation
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

# Fichiers statiques
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = BASE_DIR / 'staticfiles'
# URLs pour les médias
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Type de champ de clé primaire par défaut
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Add this to your settings.py
NPM_BIN_PATH = "C:\\Program Files\\nodejs\\npm.cmd"  # Example Windows path, adjust as needed

# Configuration Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    
]

AUTH_USER_MODEL = 'core.User' 

# Configuration de Django Debug Toolbar
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: not request.path.startswith('/__reload__/'),
}