from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User

# Each step of a recipe
class Step(models.Model):
    description = models.CharField(max_length=200, null=True, blank=True)
    # Each step can come with an optional picture
    picture = models.ImageField(null=True, blank=True, upload_to='step')
    # The preparation time to be spent on this step, default is 0
    preptime = models.IntegerField(max_length=10, default=0)
    # The cook time to be spent on this step, default is 0
    cooktime = models.IntegerField(max_length=10, default=0)

# Ingredients database, should be predefined for user
class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    # Possible allergies of the ingredient
    kinds = (('Dairy', 'Dairy'), ('Egg','Egg'), ('Gluten','Gluten'),
             ('Peanut' ,'Peanut'), ('Seafood', 'Seafood'), ('Sesame', 'Sesame'),
             ('Soy', 'Soy'), ('Sulfite', 'Sulfite'), ('Treenut', 'Tree Nut'),
             ('Wheat', 'Wheat'))
    allergy = models.CharField(max_length=10, null=True, blank=True,
                              choices=kinds, default='None')
    # The calory of the ingredient per unit
    calory = models.IntegerField(max_length=10, default=0)

# Integrate a ingredient with some quantity
class IngredientUnit(models.Model):
    ingredient = models.ForeignKey(Ingredient, null=True)
    quantity = models.IntegerField(max_length=10, default=0)
    unit = models.CharField(max_length=20)
    notes = models.CharField(max_length=200, default='')
    
# Cooking utilities, should be predefined for user
class Utility(models.Model):
    name = models.CharField(max_length=200)

# Comments of recipe from other users
class Comment(models.Model):
    text = models.CharField(max_length=200)
    # Note: owner is string of the user name instead of User object.
    owner = models.CharField(max_length=200, default='')
    # time of creation
    time = models.DateTimeField(auto_now_add=True)

# For the bookmarklet feature. 
class Link(models.Model):
    name = models.CharField(max_length=200)
    # The link to other websites
    link = models.CharField(max_length=200)

# Recipe model
class Recipe(models.Model):
    draft = models.BooleanField(default='False')
    name = models.CharField(max_length=50, default='Recipe')
    # cover picture for the recipe
    picture = models.ImageField(null=True, blank=True, upload_to='recipe')
    description = models.CharField(max_length=1000, null=True, blank=True)
    category1 = models.CharField(max_length=20, default='Other')
    category2 = models.CharField(max_length=20, default='Other')
    owner = models.ForeignKey(User)
    steps = models.ManyToManyField(Step)
    # specifies ingredients and quantity
    ingredients = models.ManyToManyField(IngredientUnit)
    utilities = models.ManyToManyField(Utility)
    # calory of recipe: multiply ingredients' calories by quantity
    
    # how spicy it is
    spicy = models.IntegerField(max_length=5, default=0)
    # and thene sum up
    calory = models.IntegerField(max_length=10, default=0)
    # number of servings
    serving = models.IntegerField(max_length=10, default=0)
    # other users' comments
    comments = models.ManyToManyField(Comment)
    # time of creation of the recipe
    time = models.DateTimeField(auto_now_add=True)
    # the average rating of recipe
    rating = models.FloatField(default=0)
    # the number of ratings by other user
    numRating = models.IntegerField(max_length=10, default=0)
    # the number of favorites by other user
    favorites = models.IntegerField(max_length=10, default=0)
    # the number of shares by other user
    shares = models.IntegerField(max_length=10, default=0)

    # estimated time
    estimated_time = models.IntegerField(max_length=10, default=0)
    
# Rating's database for the monthly best feature.
class Rate(models.Model):
    recipe = models.ForeignKey(Recipe)
    rate = models.FloatField(max_length=10)
    time = models.DateTimeField(auto_now_add=True)

# Links a user to a third-party account
class SocialNetWorkLink(models.Model):
    user = models.OneToOneField(User)
    # source of the third-party (e.g. FB, Twitter, etc)
    source = models.CharField(max_length=20)
    # third-party account
    account = models.CharField(max_length=200)

##class SearchHistory(models.Model):
##    text = models.CharField(max_length = 100)
    
# Rout1ine profile
class Profile(models.Model):
    user = models.OneToOneField(User)
    firstname = models.CharField(max_length=20, null=True, blank=True, default='')
    lastname = models.CharField(max_length=20, null=True, blank=True, default='')
    description = models.CharField(max_length=200, null=True, blank=True, default='')
    choices = (('None', 'None'), ('Male', 'Male'), ('Female', 'Female'),)
    gender = models.CharField(max_length=10, null=True, blank=True,
                              choices=choices, default='None')
    age = models.IntegerField(max_length=10, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True,
                                default='')
    photo = models.ImageField(upload_to='user', null=True, blank=True)
    # preference for ingredients
    preference = models.ManyToManyField(Ingredient)
    # enable newsletter or not
    newsletter = models.BooleanField(blank=True, default=True)

    search_history = models.ManyToManyField(Recipe)
    

# allergies
class Allergy(models.Model):
    user = models.OneToOneField(User)

    vegetarian = models.BooleanField(default = False)
    dairy = models.BooleanField(default = False)
    egg = models.BooleanField(default = False)
    gluten = models.BooleanField(default = False)
    peanut = models.BooleanField(default = False)
    seafood = models.BooleanField(default = False)
    sesame = models.BooleanField(default = False)
    soy = models.BooleanField(default = False)
    sulfite = models.BooleanField(default = False)
    treenut = models.BooleanField(default = False)
    wheat = models.BooleanField(default = False)

# Maps a user to its followers
class Follower(models.Model):
    user = models.OneToOneField(User)
    followers = models.ManyToManyField(User, related_name='%(class)s_followers')

# Maps a user to its favorited recipes
class Favorite(models.Model):
    user = models.OneToOneField(User)
    favorites = models.ManyToManyField(Recipe)

# Maps a user to its collection of recipes from other sources
class BookMarklet(models.Model):
    user = models.OneToOneField(User)
    links = models.ManyToManyField(Link)

# Maps a user to its level data
class LevelData(models.Model):
    user = models.OneToOneField(User)
    # total login time
    loginTime = models.IntegerField(max_length=200, default=0)
    # based on user's activeness of favorites, shares, ratings on other recipes
    activityScore = models.IntegerField(max_length=200, default=0)
    # based on favorites gotton from other users
    favoriteScore = models.IntegerField(max_length=200, default=0)
    # based on shares gotton from other users
    shareScore = models.IntegerField(max_length=200, default=0)
    # based on ratings gotton from other users
    ratingScore = models.IntegerField(max_length=200, default=0)
    # editor or not
    editor = models.BooleanField(blank=True, default=False)

# Xing's new idea of menu feature opened to high-level users
# User customize its own menu and can share to others
class Menu(models.Model):
    user = models.ForeignKey(User)
    # what user includes in its menu
    appetizer = models.ManyToManyField(Recipe, related_name='%(class)s_appetizer')
    salad = models.ManyToManyField(Recipe, related_name='%(class)s_salad')
    mainCourse = models.ManyToManyField(Recipe, related_name='%(class)s_main')
    dessert = models.ManyToManyField(Recipe, related_name='%(class)s_dessert')
    drink = models.ManyToManyField(Recipe, related_name='%(class)s_drink')

class Planner(models.Model):
    user = models.ForeignKey(User)
    sunday_breakfast = models.ManyToManyField(Recipe, related_name = 'sunday_b')
    sunday_lunch = models.ManyToManyField(Recipe, related_name = 'sunday_l')
    sunday_dinner = models.ManyToManyField(Recipe, related_name = 'sunday_d')
    monday_breakfast = models.ManyToManyField(Recipe, related_name = 'monday_b')
    monday_lunch = models.ManyToManyField(Recipe, related_name = 'monday_l')
    monday_dinner = models.ManyToManyField(Recipe, related_name = 'monday_d')
    tuesday_breakfast = models.ManyToManyField(Recipe, related_name = 'tuesday_b')
    tuesday_lunch = models.ManyToManyField(Recipe, related_name = 'tuesday_l')
    tuesday_dinner = models.ManyToManyField(Recipe, related_name = 'tuesday_d')
    wednesday_breakfast = models.ManyToManyField(Recipe, related_name = 'wednesday_b')
    wednesday_lunch = models.ManyToManyField(Recipe, related_name = 'wednesday_l')
    wednesday_dinner = models.ManyToManyField(Recipe, related_name = 'wednesday_d')
    thursday_breakfast = models.ManyToManyField(Recipe, related_name = 'thurday_b')
    thursday_lunch = models.ManyToManyField(Recipe, related_name = 'thursday_l')
    thursday_dinner = models.ManyToManyField(Recipe, related_name = 'thursday_d')
    friday_breakfast = models.ManyToManyField(Recipe, related_name = 'friday_b')
    friday_lunch = models.ManyToManyField(Recipe, related_name = 'friday_l')
    friday_dinner = models.ManyToManyField(Recipe, related_name = 'friday_d')
    saturday_breakfast = models.ManyToManyField(Recipe, related_name = 'saturday_b')
    saturday_lunch = models.ManyToManyField(Recipe, related_name = 'saturday_l')
    saturday_dinner = models.ManyToManyField(Recipe, related_name = 'saturday_d')
    
