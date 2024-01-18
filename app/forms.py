from django import forms
from ckeditor.fields import CKEditorWidget

from .models import Recipe, Ingredient


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["name", "preview_image", "time_minutes", "category", "ingredients", "description"]

        widgets = {
            "description": CKEditorWidget()
        }


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name", 'calorie', "description"]
        widgets = {
            "description": CKEditorWidget()
        }

    def clean_name(self):
        # по сути из-за поля unique в модели Ingredient проверка на уникальность будет автоматом проходить
        name = self.cleaned_data['name']
        if Ingredient.objects.filter(name=name).exists():
            raise forms.ValidationError(f'Ингредиент {name} уже существует')
        return name
