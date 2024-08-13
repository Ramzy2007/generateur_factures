from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClientForm
from .models import Client

def home(request):

	return render(request, 'dashboard/home.html')

def create_client(request):
    if request.method == 'POST':

        csrf_token = request.POST.get('csrfmiddlewaretoken')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        adresse = request.POST.get('adresse')
        code_postal = request.POST.get('code_postal')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')

        print(f'Nom: {nom}')
        print(f'Prénom: {prenom}')
        print(f'Adresse: {adresse}')
        print(f'Code Postal: {code_postal}')
        print(f'Email: {email}')
        print(f'Téléphone: {telephone}')

        client = Client(
            nom=nom,
            prenom=prenom,
            adresse=adresse,
            code_postal=code_postal,
            email=email,
            telephone=telephone
        )
        client.save()
        return redirect('client_list')  # Redirige vers la liste des clients ou une autre page
    
    form = ClientForm()
    return render(request, 'client/client_form.html', {'form': form})

def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'client/client_detail.html', {'client': client})

def client_list(request):
    clients = Client.objects.all()
    return render(request, 'client/client_list.html', {'clients': clients})
