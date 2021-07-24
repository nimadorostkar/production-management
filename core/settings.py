import os
from decouple import config
from unipath import Path
import dj_database_url



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = Path(__file__).parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_1122')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True)

# load production server from .env
ALLOWED_HOSTS = ['localhost', '127.0.0.1', config('SERVER', default='127.0.0.1')]



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'app.config.AppConfig',
    'import_export',  # https://django-import-export.readthedocs.io/en/latest/index.html
    'extra_settings', # https://github.com/fabiocaccamo/django-extra-settings
    'bootstrapform',  # https://django-bootstrap-form.readthedocs.io/en/latest/
    'jalali_date',    # https://pypi.org/project/django-jalali-date/
    'extensions',
    'mptt',
    'allauth',        # Third Party - 1) All Auth
    'allauth.account',
    'allauth.socialaccount'
]





# -------------------------- General Settings ----------------------------------



WSGI_APPLICATION = 'core.wsgi.application'



#DEFAULT_AUTO_FIELD='django.db.models.AutoField'
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'



ROOT_URLCONF = 'core.urls'
#LOGIN_REDIRECT_URL = "home"   # Route defined in app/urls.py
#LOGOUT_REDIRECT_URL = "home"  # Route defined in app/urls.py



AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]





# jalali date
JALALI_DATE_DEFAULTS = {
   'Strftime': {
        'date': '%y/%m/%d',
        'datetime': '%H:%M:%S _ %y/%m/%d',
    },
    'Static': {
        'js': [
            # loading datepicker
            'admin/js/django_jalali.min.js',
            # OR
            # 'admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.core.js',
            # 'admin/jquery.ui.datepicker.jalali/scripts/calendar.js',
            # 'admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.datepicker-cc.js',
            # 'admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.datepicker-cc-fa.js',
            # 'admin/js/main.js',
        ],
        'css': {
            'all': [
                'admin/jquery.ui.datepicker.jalali/themes/base/jquery-ui.min.css',
            ]
        }
    },
}






TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")  # ROOT dir for templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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





# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        #'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}



# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]




# Required for all-auth
SITE_ID = 1

ACCOUNT_FORMS = {
    'login': 'allauth.account.forms.LoginForm',
    'signup': 'allauth.account.forms.SignupForm',
    #'signup': 'dashboard.forms.ProfileForm',            # custom signup form -- https://github.com/pennersr/django-allauth/blob/master/allauth/templates/account/signup.html
    'add_email': 'allauth.account.forms.AddEmailForm',
    'change_password': 'allauth.account.forms.ChangePasswordForm',
    'set_password': 'allauth.account.forms.SetPasswordForm',
    'reset_password': 'allauth.account.forms.ResetPasswordForm',
    'reset_password_from_key': 'allauth.account.forms.ResetPasswordKeyForm',
    'disconnect': 'allauth.socialaccount.forms.DisconnectForm',
}

ACCOUNT_AUTHENTICATION_METHOD = ("username")
ACCOUNT_EMAIL_VERIFICATION = ("none")
#ACCOUNT_EMAIL_VERIFICATION = ('mandatory')
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION  = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
EMAIL_CONFIRMATION_SIGNUP = True
ACCOUNT_EMAIL_REQUIRED =True
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = '/'
ACCOUNT_LOGOUT_ON_GET =False
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
SOCIALACCOUNT_QUERY_EMAIL = (ACCOUNT_EMAIL_REQUIRED)
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_AVATAR_SUPPORT = ( 'avatar' in INSTALLED_APPS)
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL = SERVER_EMAIL = '--email--'
EMAIL_HOST_PASSWORD = '--pass--'
EMAIL_PORT = 587
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'





# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True




# SRC: https://devcenter.heroku.com/articles/django-assets
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'core/static'),)
MEDIA_ROOT= os.path.join(BASE_DIR, 'media')
MEDIA_URL='/media/'









# End settings
