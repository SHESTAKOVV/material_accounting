from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import IncomeItem, TransferItem, WriteOffItem, Stock

# ====== ПОСТУПЛЕНИЕ ======
@receiver(post_save, sender=IncomeItem)
def update_stock_on_income(sender, instance, created, **kwargs):
    if created:
        _update_stock(instance.material, instance.direction, instance.location, instance.quantity)


@receiver(post_delete, sender=IncomeItem)
def rollback_stock_on_income_delete(sender, instance, **kwargs):
    _update_stock(instance.material, instance.direction, instance.location, -instance.quantity)

# ====== СПИСАНИЕ ======
@receiver(post_save, sender=WriteOffItem)
def update_stock_on_writeoff(sender, instance, created, **kwargs):
    if created:
        _update_stock(instance.material, instance.direction, instance.location, -instance.quantity)


@receiver(post_delete, sender=WriteOffItem)
def rollback_stock_on_writeoff_delete(sender, instance, **kwargs):
    _update_stock(instance.material, instance.direction, instance.location, instance.quantity)

# ====== ПЕРЕМЕЩЕНИЕ ======
@receiver(post_save, sender=TransferItem)
def update_stock_on_transfer(sender, instance, created, **kwargs):
    if created:
        _update_stock(instance.material, instance.from_direction, instance.from_location, -instance.quantity)
        _update_stock(instance.material, instance.to_direction, instance.to_location, instance.quantity)

@receiver(post_delete, sender=TransferItem)
def rollback_stock_on_transfer_delete(sender, instance, **kwargs):
    _update_stock(instance.material, instance.from_direction, instance.from_location, instance.quantity)
    _update_stock(instance.material, instance.to_direction, instance.to_location, -instance.quantity)


# ====== Универсальная функция обновления ======
def _update_stock(material, direction, location, delta_qty):
    stock, created = Stock.objects.get_or_create(
        material=material,
        direction=direction,
        location=location,
        defaults={"quantity": 0}
    )
    stock.quantity += delta_qty
    stock.save()