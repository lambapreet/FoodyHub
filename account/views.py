from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib import messages
from .models import *

# Create your views here.

def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            
            # user = form.save(commit=False)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('registerUser')  # Redirect to login page or another valid view
        else:
            messages.error(request, "Registration failed. Please check the form and try again.")
    else:
        form = UserForm()

    context = {'form': form}
    return render(request, 'account/registerUser.html', context)
