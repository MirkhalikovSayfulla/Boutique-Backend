from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from products.models import Customer


# Create Customer Profile
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    print('Work signals.py file :)')
    if created:
        Customer.objects.create(
            user=instance,
            full_name=instance.first_name + '  ' + instance.last_name,
            email=instance.email
        )


# post_save.connect(create_customer, sender=User)


# Update Customer Profile
"""
@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
    if not created:
        instance.customer.save()
"""
