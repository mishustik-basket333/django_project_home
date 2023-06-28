from django import forms

from catalog.models import Product, Version
from catalog.data_file import bad_words


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'  # Использование всех полей модели
        # fields = ('first_name', ) # Использование только перечисленных полей
        # exclude = ('last_name', ) # Использование всех полей, кроме перечисленных
        # # Описан может быть только один из вариантов

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name')
        for word in bad_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError('Ошибка, использовано нежелательное имя')
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data.get('description')
        for word in bad_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError('Ошибка, использовано нежелательное слово в описании')
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control-10'


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'  # Использование всех полей модели

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control-10'
