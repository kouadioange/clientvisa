
from django.urls import path
from .views import *

urlpatterns = [
    path('', accueil, name='accueil'),
    path('Enregistrement_client/', ajouter_client, name='ajouter_client'),
    path('liste_client/', liste_client, name='liste_client'),
    path('ajouter_client/', ajouter_client, name='ajouter_client'),
    path('Enregistrement_service/', enregistrement_service, name='enregistrement_service'),
    path('tous_service/', tous_service, name='tous_service'),
    path('choisir_client/', choisir_client, name='choisir_client'),
    path('info_client/<int:pk>/', info_client, name='info_client'),
    path('caisse/', caisse, name='caisse'),
    path('client_a_appeler/', client_expirer, name='client_expirer'),
]
