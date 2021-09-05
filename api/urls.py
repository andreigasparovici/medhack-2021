from . import views

from django.urls import path

urlpatterns = [
    path('diagnostics/', views.DiagnosticsList.as_view(), name='diagnostics_list'),
    path('comorbidities/', views.ComorbiditiesList.as_view(), name='comorbidities_list'),
    path('register/', views.register, name='register'),
    path('menu/', views.generate_menu, name='generate_menu'),
    path('test-auth/', views.test_auth)
]
