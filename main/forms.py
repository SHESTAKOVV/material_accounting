from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.utils import timezone
from main.models import (
    Material, Direction, Location, Supplier, MaterialIncome, IncomeItem,
    MaterialTransfer, TransferItem, MaterialWriteOff, WriteOffItem, Stock
)


class CustomLoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ["name", "article", "unit"]


class DirectionForm(forms.ModelForm):
    class Meta:
        model = Direction
        fields = ["name"]


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ["name", "address", "type", "is_active"]


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            "name", "phone", "email",
            "contact_last_name", "contact_first_name", "contact_middle_name",
            "inn", "kpp"
        ]

    def clean_inn(self):
        inn = self.cleaned_data.get("inn")
        if inn and (len(inn) not in [10, 12]):
            raise ValidationError("ИНН должен содержать 10 или 12 цифр.")
        return inn

    def clean_kpp(self):
        kpp = self.cleaned_data.get("kpp")
        if kpp and len(kpp) != 9:
            raise ValidationError("КПП должен содержать 9 цифр.")
        return kpp


class MaterialIncomeForm(forms.ModelForm):
    class Meta:
        model = MaterialIncome
        fields = ["date", "supplier", "document_number"]

    def clean_date(self):
        date = self.cleaned_data.get("date")
        if date and date > timezone.now().date():
            raise ValidationError("Дата не может быть в будущем.")
        return date


class IncomeItemForm(forms.ModelForm):
    class Meta:
        model = IncomeItem
        fields = ["material", "quantity", "direction", "location"]

    def clean_quantity(self):
        qty = self.cleaned_data.get("quantity")
        if qty is not None and qty <= 0:
            raise ValidationError("Количество должно быть больше нуля.")
        return qty


IncomeItemFormSet = inlineformset_factory(
    MaterialIncome,
    IncomeItem,
    form=IncomeItemForm,
    fields=["material", "quantity", "direction", "location"],
    extra=1,
    can_delete=True
)


class MaterialTransferForm(forms.ModelForm):
    class Meta:
        model = MaterialTransfer
        fields = ["date"]

    def clean_date(self):
        date = self.cleaned_data.get("date")
        if date and date > timezone.now().date():
            raise ValidationError("Дата не может быть в будущем.")
        return date


class TransferItemForm(forms.ModelForm):
    class Meta:
        model = TransferItem
        fields = ["material", "quantity", "from_direction", "from_location", "to_direction", "to_location"]

    def clean(self):
        cleaned_data = super().clean()
        from_location = cleaned_data.get("from_location")
        to_location = cleaned_data.get("to_location")

        if from_location and to_location and from_location == to_location:
            raise ValidationError("Место отправки и получения не должны совпадать.")


TransferItemFormSet = inlineformset_factory(
    MaterialTransfer,
    TransferItem,
    form=TransferItemForm,
    extra=1,
    can_delete=True
)


class MaterialWriteOffForm(forms.ModelForm):
    class Meta:
        model = MaterialWriteOff
        fields = ["date", "reason"]

    def clean_date(self):
        date = self.cleaned_data.get("date")
        if date and date > timezone.now().date():
            raise ValidationError("Дата не может быть в будущем.")
        return date


class WriteOffItemForm(forms.ModelForm):
    class Meta:
        model = WriteOffItem
        fields = ["material", "quantity", "direction", "location"]

    def clean(self):
        cleaned_data = super().clean()
        material = cleaned_data.get("material")
        direction = cleaned_data.get("direction")
        location = cleaned_data.get("location")
        quantity = cleaned_data.get("quantity")

        if material and direction and location and quantity:
            stock = Stock.objects.filter(
                material=material, direction=direction, location=location
            ).first()

            available = stock.quantity if stock else 0
            if quantity > available:
                raise ValidationError(
                    f"Недостаточно остатков: доступно {available}, вы пытаетесь списать {quantity}"
                )


WriteOffItemFormSet = inlineformset_factory(
    MaterialWriteOff,
    WriteOffItem,
    form=WriteOffItemForm,
    extra=1,
    can_delete=True
)