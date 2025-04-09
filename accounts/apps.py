from django.apps import AppConfig

from django.contrib.auth import get_user_model


from django.db.models.signals import post_migrate

def create_admin_user(sender, **kwargs):
    Account = get_user_model()

    if not Account.objects.filter(email="admin@mail.com").exists():
        Account.objects.create_superuser(
            username="admin",
            email="admin",
            password="admin"
        )


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"


    def ready(self):
        post_migrate.connect(create_admin_user, sender=self)
