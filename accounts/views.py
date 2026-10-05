from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from .forms import EmailAuthenticationForm, RegistrationForm

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(); login(request, user); return redirect("packages:catalog")
        # RUT and telephone are protected profile data: never re-render them after an error.
        safe_data = form.data.copy()
        safe_data["rut"] = ""
        safe_data["telephone"] = ""
        form.data = safe_data
    else: form = RegistrationForm()
    return render(request, "accounts/register.html", {"form": form})
class EmailLoginView(LoginView):
    template_name = "accounts/login.html"; authentication_form = EmailAuthenticationForm
class EmailLogoutView(LogoutView):
    next_page = "packages:catalog"
