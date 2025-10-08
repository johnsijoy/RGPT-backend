# inventory/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Unit, Project, Block

@receiver(post_save, sender=Unit)
def unit_post_save(sender, instance, created, **kwargs):
    if created:
        Project.objects.filter(id=instance.project_id).update(
            total_units=models.F('total_units') + 1
        )

@receiver(post_delete, sender=Unit)
def unit_post_delete(sender, instance, **kwargs):
    Project.objects.filter(id=instance.project_id).update(
        total_units=models.F('total_units') - 1
    )
