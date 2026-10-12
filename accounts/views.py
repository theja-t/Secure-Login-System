from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .forms import RegistrationForm


@require_http_methods(['GET', 'POST'])
def signup(request):
	if request.user.is_authenticated:
		return redirect('dashboard')

	form = RegistrationForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		user = form.save()
		login(request, user, backend='django.contrib.auth.backends.ModelBackend')
		messages.success(request, 'Your account is ready.')
		return redirect('dashboard')

	return render(request, 'accounts/signup.html', {'form': form})


@login_required
def dashboard(request):
	return render(request, 'accounts/dashboard.html')
