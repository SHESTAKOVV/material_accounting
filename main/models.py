from django.db import models
from django.contrib.auth.models import User

# === Справочники ===

class Unit(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Единица измерения")

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название поставщика")

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Наименование материала")
    article = models.CharField(max_length=100, unique=True, verbose_name="Артикул")
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, verbose_name="Ед. изм.")

    def __str__(self):
        return f"{self.name} ({self.article})"


class Direction(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Направление")

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Место хранения")

    def __str__(self):
        return self.name


# === Поступление материалов ===

class MaterialIncome(models.Model):
    date = models.DateField(verbose_name="Дата поступления")
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, verbose_name="Поставщик")
    responsible = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Ответственный")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Поступление от {self.date} ({self.supplier})"


class IncomeItem(models.Model):
    income = models.ForeignKey(MaterialIncome, on_delete=models.CASCADE, related_name="items")
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    direction = models.ForeignKey(Direction, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.material} - {self.quantity} {self.material.unit}"


# === Перемещение материалов ===

class MaterialTransfer(models.Model):
    date = models.DateField()
    responsible = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Перемещение от {self.date}"


class TransferItem(models.Model):
    transfer = models.ForeignKey(MaterialTransfer, on_delete=models.CASCADE, related_name="items")
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    from_direction = models.ForeignKey(Direction, on_delete=models.PROTECT, related_name="transfer_from")
    from_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="transfer_from")
    to_direction = models.ForeignKey(Direction, on_delete=models.PROTECT, related_name="transfer_to")
    to_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="transfer_to")

    def __str__(self):
        return f"{self.material} ({self.quantity}) из {self.from_location} в {self.to_location}"


# === Списание материалов ===

class MaterialWriteOff(models.Model):
    date = models.DateField(verbose_name="Дата")
    reason = models.CharField(max_length=255, verbose_name="Причина")
    responsible = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Списание от {self.date} — {self.reason}"


class WriteOffItem(models.Model):
    writeoff = models.ForeignKey(MaterialWriteOff, on_delete=models.CASCADE, related_name="items")
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    direction = models.ForeignKey(Direction, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.material} - {self.quantity} списано"


# === Остатки на складе ===

class Stock(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=3, default=0)

    class Meta:
        unique_together = ("material", "direction", "location")

    def __str__(self):
        return f"{self.material} — {self.quantity} в {self.location}"