from django.db import models
from django.contrib.auth.models import User


class Unit(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Единица измерения")

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название компании")
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True, null=True)
    email = models.EmailField(verbose_name="Email", blank=True, null=True)
    contact_last_name = models.CharField(max_length=100, verbose_name="Фамилия", blank=True)
    contact_first_name = models.CharField(max_length=100, verbose_name="Имя", blank=True)
    contact_middle_name = models.CharField(max_length=100, verbose_name="Отчество", blank=True)
    inn = models.CharField(max_length=12, verbose_name="ИНН", blank=True, null=True)
    kpp = models.CharField(max_length=9, verbose_name="КПП", blank=True, null=True)

    def get_contact_name(self):
        parts = [self.contact_last_name, self.contact_first_name, self.contact_middle_name]
        return ' '.join(filter(None, parts))

    def __str__(self):
        contact = self.get_contact_name()
        return f"{self.name} ({contact})" if contact else self.name


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
    LOCATION_TYPES = [
        ('WAREHOUSE', 'Склад'),
        ('PRODUCTION', 'Производство'),
        ('OFFICE', 'Офис'),
        ('OTHER', 'Другое'),
    ]

    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    address = models.TextField(verbose_name="Адрес", blank=True)
    type = models.CharField(max_length=20, choices=LOCATION_TYPES, default='WAREHOUSE', verbose_name="Тип")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        verbose_name = "Место хранения"
        verbose_name_plural = "Места хранения"

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"



class MaterialIncome(models.Model):
    date = models.DateField(verbose_name="Дата поступления")
    document_number = models.CharField(max_length=100, verbose_name="Номер документа", blank=True, null=True)
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



class MaterialTransfer(models.Model):
    date = models.DateField(verbose_name="Дата перемещения")
    document_number = models.CharField(max_length=100, verbose_name="Номер документа", blank=True, null=True)
    responsible = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Ответственный")
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



class MaterialWriteOff(models.Model):
    date = models.DateField(verbose_name="Дата списания")
    reason = models.CharField(max_length=255, verbose_name="Причина")
    document_number = models.CharField(max_length=100, verbose_name="Номер документа", blank=True, null=True)
    responsible = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Ответственный")
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


class Stock(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=3, default=0)

    class Meta:
        unique_together = ("material", "direction", "location")

    def __str__(self):
        return f"{self.material} — {self.quantity} в {self.location}"