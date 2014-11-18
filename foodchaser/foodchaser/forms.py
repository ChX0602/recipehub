from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from models import *
from cgitb import text
from django.forms.widgets import FileInput
from django.utils.translation import ugettext_lazy as _

import selectable.forms as selectable

from lookups import RecipeLookup

class RegistrationForm(forms.Form):
    
    username = forms.CharField(max_length = 20,
                               widget=forms.TextInput(
                               attrs={'class': 'form-control'}))
    firstname = forms.CharField(max_length=20,
                                widget=forms.TextInput(
                                attrs={'class': 'form-control'}))
    lastname = forms.CharField(max_length=20,
                               widget=forms.TextInput(
                               attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=30,
                               widget=forms.TextInput(
                               attrs={'class': 'form-control'}))
    password1 = forms.CharField(max_length = 20, 
                                label='Password', 
                                widget = forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(max_length = 20, 
                                label='Confirm Password',  
                                widget = forms.PasswordInput(attrs={'class': 'form-control'}))
    
    # Overrides the forms.Form.clean function.
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data


    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        return username

# This is for the use of autocomplete
# This is for the use of autocomplete
class AutocompleteSearchForm(forms.Form):
    CHOICES1 = (
         ('', ''), \
         ('Appetizers','Appetizers'), \
         ('Main Dish','Main Dish'), \
         ('Side Dish','Side Dish'), \
         ('Soup','Soup')
         )

    CHOICES2 = (
        ('', ''), \
        ('Poultry','Poultry'), \
        ('Pork','Pork'), \
        ('Beef','Beef'), \
        ('Seafood','Seafood'), \
        ('Vegetables','Vegetables'))


    autocomplete = forms.CharField(
                    label='Hit enter to search',
                    widget=selectable.AutoCompleteWidget(RecipeLookup),
                    required=False,
                   )
    category1 = forms.ChoiceField(choices=CHOICES1, label='category1', required=False)
    category2 = forms.ChoiceField(choices=CHOICES2, label='category2', required=False)

class AddRecipebyURLForm(forms.Form):
    url = forms.CharField(max_length = 100,
                               widget=forms.TextInput(
                               attrs={'class': 'form-control', 'placeholder': 'Add by URL'}))
    
    name = forms.CharField(max_length = 40,
                               widget=forms.TextInput(
                               attrs={'class': 'form-control', 'placeholder': 'Name the recipe'}))
    
    def clean_url(self):
        
        url = self.cleaned_data.get('url')
        if url == '':
            raise forms.ValidationError("Url is empty")
        return url
    
    def clean_name(self):
        
        name = self.cleaned_data.get('name')
        if name == '':
            raise forms.ValidationError("Name is empty")
        return name


# for editing use
class RecipeForm(forms.ModelForm):
    
    name = forms.CharField(max_length = 50,
                               widget=forms.TextInput(
                               attrs={'class': 'form-control'}))
     
    description = forms.CharField(max_length= 1000,
                                  widget=forms.TextInput(
                               attrs={'class': 'form-control'}))
     
    category1 = forms.ChoiceField(choices=[('Appetizers','Appetizers'), \
                                           ('Main Dish','Main Dish'), \
                                           ('Side Dish','Side Dish'), \
                                           ('Soup','Soup')])
    category2 = forms.ChoiceField(choices=[('Poultry','Poultry'), \
                                           ('Pork','Pork'), \
                                           ('Beef','Beef'), \
                                           ('Seafood','Seafood'), \
                                           ('Vegetables','Vegetables')])
     
    spicy = forms.IntegerField(max_value=5, min_value=1, widget=forms.TextInput(
                               attrs={'class': 'rating', 'data-size': "xs", 'data-step':"1"}))
     
    estimated_time = forms.IntegerField(min_value=0, 
                                        widget=forms.NumberInput(
                               attrs={'class': 'form-control',
                                      'placeholder': '0'}))
     
    picture = forms.ImageField(widget=forms.FileInput())

    class Meta:
        model = Recipe
        exclude = ('draft', 'owner', 'steps', 'ingredients', 'utilities', \
                   'calory', 'serving', 'comments', 'rating', 'numRating', \
                   'favorites', 'shares')

# form for adding recipe
class AddInstructionsForm(forms.Form):
    des = forms.CharField(max_length = 200,
                               widget=forms.TextInput(
                               attrs={'class': 'form-control'}))
    
    preptime = forms.IntegerField(min_value=0,
                                  widget=forms.NumberInput(
                               attrs={'class': 'form-control',
                                      'placeholder': '0'}))

    cooktime = forms.IntegerField(min_value=0,
                                  widget=forms.NumberInput(
                               attrs={'class': 'form-control', 
                                      'placeholder': '0'}))
    
    stepPic = forms.ImageField(widget=forms.FileInput(), required = False)

# for editing use
class InstructionsForm(forms.ModelForm):
    description = forms.CharField(max_length = 200,
                               widget=forms.TextInput(
                               attrs={'class': 'form-control'}))
    
    preptime = forms.IntegerField(min_value=0,
                                  widget=forms.NumberInput(
                               attrs={'class': 'form-control',
                                      'placeholder': '0'}))

    cooktime = forms.IntegerField(min_value=0,
                                  widget=forms.NumberInput(
                               attrs={'class': 'form-control', 
                                      'placeholder': '0'}))
    
    stepPic = forms.ImageField(widget=forms.FileInput(), required = False)
    
    class Meta:
        model = Step
        exclude =()

# form for adding recipe
class AddIngredientsForm(forms.Form):
    
    item = forms.CharField(max_length = 20,
                               widget=forms.TextInput(
                               attrs={'class': 'form-control'}))
    
    quantity = forms.IntegerField(min_value=0,
                                  widget=forms.NumberInput(
                               attrs={'class': 'form-control'}))
    
    unit = forms.CharField(max_length = 20,
                               widget=forms.TextInput(
                               attrs={'class': 'form-control'}))

    notes = forms.CharField(max_length = 200,
                               widget=forms.TextInput(
                               attrs={'class': 'form-control'}),
                            required = False)

# for editing use
class IngredientsForm(forms.ModelForm):
    
    item = forms.CharField(max_length = 20,
                               widget=forms.TextInput(
                               attrs={'class': 'form-control'}))
    
    quantity = forms.IntegerField(min_value=0,
                                  widget=forms.NumberInput(
                               attrs={'class': 'form-control'}))
    
    unit = forms.CharField(max_length = 20,
                               widget=forms.TextInput(
                               attrs={'class': 'form-control'}))

    notes = forms.CharField(max_length = 200,
                               widget=forms.TextInput(
                               attrs={'class': 'form-control'}),
                            required = False)
    
    class Meta:
        model = IngredientUnit
        exclude = ('ingredient', )

class RatingForm(forms.Form):
    rate = forms.IntegerField(max_value=5, min_value=1, widget=forms.TextInput(
                               attrs={'class': 'rating', 'data-size': "xs", 'data-step':"1"}))

class CommentForm(forms.Form):
    
    comment = forms.CharField(max_length = 200,
                               widget=forms.TextInput(
                               attrs={'class': 'form-control'}))
    
    def clean(self):
        cleaned_data = super(CommentForm, self).clean()
        
        comment = cleaned_data.get('comment')
        
        if comment == '':
            raise forms.ValidationError("Comment should be non-empty")
        return cleaned_data
    
    
class SearchForm(forms.Form):
    
    text = forms.CharField(max_length = 200,
                               widget=forms.TextInput(
                               attrs={'class': 'form-control', 'placeholder': 'Search'}))
    
    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        
        text = cleaned_data.get('text')
        
        if text == '':
            raise forms.ValidationError("Search field should be non-empty")
        return cleaned_data

class DislikeIngredientForm(forms.Form):
    ingredient = forms.CharField(max_length = 50)
    
class PreferenceForm(forms.ModelForm):
    class Meta:
        model = Allergy
        exclude = ('user', )
        labels = {
            'vegetarian':_('Vegetarian'),
            'dairy': _('Dairy-Free'),
            'egg':_('Egg-Free'),
            'gluten':_('Gluten-Free'),
            'peanut':_('Peanut-Free'),
            'seafood':_('Seafood-Free'),
            'sesame':_('Sesame-Free'),
            'soy':_('Soy-Free'),
            'sulfite':_('Sulfite-Free'),
            'treenut':_('Tree Nut-Free'),
            'wheat':_('Wheat-Free'),
        }

class LeftOverForm(forms.Form):
    ingredient1 = forms.CharField(max_length = 20)
    ingredient2 = forms.CharField(max_length = 20, required=False)
    ingredient3 = forms.CharField(max_length = 20, required=False)