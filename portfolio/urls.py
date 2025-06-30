from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('contact/', views.contact, name='contact'),
    path('terms/', views.terms, name='terms'),
    path('ajax/validate-field/', views.validate_contact_field, name='validate_contact_field'),
]
