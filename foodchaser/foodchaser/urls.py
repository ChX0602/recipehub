from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
	
    # Route for built-in authentication with our own custom login page
    url(r'^loginandregister$', 'django.contrib.auth.views.login', {'template_name':'foodchaser/registerandlogin.html'}, name='login'),

    # Route to logout a user and send them back to the login page
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login'),

    url(r'^register$', 'foodchaser.views.register', name='register'),

    url(r'^userhome$', 'foodchaser.views.userhome', name='home'),

    url(r'^trial$', 'foodchaser.views.trial'),

    url(r'^recommend$', 'foodchaser.views.recommendpage', name='recommend'),

    url(r'^menuplanner$', 'foodchaser.views.menuplanner', name='menuplanner'),

    # any token produced by the default_token_generator
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', 'foodchaser.views.confirm_registration', name='confirm'),

    url(r'^add_recipe$', 'foodchaser.handle_recipe.add_recipe', name='add_recipe'),

    url(r'^confirm-reset-password/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<new_password>[a-zA-Z0-9_@\+\- ]+)/(?P<token>[a-z0-9\-]+)$', 'foodchaser.views.confirm_resetpassword', name='confirmpassword'),

    url(r'^changepassword$', 'foodchaser.views.change_password'),

    url(r'^recipebox_maindish$', 'foodchaser.handle_recipe.recipebox_maindish', name='recipebox_maindish'),
	
    url(r'^recipe_view/(?P<id>\d+)$', 'foodchaser.handle_recipe.recipe_view', name='recipe_view'),
	
    url(r'^search$', 'foodchaser.handle_recipe.search', name='search'),

    url(r'^recipe/photo/(?P<id>\d+)$', 'foodchaser.views.get_recipe_picture'),
                       
    url(r'^step/photo/(?P<id>\d+)$', 'foodchaser.views.get_step_picture'),

    url(r'^rate$', 'foodchaser.handle_recipe.rate', name='rate'),

    url(r'^comment$', 'foodchaser.handle_recipe.comment', name='comment'),

    url(r'^settings$', 'foodchaser.views.settings_page', name='settings'),

    url(r'^virtual_restaurant$', 'foodchaser.views.virtual_restaurant', name='virtual_restaurant'),

    url(r'^virtual_restaurant_menu$', 'foodchaser.views.virtual_restaurant_menu', name='virtual_restaurant_menu'),

    url(r'^favorites$', 'foodchaser.views.get_favorites', name='favorites'),

    url(r'^add_favorite/(?P<id>\d+)$', 'foodchaser.views.add_favorite', name='add_favorite'),

    url(r'^preference$', 'foodchaser.views.preference', name='preference'),

    url(r'^add-dislike$', 'foodchaser.views.add_dislike', name='dislike'),
    
    url(r'^edit/(?P<id>\d+)$', 'foodchaser.handle_recipe.edit', name='edit'),

    url(r'^save_planner$', 'foodchaser.views.save_planner', name='save_planner'),

    url(r'^get_planner$', 'foodchaser.views.get_planner', name='get_planner'),
    
    url(r'^delete/(?P<id>\d+)$', 'foodchaser.handle_recipe.delete', name='delete'),

    url(r'^changemyprofile$', 'foodchaser.views.changemyprofile'),

    url(r'^leftover$', 'foodchaser.views.use_leftover', name='leftover'),

    url(r'^suggest-leftover$', 'foodchaser.views.suggest_leftover', name='suggest_leftover')

)
