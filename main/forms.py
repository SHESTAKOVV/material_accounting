from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from main.models import Material, Direction, Location, Supplier, MaterialIncome, IncomeItem, MaterialTransfer, \
    TransferItem, MaterialWriteOff, WriteOffItem, Stock


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
        fields = ["name"]

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["name"]

class MaterialIncomeForm(forms.ModelForm):
    class Meta:
        model = MaterialIncome
        fields = ["date", "supplier"]

class IncomeItemForm(forms.ModelForm):
    class Meta:
        model = IncomeItem
        fields = ["material", "quantity", "direction", "location"]


IncomeItemFormSet = inlineformset_factory(
    MaterialIncome,
    IncomeItem,
    fields=["material", "quantity", "direction", "location"],
    extra=1,
    can_delete=True
)


class MaterialTransferForm(forms.ModelForm):
    class Meta:
        model = MaterialTransfer
        fields = ["date"]

TransferItemFormSet = inlineformset_factory(
    MaterialTransfer,
    TransferItem,
    fields=["material", "quantity", "from_direction", "from_location", "to_direction", "to_location"],
    extra=1,
    can_delete=True
)


class MaterialWriteOffForm(forms.ModelForm):
    class Meta:
        model = MaterialWriteOff
        fields = ["date", "reason"]

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