from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),             # Home Page
    path('jobs/', views.jobs, name='jobs'),        # Job Listings
    path('safety/', views.safety, name='safety'),  # Safety Section
    path('learning/', views.learning, name='learning'),  # Learning Section
    path('community/', views.community, name='community'),  # Community Forums
    path('profile/', views.profile, name='profile'),  # User Profile
    path('community/', views.community, name='community'),
    path('discussion/<int:discussion_id>/', views.discussion_detail, name='discussion_detail'),

    # Authentication URLs
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]

