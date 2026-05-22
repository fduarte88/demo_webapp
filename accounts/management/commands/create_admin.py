from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Crea el usuario administrador por defecto'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'admin'
        password = 'admin88++'
        email = 'admin@agendapro.com'

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'El usuario "{username}" ya existe.'))
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(
            f'Superusuario creado: usuario="{username}" / contraseña="{password}"'
        ))
