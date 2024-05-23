#!/usr/bin/env python
import logging
from pathlib import Path

from dateutil.relativedelta import relativedelta
from edc_test_utils import func_main
from edc_utils import get_utcnow

app_name = "intecomm_form_validators"
base_dir = Path(__file__).resolve().parent.parent

project_settings = dict(  # nosec B106
    BASE_DIR=Path(__file__).resolve().parent.parent,
    SECRET_KEY="django-insecure",  # nosec B106
    DEBUG=True,
    SITE_ID=101,
    EDC_PROTOCOL_NUMBER="101",
    SUBJECT_CONSENT_MODEL=None,
    SUBJECT_SCREENING_MODEL=None,
    EDC_PROTOCOL_STUDY_OPEN_DATETIME=get_utcnow() - relativedelta(years=1),
    EDC_PROTOCOL_STUDY_CLOSE_DATETIME=get_utcnow() + relativedelta(years=1),
    EDC_DX_LABELS=dict(hiv="HIV", dm="Diabetes", htn="Hypertension"),
    ALLOWED_HOSTS=[],
    INSTALLED_APPS=[
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.sites",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "intecomm_form_validators.apps.AppConfig",
    ],
    MIDDLEWARE=[
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "edc_dashboard.middleware.DashboardMiddleware",
    ],
    ROOT_URLCONF="intecomm_form_validators.urls",
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
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
    ],
    WSGI_APPLICATION="intecomm_form_validators.wsgi.application",
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str(base_dir / "db.sqlite3"),
        }
    },
    AUTH_PASSWORD_VALIDATORS=[
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
    ],
    LANGUAGE_CODE="en-us",
    TIME_ZONE="UTC",
    USE_I18N=True,
    USE_L10N=True,
    USE_TZ=True,
    STATIC_URL="/static/",
    DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
    INTECOMM_MAX_MONTHS_TO_NEXT_APPT=7,
)


def main():
    func_main(project_settings, f"{app_name}.tests")


if __name__ == "__main__":
    logging.basicConfig()
    main()
