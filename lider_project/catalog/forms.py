from django import forms

from catalog.models import Category


class SearchForm(forms.Form):
    search = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Поиск"}),
        required=False
    )

class CategoryFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label=" Выберите категорию "
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({
            'class': 'custom-select'
        })