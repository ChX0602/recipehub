from mimetypes import guess_type

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg

from foodchaser.models import *
from forms import *
from models import *
import json
import datetime

def homepage(request):
    return render(request, 'foodchaser/home.html', {})

@login_required
def userhome(request):
    
    # We should initialize the user if the user is logged in through third party.
    if (len(Profile.objects.filter(user = request.user)) == 0):
        profile = Profile(user = request.user)
        profile.save()
    if (len(Allergy.objects.filter(user = request.user)) == 0):
        allergy = Allergy(user = request.user)
        allergy.save()

    context = {}
    thisusername = request.user.username
    context['thisusername'] = thisusername
    context['autocompleteform'] = AutocompleteSearchForm()
    return render(request, 'foodchaser/recipebox.html', context)


@login_required
def change_password(request):

    if request.method == 'GET':
        return render(request, 'foodchaser/reset_password.html', {})

    errors = []

    # Creates a new item if it is present as a parameter in the request
    # This line needs to be changed later
    if not 'new_password' in request.POST or not request.POST['new_password']:
        errors.append('You must enter the new password.')
        return render(request, 'foodchaser/reset_password.html', {'errors': errors})

    if not 'new_password_confirm' in request.POST or not request.POST['new_password_confirm']:
        errors.append('You must confirm the new password.')
        return render(request, 'foodchaser/reset_password.html', {'errors': errors})


    if request.POST['new_password_confirm'] != request.POST['new_password']:
        errors.append('confirmed password does not match.')
        return render(request, 'foodchaser/reset_password.html', {'errors': errors})

    if not 'cur_password' in request.POST or not request.POST['cur_password']:
        errors.append('You must enter your current password.')
        return render(request, 'foodchaser/reset_password.html', {'errors': errors})
    # Authenticate
    user = authenticate(username=request.user.username, password=request.POST['cur_password'])
    if user is None:
        errors.append('Password is incorrect.')
        return render(request, 'foodchaser/reset_password.html', {'errors': errors})

    # Change the password
    new_password = request.POST['new_password']

    thisuser = User.objects.get(username=request.user.username)

    # Generate a one-time use token and an email message body
    token = default_token_generator.make_token(thisuser)
    email_body = """
Please click the link below to complete the reset of your password:

  http://%s%s
""" % (request.get_host(), 
       reverse('confirmpassword', args=(thisuser.username, new_password, token))) 

    send_mail(subject="Reset password",
             message=email_body,
             from_email="foodchaser@gmail.com",
             recipient_list=[thisuser.email])
    context = []
    return render(request, 'foodchaser/needs-confirmation-password.html', context)

@transaction.atomic
def confirm_resetpassword(request, username, new_password, token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    user.set_password(new_password)

    user.save()

    return render(request, 'foodchaser/confirmedpassword.html', {})


@login_required
def changemyprofile(request):

    context = {}
    # Just display the change form if this is a GET request
    if request.method == 'GET':
        return render(request, 'foodchaser/preference_settings.html', context)

    thisusername = request.user.username

    thisprofile = Profile.objects.get(user=request.user)

    if (request.method == 'POST'):
        if (request.POST['first_name']):
            thisprofile.firstname = request.POST['first_name']
            thisprofile.save()
        if (request.POST['last_name']):
            thisprofile.lastname = request.POST['last_name']
            thisprofile.save()
        if (request.POST['gender']):
            thisprofile.gender = request.POST['gender']
            thisprofile.save()
        if (request.POST['city']):
            thisprofile.location = request.POST['city']
            thisprofile.save()
        if (request.POST['description']):
            thisprofile.description = request.POST['description']
            thisprofile.save()

    return render(request, 'foodchaser/preference_settings.html', context)


def register(request):
    context = {}

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        return render(request, 'foodchaser/registerandlogin.html', context)

    errors = []
    context['errors'] = errors

    # Checks the validity of the form data
    if 'register_username' in request.POST and request.POST['register_username']:
        context['username'] = request.POST['register_username']

    if 'register_password' in request.POST and 'register_password_confirm' in request.POST \
       and request.POST['register_password'] and request.POST['register_password_confirm'] \
       and request.POST['register_password'] != request.POST['register_password_confirm']:
        errors.append('Passwords did not match.')

    if len(User.objects.filter(username = request.POST['register_username'])) > 0:
        errors.append('Username is already taken.')

    if errors:
        return render(request, 'foodchaser/registerandlogin.html', context)

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=request.POST['register_username'], \
                                        password=request.POST['register_password'])

    # The user is inactive for now before confirmation
    new_user.is_active = False
    new_user.save()
    favorite = Favorite(user = new_user)
    favorite.save()


    # Generate a one-time use token and an email message body
    token = default_token_generator.make_token(new_user)
    email_body = """
Welcome to FoodChaser.  Please click the link below to
verify your email address and complete the registration of your account:

  http://%s%s
""" % (request.get_host(), 
       reverse('confirm', args=(new_user.username, token))) 

    send_mail(subject="Verify your email address",
             message=email_body,
             from_email="foodchaser@gmail.com",
             recipient_list=[request.POST['register_email']])

    context['email'] = request.POST['register_email']

    return render(request, 'foodchaser/needs-confirmation.html', context)

@transaction.atomic
def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()

    # Create corresponding profile
    profile = Profile(user = user)
    profile.save()
    allergy = Allergy(user = user)
    allergy.save()

    planner = Planner(user = user)
    planner.save()
    return render(request, 'foodchaser/confirmed.html', {})

# this page has static content for now
@login_required
def recommendpage(request):
    logged_in = True

    current = datetime.date.today()
    # monthly ranking
    monthAgo = current - datetime.timedelta(days = 30)
    monthRates = Rate.objects.filter(time__gt = monthAgo)
    avgMRates = monthRates.values('recipe').annotate(average_rating=Avg('rate'))
    topM = avgMRates.order_by('-average_rating')[:10]
    i = 1
    for topm in topM:
        topm['recipe'] = get_object_or_404(Recipe, id=topm['recipe'])
        topm['count'] = i
        topm['average_rating'] = round(topm['average_rating'], 1)
        i += 1

    # seasonal ranking
    seasonAgo = current - datetime.timedelta(days = 90)
    seasonRates = Rate.objects.filter(time__gt = seasonAgo)
    avgSRates = seasonRates.values('recipe').annotate(average_rating=Avg('rate'))
    topS = avgSRates.order_by('-average_rating')[:10]
    i = 1
    for tops in topS:
        tops['recipe'] = get_object_or_404(Recipe, id=tops['recipe'])
        tops['count'] = i
        tops['average_rating'] = round(tops['average_rating'], 1)
        i += 1
    
    return render(request, 'foodchaser/recommend.html', {'user':request.user, \
                                                         'logged_in' : logged_in, \
                                                         'searchform' : SearchForm(), \
                                                         'monthly' : topM, \
                                                         'seasonal' : topS, \
                                                         'autocompleteform' : AutocompleteSearchForm()})

def trial(request):
    logged_in = False
    return render(request, 'foodchaser/recommend.html', {'logged_in': logged_in})

def menuplanner(request):
    context = {}
    context['autocompleteform'] = AutocompleteSearchForm()
    return render(request, 'foodchaser/menu_planner.html', context)

def get_recipe_picture(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if not recipe.picture:
        raise Http404
    content_type = guess_type(recipe.picture.name)
    return HttpResponse(recipe.picture, content_type=content_type)

def get_step_picture(request, id):
    step = get_object_or_404(Step, id=id)
    if not step.picture:
        raise Http404
    content_type = guess_type(step.picture.name)
    return HttpResponse(step.picture, content_type=content_type)

def settings(request, allergyForm):
    context = {}
    profile = get_object_or_404(Profile, user=request.user)
    context['dislikes'] = profile.preference.all()
    context['allergyForm'] = allergyForm
    context['autocompleteform'] = AutocompleteSearchForm()
    return render(request, 'foodchaser/preference_settings.html', context)

def settings_page(request):
    allergy = get_object_or_404(Allergy, user=request.user)
    preferenceForm = PreferenceForm(instance=allergy)
    return settings(request, preferenceForm)

def virtual_restaurant(request):
    return render(request, 'foodchaser/virtual_restaurant.html')

def virtual_restaurant_menu(request):
    return render(request, 'foodchaser/virtual_restaurant_menu.html')

def get_favorites(request):
    favorite = get_object_or_404(Favorite, user=request.user)
    favorite_recipes = favorite.favorites.all()
    context = {'favorites': favorite_recipes}
    return render(request, 'foodchaser/favorites.html', context)

def add_favorite(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    favorite = get_object_or_404(Favorite, user=request.user)
    favorite.favorites.add(recipe)
    return render(request, 'foodchaser/favorites.html')

def preference(request):
    allergy = get_object_or_404(Allergy, user=request.user)

    # A form for editing if this is a GET request
    if request.method == 'GET':
        preferenceForm = PreferenceForm(instance=allergy)
        return settings(request, preferenceForm)

    preferenceForm = PreferenceForm(request.POST, instance=allergy)
    
    if preferenceForm.is_valid():
        print(preferenceForm.cleaned_data['vegetarian'])
        preferenceForm.save()
        
    return settings(request, preferenceForm)

def add_dislike(request):
    dislikeForm = DislikeIngredientForm(request.POST)
    
    if dislikeForm.is_valid():
        profile = get_object_or_404(Profile, user=request.user)
        ingredient = Ingredient(name = dislikeForm.cleaned_data['ingredient'])
        ingredient.save()
        profile.preference.add(ingredient)
        profile.save()

    allergy = get_object_or_404(Allergy, user=request.user)
    preferenceForm = PreferenceForm(instance=allergy)
    
    return settings(request, preferenceForm)
    
def save_planner(request):
    old_planner = get_object_or_404(Planner, user = request.user)
    try:
        new_planner = Planner(user = request.user)
        new_planner.save()
        data = request.POST
        for item in data:
            info = json.loads(item)
            for dish in info:
                date =  dish['key']
                print date
                recipe_id = dish['value']
                print recipe_id
                recipe = get_object_or_404(Recipe, id=recipe_id)
                print "i reached here after get recipe"
                field = getattr(new_planner, date)
                print "i reached here after finding field"
                field.add(recipe)
                print "i added recipe to field"
        old_planner.delete()
        new_planner.save()
        
    except:
        print 'nope'
    return HttpResponse('')

def get_planner(request):
    
    # We should initialize the user if the user is logged in through third party.
    if (len(Planner.objects.filter(user = request.user)) == 0):
        planner = Planner(user = request.user)
        planner.save()
    
    planner = get_object_or_404(Planner, user = request.user)
    favorite = get_object_or_404(Favorite, user=request.user)
    favorite_recipes = favorite.favorites.all()
    recipes = ((Recipe.objects.filter(owner = request.user)) | favorite_recipes)
    context = {}
    context['recipes'] = recipes
    context['autocompleteform'] = AutocompleteSearchForm()
    
    context['sunday_breakfast'] = planner.sunday_breakfast.all()
    context['sunday_lunch'] = planner.sunday_lunch.all()
    context['sunday_dinner'] = planner.sunday_dinner.all()
    
    context['monday_breakfast'] = planner.monday_breakfast.all()
    context['monday_lunch'] = planner.monday_lunch.all()
    context['monday_dinner'] = planner.monday_dinner.all()

    context['tuesday_breakfast'] = planner.tuesday_breakfast.all()
    context['tuesday_lunch'] = planner.tuesday_lunch.all()
    context['tuesday_dinner'] = planner.tuesday_dinner.all()

    context['wednesday_breakfast'] = planner.wednesday_breakfast.all()
    context['wednesday_lunch'] = planner.wednesday_lunch.all()
    context['wednesday_dinner'] = planner.wednesday_dinner.all()

    context['thursday_breakfast'] = planner.thursday_breakfast.all()
    context['thursday_lunch'] = planner.thursday_lunch.all()
    context['thursday_dinner'] = planner.thursday_dinner.all()

    context['friday_breakfast'] = planner.friday_breakfast.all()
    context['friday_lunch'] = planner.friday_lunch.all()
    context['friday_dinner'] = planner.friday_dinner.all()

    context['saturday_breakfast'] = planner.saturday_breakfast.all()
    context['saturday_lunch'] = planner.saturday_lunch.all()
    context['saturday_dinner'] = planner.saturday_dinner.all()

    return render(request, 'foodchaser/menu_planner.html', context)

def use_leftover(request):
    context = {}
    return render(request, 'foodchaser/leftover.html', context)

def suggest_leftover(request):
    context = {}
    
    if request.method == 'GET':
        return render(request, 'foodchaser/leftover.html', context)
    
    form = LeftOverForm(request.POST)
    if (form.is_valid()):
        ingre1 = form.cleaned_data['ingredient1']
        recipes = Recipe.objects.filter(ingredients__ingredient__name = ingre1)
        if ('ingredient2' in form.cleaned_data):
            ingre2 = form.cleaned_data['ingredient2']
            if (ingre2 != ''):
                recipes = Recipe.objects.filter(ingredients__ingredient__name = ingre2)
        if ('ingredient3' in form.cleaned_data):
            ingre3 = form.cleaned_data['ingredient3']
            if (ingre3 != ''):
                recipes = Recipe.objects.filter(ingredients__ingredient__name = ingre3)
    
        context['results'] = recipes
    return render(request, 'foodchaser/leftover.html', context)

    
