from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup', views.signup_view, name='signup'),
    path('goals', views.goals, name='goals'),
    path('moodlogin', views.moodlogin, name='moodlogin'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('add_challenge', views.add_challenge, name='add_challenge'),
    path('journaling', views.journaling, name='journaling'),
    path('add_goal', views.add_goal, name='add_goal'), 
    path('remove_goals', views.remove_goals, name='remove_goals'),
    path('mood-graph/', views.mood_graph, name='mood-graph'),

]
