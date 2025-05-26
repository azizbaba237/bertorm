from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import EmailVerificationToken, PasswordResetToken

class Command(BaseCommand):
    help = 'Supprime les tokens de vérification et réinitialisation expirés'

    def handle(self, *args, **options):
        now = timezone.now()
        
        # Nettoyer les tokens de vérification d'email
        expired_email_tokens = EmailVerificationToken.objects.filter(expires_at__lt=now)
        count_email = expired_email_tokens.count()
        expired_email_tokens.delete()
        
        # Nettoyer les tokens de réinitialisation
        expired_password_tokens = PasswordResetToken.objects.filter(expires_at__lt=now)
        count_password = expired_password_tokens.count()
        expired_password_tokens.delete()
        
        self.stdout.write(self.style.SUCCESS(
            f'Supprimé {count_email} tokens email et {count_password} tokens password expirés.'
        ))