import os
from .settings import BASE_DIR

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "be_project_dev",
        "USER": "magic",
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", 5000),
    }
}