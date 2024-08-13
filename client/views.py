from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClientForm
from .models import Client

def home(request):

	return render(request, 'dashboard/home.html')

def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')  # Redirige vers la liste des clients ou une autre page
    else:
        form = ClientForm()
    return render(request, 'client/client_form.html', {'form': form})

def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'client/client_detail.html', {'client': client})

def client_list(request):
    clients = Client.objects.all()
    return render(request, 'client/client_list.html', {'clients': clients})
