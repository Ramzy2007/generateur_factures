from pyexpat.errors import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect

from client.models import Client
from .forms import CategorieForm, ProduitForm, FactureForm, DetailFactureForm
from .models import Categorie, Produit, Facture, DetailFacture
from django.template.loader import render_to_string
from xhtml2pdf import pisa

def create_categorie(request):
    if request.method == 'POST':
        form = CategorieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categorie_list')
    else:
        form = CategorieForm()
    return render(request, 'produit/categorie_form.html', {'form': form})

def categorie_list(request):
    categories = Categorie.objects.all()
    return render(request, 'produit/categorie_list.html', {'categories': categories})

def create_produit(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('produit_list')
    else:
        form = ProduitForm()
    return render(request, 'produit/produit_form.html', {'form': form})

def produit_list(request):
    produits = Produit.objects.select_related('categorie').all()
    return render(request, 'produit/produit_list.html', {'produits': produits})

def facture_list(request):
    factures = Facture.objects.all()
    return render(request, 'facture/factures_list.html', {'factures': factures})

def creer_facture(request):
    clients = Client.objects.all()
    categories = Categorie.objects.all()

    if request.method == 'POST':
        client_id = request.POST.get('client')
        category_id = request.POST.get('categorie')
        produit_ids = request.POST.getlist('produits')
        prix = request.POST.getlist('prix')
        quantite = request.POST.getlist('quantite')
        date = request.POST.get('date')

        # Extract prices and quantities
        prix = {}
        quantite = {}
        for key, value in request.POST.items():
            if key.startswith('prix_'):
                produit_id = key.split('_')[1]
                prix[produit_id] = float(value)
            elif key.startswith('quantite_'):
                produit_id = key.split('_')[1]
                quantite[produit_id] = int(value)

        client = Client.objects.get(id=client_id)
        facture = Facture.objects.create(
            client=client,
            date=date
        )


        # Process each product ID
        for produit_id in produit_ids:
            produit = Produit.objects.get(pk=produit_id)

            print(f"Produit_id 855: {produit_id}")

            # Ensure produit_id is a string
            produit_id_str = str(produit_id)

            print(f"Produit_id: {produit_id_str}")

            produit_prix = prix.get(produit_id_str, 0.0)
            produit_quantite = quantite.get(produit_id_str, 0)


            print(f"Product ID: {produit_id_str}, Price: {produit_prix}, Quantity: {produit_quantite}")

            DetailFacture.objects.create(
                facture=facture,
                produit=produit,
                quantite=produit_quantite,
                prix=produit_prix
            )

        # Calculate total
        facture.total = sum(
            d.prix * d.quantite * (1 + d.produit.tva / 100) for d in facture.detailfacture_set.all()
        )
        print("###############################")
        print(facture.total )
        print("###############################")
        facture.save()

        return redirect('facture_list')  # Redirection vers la liste des factures

    return render(request, 'facture/creer_facture.html', {'clients': clients, 'categories': categories})

def get_produits_by_categorie(request):
    categorie_id = request.GET.get('categorie_id')
    produits = Produit.objects.filter(categorie=categorie_id)
    return JsonResponse({'produits': list(produits.values('id', 'nom', 'prix'))})

def modifier_facture(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    clients = Client.objects.all()
    categories = Categorie.objects.all()
    
    # Prepare a list of selected product IDs
    # selected_produit_ids = facture.produits.values_list('pk', flat=True)

    if request.method == 'POST':
        # Handle the POST request to update the facture
        client_id = request.POST.get('client')
        facture.client = get_object_or_404(Client, pk=client_id)
        facture.date = request.POST['date']
        facture.save()

        # Suppression des détails existants
        DetailFacture.objects.filter(facture=facture).delete()

        produits = request.POST.getlist('produits')
        for produit_id in produits:
            produit = get_object_or_404(Produit, pk=produit_id)
            prix = request.POST[f'prix_{produit_id}']
            quantite = request.POST[f'quantite_{produit_id}']
            DetailFacture.objects.create(facture=facture, produit=produit, prix=prix, quantite=quantite)

        return redirect('facture_list')

    context = {
        'facture': facture,
        'clients': clients,
        'categories': categories,
    }
    return render(request, 'facture/modifier_facture.html', context)

def add_produits(request):
    facture_id = request.session.get('facture_id')
    facture = Facture.objects.get(id=facture_id)

    if request.method == 'POST':
        produit_id = request.POST.get('produit')
        quantite = request.POST.get('quantite')
        prix = request.POST.get('prix')
        produit = Produit.objects.get(id=produit_id)
        DetailFacture.objects.create(facture=facture, produit=produit, quantite=quantite, prix=prix)
        return redirect('generer_facture_pdf')

    categories = Categorie.objects.all()
    return render(request, 'produit/add_produits.html', {'categories': categories})

def generer_facture_pdf(request, pk):
    facture_id = pk
    facture = get_object_or_404(Facture, pk=facture_id)
    details = []

    print(f"Prices: {facture}")

    context = {
        'facture': facture,
        'details': []
    }

    for detail in facture.detailfacture_set.all():

        #facture.produits.set(produit_ids)
        try:
            produit = detail.produit
            produit_prix = float(detail.prix) if detail.prix else 0.0
            produit_quantite = int(detail.quantite) if detail.quantite else 0
            produit_tva = produit.tva if produit.tva else 0
            print(f"Prices-------: { (1 + produit_tva / 100)}")

            print(f"Prices---7777----: { produit_prix}")
            tva = (1 + produit_tva / 100)
            prix_ttc = float(produit_prix) * float(tva)
            print(f"Prices---777788888----: { prix_ttc}")
            total_ligne = float(produit_quantite )* float(prix_ttc)
                    # Debugging information
            
            print(f"Quantities*********: {total_ligne}")

            context['details'].append({
                'description': produit.description,
                'prix': produit.prix,
                'tva': produit.tva,
                'produit': produit,
                'quantite': produit_quantite,
                'prix_ttc': prix_ttc,
                'total_ligne': total_ligne
            })

            

        except (ValueError, TypeError) as e:
            # Handle invalid data gracefully
            context['details'].append({
                'produit': detail.produit,
                'quantite': 0,
                'prix_ttc': 0,
                'total_ligne': 0
            })
    
    context = {
        'facture': facture,
        'details': context['details'],
        'total_facture': sum(detail['total_ligne'] for detail in context['details'])
    }
    
    print(f"Context: {context}")
    # Render the HTML template with the context
    html_string = render_to_string('facture/facture_pdf.html', context)
    
    # Create a HttpResponse object to hold the PDF content
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=facture_{facture.id}.pdf'
    
    # Convert HTML to PDF
    result = pisa.CreatePDF(html_string, dest=response)
    
    # If there's an error, return it
    if result.err:
        return HttpResponse('We encountered some errors <pre>' + html_string + '</pre>')
    
    return response


def imprimer_facture(request, pk):
    facture = get_object_or_404(Facture, id=pk)
    
    html_string = render_to_string('facture/facture_pdf.html', {'facture': facture})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=facture_{facture.id}.pdf'

    pisa_status = pisa.CreatePDF(html_string, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Une erreur est survenue lors de la génération du PDF.')

    return response