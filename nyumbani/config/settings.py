import decimal
import json
import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

import dj_database_url

from datetime import timedelta


def get_bool_env(env_var, default=False):
    assert default in [False, True]
    value = os.getenv(env_var)
    if value is None:
        return default
    try:
        parsed = json.loads(value.lower())
        assert parsed in [False, True]
        return parsed
    except ValueError:
        raise Exception("Invalid boolean value: {}".format(value))


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "1cihulg0o6e2d-=mcykt$f0p*5z*l)t099@!ug=qz%r(vbw6b%"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_bool_env("DEBUG")
ENVIRONMENT = os.getenv("ENVIRONMENT", "DEVELOPMENT")
allowed_hosts = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1")
ALLOWED_HOSTS = allowed_hosts.split(",")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # third party
    # 'oauth2_provider',
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    # 'django_filters',
    # 'djoser',
    # 'ckeditor',
    # local
    "common",
    "users",
    "organizations",
    "bookings",
    "restaurant",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 'oauth2_provider.middleware.OAuth2TokenMiddleware',
]

SITE_ID = 1
CORS_ORIGIN_ALLOW_ALL = True
CSRF_COOKIE_SECURE = get_bool_env("CSRF_COOKIE_SECURE", False)
SESSION_COOKIE_SECURE = get_bool_env("CSRF_COOKIE_SECURE", False)

CSRF_TRUSTED_ORIGINS = (
    "localhost:4000",
    "127.0.0.1:4000",
)

sentry_sdk.init(
    dsn=os.getenv(
        "SENTRY_DSN",
        "https://432df80113f64d0786a15b93f227e6f2@o1383561.ingest.sentry.io/6700839",
    ),
    integrations=[
        DjangoIntegration(),
    ],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)

# CORS_ALLOWED_ORIGINS = [
#     'http://hr.sasdef.go.ke',
#     'http://www.hr.sasdef.go.ke',
# ]

# auth
OAUTH2_PROVIDER = {"SCOPES": {"delivery_requests": "Access to delivery requests"}}
LOGIN_URL = "/admin/login/"
CLIENT_ID = os.getenv("CLIENT_ID", "")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
AUTH_SERVER_URL = os.getenv("AUTH_SERVER_URL", "http://localhost:4000")
AUTH_USER_MODEL = "users.User"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=int(os.getenv("ACCESS_TOKEN_LIFETIME", 1))),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=int(os.getenv("REFRESH_TOKEN_LIFETIME", 30))
    ),
    "AUTH_HEADER_TYPES": ("Bearer", "Token"),
}

DEFAULT_SENDER_EMAIL = os.getenv("DEFAULT_SENDER_EMAIL", "admin@example.com")
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = DEFAULT_SENDER_EMAIL
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')

# OAUTH2_PROVIDER_APPLICATION_MODEL = 'oauth2_provider.Application'
# EMAILS
if ENVIRONMENT == "DEVELOPMENT":
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# DEFAULT_SENDER_EMAIL = os.getenv('DEFAULT_SENDER_EMAIL', 'dev@sasdef.go.ke')

# SMS - africa's talking
AT_API_KEY = os.getenv("AT_API_KEY")
AT_USERNAME = os.getenv("AT_USERNAME")
AT_SENDER_ID = os.getenv("AT_SENDER_ID")

VARIANCE_PERCENTAGE = int(os.getenv("VARIANCE_PERCENTAGE", 10))

API_DOMAIN = os.getenv("API_DOMAIN", "http://localhost:7171")
FRONTEND_DOMAIN = os.getenv("FRONTEND_DOMAIN", "localhost:4200")
DOMAIN = FRONTEND_DOMAIN


# bolt food
bf_commission = os.getenv("DEFAULT_BOLT_FOOD_COMMISSION", "0.18")
DEFAULT_BOLT_FOOD_COMMISSION = round(decimal.Decimal(bf_commission), 2)
BOLT_FOOD_BAG_COST = os.getenv("BOLT_FOOD_BAG_COST", "3000")
DEFAULT_BOLT_FOOD_BAG_DEDUCTION = os.getenv("DEFAULT_BOLT_FOOD_BAG_DEDUCTION", "500")
no_email_bf_couriers = os.getenv("NO_EMAIL_BF_COURIERS", "182255,171110")
NO_EMAIL_BF_COURIERS = no_email_bf_couriers.split(",")

WAITING_FILE_ID = int(os.getenv("WAITING_FILE_ID", 37))
TIPS_FILE_ID = int(os.getenv("TIPS_FILE_ID", 57))
ADJUSTED_TIPS_FILE_ID = int(os.getenv("ADJUSTED_TIPS_FILE_ID", 80))
COURIER_UID_FILE_ID = int(os.getenv("COURIER_UID_FILE_ID", 92))

DJOSER = {
    "PASSWORD_RESET_CONFIRM_URL": "auth/set-password?uid={uid}&token={token}",
    "ACTIVATION_URL": "verification/?uid={uid}&token={token}",
    "SEND_ACTIVATION_EMAIL": True,
    "SERIALIZERS": {
        "user": "users.serializers.UserSerializer",
        "user_create": "users.serializers.CreateUserSerializer",
        "current_user": "users.serializers.MeUserSerializer",
    },
}

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'zoloni.oauth2.OAuth2ClientCredentialAuthentication',
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
        # "rest_framework.renderers.AdminRenderer",
        # "drf_renderer_xlsx.renderers.XLSXRenderer",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
    ],
    "PAGE_SIZE": 25,
}

AUTHENTICATION_BACKENDS = (
    # 'oauth2_provider.backends.OAuth2Backend',
    "django.contrib.auth.backends.ModelBackend",
)

WSGI_APPLICATION = "config.wsgi.application"
# ASGI_APPLICATION = 'zoloni.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [("127.0.0.1", 6379)]},
    }
}

DATABASES = {"default": dj_database_url.config()}
DATABASES["default"]["ENGINE"] = "django.db.backends.postgresql"


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Nairobi"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/


STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
DEFAULT_MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles/")
MEDIA_ROOT = os.getenv("MEDIA_ROOT", DEFAULT_MEDIA_ROOT)
MEDIA_URL = "/media/"

GDAL_LIBRARY_PATH = os.environ.get("GDAL_LIBRARY_PATH")
GEOS_LIBRARY_PATH = os.environ.get("GEOS_LIBRARY_PATH")

# SMS
BUNICOM_SMS_URL = os.getenv(
    "BUNICOM_SMS_URL", "https://portal.bunicom.com/api/services/sendsms/"
)
BUNICOM_BULK_SMS_URL = os.getenv(
    "BUNICOM_BULK_SMS_URL", "https://api.bunicom.com/sendbulksms"
)
BUNICOM_SMS_DELIVERY_REPORT_URL = os.getenv(
    "BUNICOM_SMS_DELIVERY_REPORT_URL", "https://api.bunicom.com/getdlr"
)
BUNICOM_API_KEY = os.getenv("BUNICOM_API_KEY", "KIFUNGUO")
BUNICOM_SHORTCODE = os.getenv("BUNICOM_SHORTCODE", "BuniComSMS")
BUNICOM_PARTNER_ID = os.getenv("BUNICOM_PARTNER_ID", "8678")

# partners
PARTNERS = {
    "DELVR": {
        "SCHEME": os.getenv("DELVR_SCHEME", ""),
        "HOST": os.getenv("DELVR_HOST", ""),
        "PORT": os.getenv("DELVR_PORT", "80"),
        "POST_REQUEST_URL": os.getenv("DELVR_POST_REQUEST_URL", ""),
        "TRACK_REQUEST_URL": os.getenv("DELVR_TRACK_REQUEST_URL", ""),
        "API_KEY": os.getenv("DELVR_API_KEY", ""),
        "API_SECRET": os.getenv("DELVR_API_SECRET", ""),
    },
    "GLOVO": {
        "SCHEME": os.getenv("GLOVO_SCHEME", ""),
        "HOST": os.getenv("GLOVO_HOST", ""),
        "PORT": os.getenv("DELVR_PORT", "80"),
        "API_KEY": os.getenv("GLOVO_API_KEY", ""),
        "API_SECRET": os.getenv("GLOVO_API_SECRET", ""),
    },
    "BOXLEO": {
        "SCHEME": os.getenv("BOXLEO_SCHEME", ""),
        "HOST": os.getenv("BOXLEO_HOST", ""),
        "PORT": os.getenv("BOXLEO_PORT", "80"),
        "MERCHANT_ID": os.getenv("BOXLEO_MERCHANT_ID", ""),
        "API_SECRET": os.getenv("BOXLEO_API_SECRET", ""),
    },
}

# for local 3.2 django
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

GDAL_LIBRARY_PATH = os.environ.get("GDAL_LIBRARY_PATH")
GEOS_LIBRARY_PATH = os.environ.get("GEOS_LIBRARY_PATH")

# payment alerts
PAYMENT_NOTIFICATION_EMAIL = os.getenv("PAYMENT_NOTIFICATION_EMAIL", "me@example.com")
PAYMENT_NOTIFICATION_EMAIL_PASSWORD = os.getenv(
    "PAYMENT_NOTIFICATION_EMAIL_PASSWORD", "pasuaaad"
)
PAYMENT_NOTIFICATION_EMAIL_SERVER = os.getenv(
    "PAYMENT_NOTIFICATION_EMAIL_SERVER", "some.imap.server"
)

# gmaps
GMAPS_API_KEY = os.getenv("GMAPS_API_KEY", "SumKEY")

FIRST_X_KILOMETERS = int(os.getenv("FIRST_X_KILOMETERS", 5))
FIRST_X_FEE = int(os.getenv("FIRST_X_FEE", 190))
NEXT_X_FEE = int(os.getenv("NEXT_X_FEE", 19))

CUSTOMER_CARE_PHONE_NUMBER = os.getenv("CUSTOMER_CARE_PHONE_NUMBER", "+254713942025")

# TWILIO
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "sid")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "token")
TWILIO_WHATSAPP_SENDER = os.getenv("TWILIO_WHATSAPP_SENDER", "+14155238886")

# FB whatsapp business cloud api
FB_ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN", "toKen")
FB_PHONE_NUMBER_ID = os.getenv("FB_PHONE_NUMBER_ID", "toKen")
WHATSAPP_BUSINESS_ACCOUNT_ID = os.getenv("WHATSAPP_BUSINESS_ACCOUNT_ID", "toKen")
TUMANA_SYS_USER_ACCESS_TOKEN = os.getenv("TUMANA_SYS_USER_ACCESS_TOKEN", "toKen")

FB_GRAPH_BASE_URL = os.getenv("FB_GRAPH_BASE_URL", "https://graph.facebook.com")
FB_GRAPH_VERSION = os.getenv("FB_GRAPH_VERSION", "v13.0")
FB_URL_PREFIX = f"{FB_GRAPH_BASE_URL}/{FB_GRAPH_VERSION}"

FB_WEBHOOK_VERIFY_TOKEN = os.getenv("FB_WEBHOOK_VERIFY_TOKEN", "etetey673")

# INTASEND
INTASEND_PUBLIC_KEY = os.getenv("INTASEND_PUBLIC_KEY", "-")
INTASEND_API_TOKEN = os.getenv("INTASEND_API_TOKEN", "-")
INTASEND_BASE_API_URL = os.getenv("INTASEND_BASE_API_URL", "-")
INTASEND_CHECKOUT_URL = os.getenv("INTASEND_CHECKOUT_URL", "-")
INTASEND_DEFAULT_CURRENCY = os.getenv("INTASEND_DEFAULT_CURRENCY", "KES")
INTASEND_DEFAULT_COUNTRY = os.getenv("INTASEND_DEFAULT_COUNTRY", "KE")
INTASEND_PAYMENT_STATUS_URL = os.getenv(
    "INTASEND_PAYMENT_STATUS_URL", "api/v1/payment/status/"
)
INTASEND_REDIRECT_URL = os.getenv(
    "INTASEND_REDIRECT_URL",
    "https://vertafrica.bubbleapps.io/version-test/payment-confirmation",
)

# TOOKAN
TOOKAN_V2_API_KEY = os.getenv("TOOKAN_V2_API_KEY", "key")
TOKAN_V2_BASE_URL = os.getenv("TOKAN_V2_BASE_URL", "https://api.tookanapp.com/v2")
TOOKAN_DEFAULT_TIMEZONE = os.getenv("TOOKAN_DEFAULT_TIMEZONE", "-180")
TOOKAN_PICKUP_DELTA = int(os.getenv("TOOKAN_PICKUP_DELTA", "10"))
TOOKAN_DROPOFF_DELTA = int(os.getenv("TOOKAN_DROPOFF_DELTA", "60"))

TOOKAN_CREATE_TASK_URL = os.getenv("TOOKAN_CREATE_TASK_URL", "create_task")

# admin SMS numbers
admin_nos = os.getenv("ADMIN_PHONE_NUMBERS", "254718893693")
ADMIN_PHONE_NUMBERS = admin_nos.split(",")

AWS_SERVER_PUBLIC_KEY = os.getenv("AWS_SERVER_PUBLIC_KEY", "kiii")
AWS_SERVER_SECRET_KEY = os.getenv("AWS_SERVER_SECRET_KEY", "sikret")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME", "rijon")
AWS_TEXT_ROLE_ARN = os.getenv("AWS_TEXT_ROLE_ARN", "arnadaone")
AWS_DOCSEE_BUCKET = os.getenv("AWS_DOCSEE_BUCKET", "docsee")

# firebase supabase
SUPABASE_BASE_URL = os.getenv("SUPABASE_BASE_URL", "supabase.io")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "sumsupakaey")

# slack
RESERVED_PRODUCT_SLACK_CHANNEL = os.getenv(
    "RESERVED_PRODUCT_SLACK_CHANNEL", "C053JR50GBF"
)
NEW_ORDER_SLACK_CHANNEL = os.getenv("NEW_ORDER_SLACK_CHANNEL", "C053JR50GBF")
NEW_USER_SLACK_CHANNEL = os.getenv("NEW_USER_SLACK_CHANNEL", "C053JR50GBF")
FIREBASE_ADMIN_CREDENTIAL = os.getenv("FIREBASE_ADMIN_CREDENTIAL", "key_file.json")

# firebase
FIREBASE_ACCOUNT_TYPE = os.environ.get("FIREBASE_ACCOUNT_TYPE")
FIREBASE_PROJECT_ID = os.environ.get("FIREBASE_PROJECT_ID")
FIREBASE_PRIVATE_KEY_ID = os.environ.get("FIREBASE_PRIVATE_KEY_ID")
FIREBASE_PRIVATE_KEY = os.environ.get("FIREBASE_PRIVATE_KEY")
FIREBASE_CLIENT_EMAIL = os.environ.get("FIREBASE_CLIENT_EMAIL")
FIREBASE_CLIENT_ID = os.environ.get("FIREBASE_CLIENT_ID")
FIREBASE_AUTH_URI = os.environ.get("FIREBASE_AUTH_URI")
FIREBASE_TOKEN_URI = os.environ.get("FIREBASE_TOKEN_URI")
FIREBASE_AUTH_PROVIDER_X509_CERT_URL = os.environ.get(
    "FIREBASE_AUTH_PROVIDER_X509_CERT_URL"
)
FIREBASE_CLIENT_X509_CERT_URL = os.environ.get("FIREBASE_CLIENT_X509_CERT_URL")

# forest admin
FOREST = {
    "FOREST_URL": "https://api.forestadmin.com",
    "FOREST_ENV_SECRET": "df8b28b345aefbd0805170fb231b51e90e34baba296c26ad30567ed063130513",
    "FOREST_AUTH_SECRET": "1e0f4ec9475f253c06e7a941d6fb24fa5ee505c3855989f0",
}
APPEND_SLASH = False

PLACE_HOLDER_PRODUCT_IMG_URL = os.getenv("PLACE_HOLDER_PRODUCT_IMG_URL", "url")

# ###########################################
# Nyumbani core settings
# ###########################################

NYUMBANI_CORE_URL = os.getenv("NYUMBANI_CORE_URL", "http://localhost:4000")
NYUMBANI_LOGIN_URL = f"{NYUMBANI_CORE_URL}/api/v1/login/"
NYUMBANI_PASSWORD_RESET_URL = f"{NYUMBANI_CORE_URL}/api/v1/password-reset/"
