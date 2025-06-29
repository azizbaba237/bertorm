import os
from pathlib import Path
import pymysql

# Chemin de base du projet
BASE_DIR = Path(__file__).resolve().parent

# Clé secrète (à modifier en production)
SECRET_KEY = 'votre-cle-secrete'

# Détection de l'environnement
DJANGO_ENV = os.environ.get('DJANGO_ENV', 'development')
IS_PRODUCTION = DJANGO_ENV == 'production'

# Configuration Debug et Hosts selon l'environnement
if IS_PRODUCTION:
    DEBUG = False
    ALLOWED_HOSTS = ['Azizbaba237.pythonanywhere.com']
else:
    DEBUG = True
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
    # Paramètres de développement spécifiques
    INTERNAL_IPS = ['127.0.0.1']

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

# Configuration d'authentification
LOGIN_URL = 'core:login'
LOGIN_REDIRECT_URL = 'core:accueil'
LOGOUT_REDIRECT_URL = 'core:accueil'

# App Tailwind
TAILWIND_APP_NAME = 'theme'
TAILWIND_DEV_MODE = not IS_PRODUCTION  # True en dev, False en prod

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

# IMPORTANT: Changez cette ligne pour pointer vers le nouveau urls.py
ROOT_URLCONF = 'urls'  # Au lieu de 'config.urls'

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

# IMPORTANT: Changez cette ligne pour pointer vers le nouveau wsgi.py
WSGI_APPLICATION = 'wsgi.application'  # Au lieu de 'config.wsgi.application'

# Base de données
pymysql.install_as_MySQLdb()
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bertorm_db',
        'USER': 'root',
        'PASSWORD': '',  # Par défaut, XAMPP n'a pas de mot de passe root
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

# Configuration des fichiers statiques selon l'environnement
if IS_PRODUCTION:
    # Fichiers statiques pour production
    STATIC_URL = '/static/'
    STATIC_ROOT = '/home/votrenom/monprojet/static'  # Chemin absolu sur PA
    
    # Fichiers média pour production
    MEDIA_URL = '/media/'
    MEDIA_ROOT = '/home/votrenom/monprojet/media'
    
    # Paramètres de sécurité pour production
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_PRELOAD = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
else:
    # Fichiers statiques pour développement
    STATIC_URL = 'static/'
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    
    # URLs pour les médias
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

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

# Type de champ de clé primaire par défaut
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuration NPM
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