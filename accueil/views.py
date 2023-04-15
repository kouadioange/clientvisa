from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime, timedelta

from .models import *


# Create your views here.
def accueil(request):
    client_achete = Appartenir.objects.all().order_by('-date_created')[:5]
    client = Client.objects.all()
    nombre_client = client.count()
    total_achat = Appartenir.objects.all()
    compte_achat = total_achat.count()
    montant = 0
    for clt in client_achete:
        montant = float(clt.service.montant) * int(clt.quantite)

    verification = Appartenir.objects.all()
    now = datetime.today()
    date = "{}-{}-{}".format(now.year, now.month, now.day)
    date1 = datetime.strptime(date, "%Y-%m-%d").date()

    t = []
    compte = 0
    for expiration in verification:
        date_d = expiration.date_debut
        date_de = "{}-{}-{}".format(date_d.year, date_d.month, date_d.day)
        date_debut = datetime.strptime(date_de, "%Y-%m-%d").date()
        if date_debut <= date1:
            date2 = expiration.date_expiration
            date_expi = "{}-{}-{}".format(date2.year, date2.month, date2.day)
            date_expiration = datetime.strptime(date_expi, "%Y-%m-%d").date()
            date = date_expiration - date1
            jours = date.days
            if jours <= 10:
                t += [expiration]
                compte = compte + 1
        else:
            print("La date de debut n'a pas encore commencée")
    context = {
        'produit_expirer': t,
        'compte': compte,
        'clients': client_achete,
        'montant': montant,
        'compte_achat': compte_achat,
        'nombre_client': nombre_client,
    }

    return render(request, 'accueil/index.html', context)


def ajouter_client(request):
    if request.method == 'POST':
        if 'btn_enregistrer' in request.POST:
            nom_client = request.POST['nom_client']
            prenom_client = request.POST['prenom_client']
            dnaiss_client = request.POST['date_naissance_client']
            residence_client = request.POST.get('residence_client')
            nationalite_client = request.POST.get('nationalite_client')
            sexe_client = request.POST.get('sexe_client')
            email_client = request.POST.get('email_client')
            contact_client = request.POST.get('contact_client')
            numero_passeport_client = request.POST.get('numeroPasseport_client')
            date_expiration_passeport_client = request.POST.get('dateExpirationPasseport_client')
            save_by = request.user

            verifie = Client.objects.filter(numero_passeport=numero_passeport_client)
            if not verifie:
                Client.objects.create(
                    nom=nom_client,
                    prenom=prenom_client,
                    dnaiss=dnaiss_client,
                    residence=residence_client,
                    nationalite=nationalite_client,
                    sexe=sexe_client,
                    email=email_client,
                    contact=contact_client,
                    numero_passeport=numero_passeport_client,
                    date_expiration_passeport=date_expiration_passeport_client,
                    save_by=save_by,
                )
                messages.success(request, 'Enregistrer avec succès')
                print('ok')
            else:
                messages.error(request, 'Enregistrement échoué')
                print('poto')

    return render(request, 'clients/ajouter_client.html')


def liste_client(request):
    listes = Client.objects.all()
    context ={
        'liste': listes
    }
    return render(request, 'clients/liste_client.html', context)

def tous_service(request):
    service = Service.objects.order_by('date_created')

    context = {
        'services': service
    }
    return render(request, 'service/tous_service.html', context)

def enregistrement_service(request):
    service = Service.objects.order_by('-date_created')
    if request.method == 'POST' and 'btn_enregistrer' in request.POST:
        libelle = request.POST.get('libelle_service')
        jours = request.POST.get('jours_service')
        montant = request.POST.get('montant_service')
        services = Service.objects.filter(libelle=libelle)

        if not services:
            Service.objects.create(
                libelle=libelle,
                nombre_jours=jours,
                montant=montant,
            )
            messages.success(request, 'Enregistrer avec succès')
            return redirect('tous_service')
        else:
            messages.error(request, 'Cet Service à deja été Enregistré')
    context = {
        'service': service
    }
    return render(request, 'service/enregistrement_service.html', context)

def choisir_client(request):
    listes = Client.objects.all()
    if request.method == 'POST':
        client = request.POST.get('nom_client')
        client_obj = Client.objects.get(id=client)
        return redirect('/info_client/' + str(client_obj.id) + '/')

    context = {
        'clients': listes,
    }
    return render(request, 'facturation/choisir_client.html', context)

def info_client(request, pk):
    service = Service.objects.all()
    client = Client.objects.filter(id=pk)
    montant_service = 0
    if request.method == 'POST' and 'btn_facturer' in request.POST:
        clt = Client.objects.get(id=pk)
        print(clt)
        recup_date = request.POST.getlist('date_debut')
        recup_montant = request.POST.getlist('montant')
        recup_destination = request.POST.getlist('destination')
        recup_jours = request.POST.getlist('nombre_jours')
        recup_clt = request.POST.getlist('clt')
        recup_quantite = request.POST.getlist('quantite')
        recup_id_service = request.POST.getlist('id_service')
        recup_client = request.POST.getlist('client')
        save_by = request.user
        total = 0
        for i in range(len(service)):
            if recup_quantite[i] == "" and recup_destination[i] == "":
                recup_quantite[i] = 0
                recup_montant[i] = 0
            else:
                montant_service = recup_montant[i]
                quantite = recup_quantite[i]
                date_debut = datetime.strptime(recup_date[i], "%Y-%m-%d").date()
                nombre_jours = recup_jours[i]
                services = recup_id_service[i]
                service_obj = Service.objects.get(id=services)
                destination = recup_destination[i]
                date_expiration = date_debut + timedelta(days=int(nombre_jours))
                total_unitaire = float(montant_service) * int(quantite)
                total += total_unitaire
                verif = Appartenir.objects.filter(destination=destination, date_debut=date_debut)
                if not verif:
                    Appartenir.objects.create(
                        client=clt,
                        service=service_obj,
                        destination=destination,
                        total_unitaire=total_unitaire,
                        quantite=quantite,
                        date_debut=date_debut,
                        date_expiration=date_expiration,
                        save_by=save_by,
                    )
                    print('reussir')
    context = {
        'info_charger': client,
        'services': service,
    }
    return render(request, 'facturation/info_client.html', context)


def caisse(request):
    now = datetime.today()
    date = "{}-{}-{}".format(now.year, now.month, now.day)
    total_journalier = 0
    liste_total_unitaire = Appartenir.objects.filter(date_created=date)

    for tot in liste_total_unitaire:
        total_journalier += tot.total_unitaire
    context = {
        'total': total_journalier
    }
    return render(request, 'caisse/caisse.html', context)
