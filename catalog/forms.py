from django import forms
from django.forms import ModelForm
from catalog.models import Product, Version


# class StyleForMixin:
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'form-control'



class ProductModeratorForm(ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'description', 'is_published')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('views_counter','owner', 'is_published')

    # Список запрещенных слов
    forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно',
                       'обман', 'полиция', 'радар']


    def clean_name(self):
        name = self.cleaned_data.get('product')
        if any(word in name.lower() for word in self.forbidden_words):
            raise forms.ValidationError('Название содержит запрещенные слова.')
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if any(word in description.lower() for word in self.forbidden_words):
            raise forms.ValidationError('Описание содержит запрещенные слова.')
        return description


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'
