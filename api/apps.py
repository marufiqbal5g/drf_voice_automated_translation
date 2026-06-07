from django.apps import AppConfig


class ApiConfig(AppConfig):

    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):

        try:
            from .services.warmup import warmup_models
            warmup_models()

        except Exception as e:
            print("Warmup failed:", e)