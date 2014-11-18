from _ast import Num
from mimetypes import guess_type

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.comments.models import Comment
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404

from foodchaser.models import *
from forms import *
from models import Ingredient, IngredientUnit, Step, Recipe, Rate


def add_recipe(request):
    context = {}
    context['urlform'] = AddRecipebyURLForm()
    context['recipe'] = RecipeForm()
    context['instruction'] = AddInstructionsForm()
    context['ingredients'] = AddIngredientsForm()      
    context['autocompleteform'] = AutocompleteSearchForm()
    
    if request.method == 'GET':
        return render(request, 'foodchaser/add_recipe.html', context)

    user = request.user
    recipef = RecipeForm(request.POST, request.FILES)
    instructionf = AddInstructionsForm(request.POST, request.FILES)
    ingredientsf = AddIngredientsForm(request.POST)
    
    if not recipef.is_valid() or not instructionf.is_valid() or not \
    ingredientsf.is_valid():
        return render(request, 'foodchaser/add_recipe.html', context)
    
    # Store ingredient
    ingredient = Ingredient(name = ingredientsf.cleaned_data['item'])
    
    ingredient.save()
    
    ingredientunit = IngredientUnit(quantity =  ingredientsf.cleaned_data['quantity'], \
                            unit = ingredientsf.cleaned_data['unit'], \
                            notes = ingredientsf.cleaned_data['notes'], \
                            ingredient = ingredient)
     
    ingredientunit.save()
    
    # Store instructions
    step = Step(description = instructionf.cleaned_data['des'], \
                preptime = instructionf.cleaned_data['preptime'], \
                cooktime = instructionf.cleaned_data['cooktime'], \
                picture = instructionf.cleaned_data['stepPic'])
    
    step.save()
    
    recipe = Recipe(name = recipef.cleaned_data['name'], \
                    description = recipef.cleaned_data['description'], \
                    category1 = recipef.cleaned_data['category1'], \
                    category2 = recipef.cleaned_data['category2'], \
                    spicy = recipef.cleaned_data['spicy'], \
                    estimated_time= recipef.cleaned_data['estimated_time'],\
                    owner = user,\
                    picture = recipef.cleaned_data['picture'])

    recipe.save()
    recipe.ingredients.add(ingredientunit)
    recipe.steps.add(step)

    # Add additional ingredients and steps
    # Parse additional steps
    i = 2
    while (('des'+str(i)) in request.POST):
        request.POST['des'] = request.POST['des'+str(i)]
        request.POST['preptime'] = request.POST['preptime'+str(i)]
        request.POST['cooktime'] = request.POST['cooktime'+str(i)]
        if (('stepPic'+str(i)) in request.FILES):
            request.FILES['stepPic'] = request.FILES['stepPic'+str(i)]
        else:
            request.FILES['stepPic'] = None
            
        instructionf = AddInstructionsForm(request.POST, request.FILES)
        if not instructionf.is_valid():
            return render(request, 'foodchaser/add_recipe.html', context)

        step = Step(description = instructionf.cleaned_data['des'], \
                preptime = instructionf.cleaned_data['preptime'], \
                cooktime = instructionf.cleaned_data['cooktime'], \
                picture = instructionf.cleaned_data['stepPic'])
        step.save()
        recipe.steps.add(step)
        i += 1

    # Parse additional ingredients
    i = 2
    while (('item'+str(i)) in request.POST):
        request.POST['item'] = request.POST['item'+str(i)]
        request.POST['quantity'] = request.POST['quantity'+str(i)]
        request.POST['unit'] = request.POST['unit'+str(i)]
        request.POST['notes'] = request.POST['notes'+str(i)]
            
        ingredientsf = AddIngredientsForm(request.POST)
        if not ingredientsf.is_valid():
            return render(request, 'foodchaser/add_recipe.html', context)

        # Store ingredient
        ingredient = Ingredient(name = ingredientsf.cleaned_data['item'])
        ingredient.save()
        ingredientunit = IngredientUnit(quantity = ingredientsf.cleaned_data['quantity'], \
                            unit = ingredientsf.cleaned_data['unit'], \
                            notes = ingredientsf.cleaned_data['notes'], \
                            ingredient = ingredient)
     
        ingredientunit.save()
        recipe.ingredients.add(ingredientunit)
        i += 1
    
    recipe.save()
    recipes = Recipe.objects.all().filter(owner = request.user)
    
    context['recipes'] = recipes
    context['user'] = user
    
    return render(request, 'foodchaser/recipebox_maindish.html', context)

def search(request):
    
    context = {}
    
    result = Recipe.objects.all().filter(name__contains=request.GET['autocomplete'])
    if (request.GET['category1']):
        final_result = result.filter(category1=request.GET['category1'])
    if (request.GET['category2']):
        final_result = result.filter(category2=request.GET['category2'])
    else:
        final_result = result

    context['recipes'] = final_result
    context['user'] = request.user
    context['autocompleteform'] = AutocompleteSearchForm()
    
    return render(request, 'foodchaser/recipebox_maindish.html', context)

def recipebox_maindish(request):
    context = {}
    context['autocompleteform'] = AutocompleteSearchForm()
    recipes = Recipe.objects.all().filter(owner = request.user)
   
    context['recipes'] = recipes
   
    return render(request, 'foodchaser/recipebox_maindish.html', context)

def recipe_view(request, id):
    context = {}
    
    user = request.user
    
    recipe = Recipe.objects.get(id = id)
    
    context['recipe'] = recipe
    context['ingredients'] = recipe.ingredients.all()
    context['steps'] = recipe.steps.all()
    context['user'] = user
    context['rating'] = RatingForm()
    context['comment'] = CommentForm()
    context['comments'] = recipe.comments.all()
    context['autocompleteform'] = AutocompleteSearchForm()
    return render(request, 'foodchaser/recipe_view.html', context)

    
def comment(request):
    context = {}
    rid = request.POST['id']
    recipe = Recipe.objects.get(id = rid)
    context['recipe'] = recipe
    context['ingredients'] = recipe.ingredients.all()
    context['steps'] = recipe.steps.all()
    context['user'] = request.user
    context['rating'] = RatingForm()
    context['comment'] = CommentForm()
    context['comments'] = recipe.comments.all()
    context['autocompleteform'] = AutocompleteSearchForm()
    if request.method == 'GET':
        print 1
        return render(request, 'foodchaser/recipe_view.html', context)
    if request.method == 'POST':
        print 3 
        comment = CommentForm(request.POST)
    
    if not comment.is_valid():
        return render(request, 'foodchaser/recipe_view.html', context)
    
    text = Comment(text=comment.cleaned_data['comment'], \
                   owner=request.user)
    text.save()
    recipe.comments.add(text)
    
    context['comments'] = recipe.comments.all()
    
    return render(request, 'foodchaser/recipe_view.html', context)


def rate(request):
    context = {}
    rid = request.POST['rid']
    recipe = Recipe.objects.get(id = rid)
    context['recipe'] = recipe
    context['ingredients'] = recipe.ingredients.all()
    context['steps'] = recipe.steps.all()
    context['user'] = request.user
    context['rating'] = RatingForm()
    context['comment'] = CommentForm()
    context['comments'] = recipe.comments.all()
    context['autocompleteform'] = AutocompleteSearchForm()
    if request.method == 'GET':
        return render(request, 'foodchaser/recipe_view.html', context)
    rating = RatingForm(request.POST)
    if not rating.is_valid():
        return render(request, 'foodchaser/recipe_view.html', context)
    rate = rating.cleaned_data['rate']
    numRate = recipe.numRating
    currRate = recipe.rating
    recipe.rating = round(float(currRate*numRate + rate)/float(numRate+1),1)
    recipe.numRating += 1
    recipe.save()
    rateObj = Rate(recipe=recipe, rate=rate)
    rateObj.save()
    return render(request, 'foodchaser/recipe_view.html', context)
    
def edit(request, id):
    context = {}
    context['urlform'] = AddRecipebyURLForm()
    context['instruction'] = InstructionsForm()
    context['ingredients'] = IngredientsForm()      
    context['autocompleteform'] = AutocompleteSearchForm()
    
    recipe = Recipe.objects.get(id = id)
    context['recipe'] = recipe
    context['user'] = request.user
    ingredients = recipe.ingredients.all()
    steps = recipe.steps.all()
    
    ingredientsf = []
    stepsf = []
    
    for ingredient in ingredients:
        ingredientsf.append(IngredientsForm(instance=ingredient))
    
    for step in steps:
        stepsf.append(InstructionsForm(instance=step))
        
    context['ingredientsf'] = ingredientsf
    context['stepsf'] = stepsf

    context['ingredients'] = ingredients
    context['steps'] = steps
    context['user'] = request.user
    context['rating'] = RatingForm()
    context['comment'] = CommentForm()
    context['comments'] = recipe.comments.all()
    context['searchform'] = SearchForm()
    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        recipef = RecipeForm(instance=recipe)  # Creates form from the 
        context['recipef'] = recipef          # existing entry.
        return render(request, 'foodchaser/edit_recipe.html', context)
 
    # if method is POST, get form data to update the model
    rform = RecipeForm(request.POST, request.FILES, instance=recipe)
    sform = InstructionsForm(request.POST)
    iform = IngredientsForm(request.POST)
    if not rform.is_valid() or not sform.is_valid() or not iform.is_valid():
        context['recipef'] = RecipeForm(instance=recipe)
        return render(request, 'foodchaser/recipebox_maindish.html', context)
 
    rform.save()
    sform.save()
    iform.save()
    ingredients = recipe.ingredients.all()
    steps = recipe.steps.all()
    context['ingredients'] = ingredients
    context['steps'] = steps
    context['searchform'] = SearchForm()
    recipes = Recipe.objects.all().filter(owner = request.user)
   
    context['recipes'] = recipes
    return render(request, 'foodchaser/recipe_view.html', context)
   
def delete(request, id):
    context = {}
    context['autocompleteform'] = AutocompleteSearchForm()
    recipes = Recipe.objects.all().filter(owner = request.user)
    recipe = get_object_or_404(Recipe, id=id)
    if recipe:
        recipe.delete()
    else:
        context['recipes'] = recipes
        return render(request, 'foodchaser/recipebox_maindish.html', context)
        
    context['searchform'] = SearchForm()   
    context['recipes'] = recipes
   
    return render(request, 'foodchaser/recipebox_maindish.html', context)   

