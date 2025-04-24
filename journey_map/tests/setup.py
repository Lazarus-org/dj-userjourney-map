import django
from django.conf import settings
from django.core.management.utils import get_random_secret_key


def configure_django_settings() -> None:
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            SECRET_KEY=get_random_secret_key(),  # Add a secret key for testing
            DATABASES={
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": ":memory:",
                }
            },
            INSTALLED_APPS=[
                "django.contrib.admin",
                "django.contrib.auth",
                "django.contrib.contenttypes",
                "django.contrib.sessions",
                "django.contrib.messages",
                "django.contrib.staticfiles",
                "rest_framework",
                "django_filters",
                "journey_map",
                "persona_manager",
            ],
            MIDDLEWARE=[
                "django.middleware.security.SecurityMiddleware",
                "django.contrib.sessions.middleware.SessionMiddleware",
                "django.middleware.common.CommonMiddleware",
                "django.middleware.csrf.CsrfViewMiddleware",
                "django.contrib.auth.middleware.AuthenticationMiddleware",
                "django.contrib.messages.middleware.MessageMiddleware",
                "django.middleware.clickjacking.XFrameOptionsMiddleware",
            ],
            TEMPLATES=[
                {
                    'BACKEND': 'django.template.backends.django.DjangoTemplates',
                    'DIRS': [],
                    'APP_DIRS': True,
                    'OPTIONS': {
                        'context_processors': [
                            'django.template.context_processors.request',
                            'django.contrib.auth.context_processors.auth',
                            'django.contrib.messages.context_processors.messages',
                        ],
                    },
                },
            ],
            JOURNEY_MAP_API_USER_JOURNEY_FILTERSET_CLASS="journey_map.api.filters.UserJourneyFilter",
            ROOT_URLCONF="journey_map.tests.urls",
            LANGUAGE_CODE="en-us",
            TIME_ZONE="UTC",
            USE_I18N=True,
            USE_TZ=True,
        )
        django.setup()


configure_django_settings()
