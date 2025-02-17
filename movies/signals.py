from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mass_mail
from django.contrib.auth.models import User
from .models import Movie

@receiver(post_save, sender=Movie)
def notify_users_new_movie(sender, instance, created, **kwargs):
    if created:
        users = User.objects.all()
        emails = [(
            'Yangi film qo\'shildi!',
            f'Yangi film: {instance.title}\n\nTavsif: {instance.description}',
            'brnasra@example.com',
            [user.email]
        ) for user in users if user.email]
        send_mass_mail(emails, fail_silently=False)