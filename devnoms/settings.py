from pathlib import Path
import os


DEBUG = True
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = "django-insecure-*$x=ow7f(%i$u-jijnq+_x)-7z&ms7!a=_khkt$18x8jq4zdrg"

# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "chat",
    "corsheaders",
    'cloudinary',
]
ASGI_APPLICATION = "devnoms.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}


MIDDLEWARE = [
     "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]






STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}



ROOT_URLCONF = "devnoms.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "devnoms.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

# TIME_ZONE = "UTC"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = "login"


STATIC_URL = "/static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATIC_ROOT=os.path.join(BASE_DIR,'staticfiles')


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }



# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'defaultdb',
#         'USER': 'avnadmin',
#         'PORT':'23763',
#         'PASSWORD': 'AVNS_ddCr3Veso9grzt2aqhd',
#         'HOST': 'pg-ac4b4510cde34abc8e805b7c7b1472b8-test1645099799-choreo-org-a.d.aivencloud.com',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'koyebdb',
        'USER': 'koyeb-adm',
        'PASSWORD': 'npg_Wl34iHrRqLYx',
        'HOST': 'ep-lucky-bird-a2j752bg.eu-central-1.pg.koyeb.app',
        'OPTIONS': {'sslmode': 'require'},
    }
}

import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
    cloud_name="dn31ev1gi",
    api_key="655723243684832",
    api_secret="MIUDoWIaICZJNdvLqI-foVrhFQQ",
)
