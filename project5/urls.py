from django.urls import include, re_path
from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("projects", views.projects, name="projects"),
    path("archived", views.archived, name="archived"),
    path("create_project", views.create_project, name="create_project"),
    path('update_project/<int:project_id>/', views.update_project, name='update_project'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('archive_project/<int:project_id>/', views.archive_project, name='archive_project'),
    path('unarchive_project/<int:project_id>/', views.unarchive_project, name='unarchive_project'),
    path('manage_project/<int:project_id>/', views.manage_project, name='manage_project'),
    path('get_events/<int:project_id>/', views.get_events, name='get_events'),
    path('create_event/<int:project_id>/', views.create_event, name='create_event'),
    path('update_event/<int:project_id>/<int:event_id>/', views.update_event, name='update_event'),
    path('delete_event/<int:project_id>/<int:event_id>/', views.delete_event, name='delete_event'),
] 
