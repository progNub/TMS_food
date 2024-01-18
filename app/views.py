from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.postgres.aggregates import ArrayAgg

from .forms import RecipeForm, IngredientForm
from .models import Recipe, Ingredient


def home(request: WSGIRequest):
    recipes = (
        Recipe.objects.all()
        .prefetch_related("ingredients")
        .annotate(
            # Создание массива уникальных имен тегов для каждой заметки
            ingredients_list=ArrayAgg('ingredients__name', distinct=True)
        )
        .values("id", "name", "time_minutes", "preview_image", "ingredients_list", "category")
    )

    search = request.GET.get("search")
    if search:
        recipes = recipes.filter(description__search=search)

    print(recipes.query)

    return render(request, 'home.html', {"recipes": recipes})


@login_required
def create_recipe(request: WSGIRequest):
    form = RecipeForm()

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)  # Файлы находятся отдельно!
        if form.is_valid():
            recipe: Recipe = form.save(commit=False)  # Не сохранять в базу рецепт, а вернуть его объект.
            recipe.user = request.user
            recipe.save()  # Сохраняем в базу объект.
            form.save_m2m()  # Сохраняем отношения many to many для ингредиентов и рецепта.

            return HttpResponseRedirect("/")

    return render(request, 'recipe-form.html', {'form': form})


@login_required
def update_recipe(request: WSGIRequest, recipe_id: int):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe.user != request.user:
        return HttpResponseForbidden("You do not have permission to edit this recipe")

    form = RecipeForm(instance=recipe)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)  # Файлы находятся отдельно!
        if form.is_valid():
            recipe: Recipe = form.save()
            return HttpResponseRedirect(reverse("show-recipe", args=(recipe.id,)))

    return render(request, 'recipe-form.html', {'form': form})


def show_recipe(request: WSGIRequest, recipe_id: int):
    recipe: Recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, "recipe/recipe.html", {"recipe": recipe})


def show_ingredient(request: WSGIRequest, name_ingredient):
    print(name_ingredient)
    ingredient = get_object_or_404(Ingredient, name=name_ingredient)
    return render(request, "ingredient/show_ingredients.html", {"ingredient": ingredient})


@login_required
def create_ingredient(request: WSGIRequest):
    form = IngredientForm()
    if request.POST:
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(show_ingredient, form['name'].value())
        return render(request, 'ingredient/create_ingredient.html', {'form': form})

    return render(request, 'ingredient/create_ingredient.html', {'form': form})
