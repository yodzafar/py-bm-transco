import sys

from django.apps import AppConfig
from django.db.models.signals import post_migrate


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"

    def ready(self):
        post_migrate.connect(self.create_admin_user, sender=self)

    def create_admin_user(self, sender, **kwargs):
        if sender.name != self.name:
            return

        print(f"📢 post_migrate signal received from: {sender.name}")

        if not any(
            cmd in sys.argv for cmd in ["runserver", "runserver_plus", "migrate"]
        ):
            print(f"⏭️  Skipping - command not in allowed list")
            return

        try:
            from django.contrib.auth import get_user_model
            from django.contrib.auth.models import Group, Permission
            from django.db import connection

            User = get_user_model()

            # Table mavjudligini tekshirish
            table_name = User._meta.db_table
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables
                        WHERE table_schema = 'public'
                        AND table_name = %s
                    );
                    """,
                    [table_name],
                )
                result = cursor.fetchone()
                table_exists = result[0] if result else False

            if not table_exists:
                print(f"⚠️ Table '{table_name}' does not exist yet")
                return

            admin_exists = User.objects.filter(is_superuser=True).exists()
            print(f"🔍 Checking for existing admin: {admin_exists}")

            if admin_exists:
                print("ℹ️ Admin user already exists, skipping creation")
                return

            print("🔄 Seeding admin user...")

            user = User.objects.create_superuser(
                username="admin", password="eswun3ua", email="admin@example.com"
            )

            admin_group, created = Group.objects.get_or_create(name="admin")

            user.groups.add(admin_group)

            perms = Permission.objects.all()
            admin_group.permissions.set(perms)

            print("✅ Admin user created successfully!")

        except Exception as e:
            print(f"⚠️ Error creating admin user: {e}")
            import traceback

            traceback.print_exc()
