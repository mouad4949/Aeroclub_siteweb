from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import News,avions,Profile
from .forms import CustomUserCreationForm,EmailAuthenticationForm
from django.contrib.auth.models import User
def index(request):
    actualité=News.objects.order_by("-id")
    av=avions.objects.order_by("-id")
    avions_count=avions.objects.count()
    prof=Profile.objects.filter(type_pilote="pilote_licencié")
    pilotes_count=prof.count()
    context={"actualité":actualité,"av":av,"prof":prof,"avions_count":avions_count,"pilotes_count":pilotes_count}
    return render(request,"app/index.html",context)

def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Rediriger vers la page d'accueil après une connexion réussie
            else:
                messages.error(request, 'Invalid email or password')
        else:
            messages.error(request, 'Formulaire n\'est pas valide')
            print(form.errors)  # Pour le débogage
    else:
        form = EmailAuthenticationForm()
    return render(request, 'app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def Register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully!')
            return redirect('login')  # Rediriger vers la page de connexion après l'inscription réussie
    else:
        form = CustomUserCreationForm()
    return render(request, 'app/register.html', {'form': form})