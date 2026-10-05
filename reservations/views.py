from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from packages.models import Package
from .forms import ReservationForm
from .models import Reservation
from .services import create_reservation, transition_reservation


@login_required
def create(request, package_pk):
    package = get_object_or_404(Package, pk=package_pk)
    form = ReservationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            reservation, created = create_reservation(client=request.user, package=package, people_count=form.cleaned_data["people_count"], token=form.cleaned_data["submission_token"])
        except ValidationError as error:
            form.add_error(None, error)
        else:
            return redirect("reservations:detail", pk=reservation.pk)
    return render(request, "reservations/form.html", {"form": form, "package": package})


@login_required
def history(request):
    return render(request, "reservations/history.html", {"reservations": Reservation.objects.filter(client=request.user)})


@login_required
def detail(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, client=request.user)
    return render(request, "reservations/detail.html", {"reservation": reservation})


@staff_member_required
def admin_list(request):
    return render(request, "reservations/admin_list.html", {"reservations": Reservation.objects.select_related("client", "package")})


@staff_member_required
@require_POST
def transition(request, pk, state):
    reservation = get_object_or_404(Reservation, pk=pk)
    try:
        transition_reservation(reservation, state)
    except ValidationError:
        pass
    return redirect("reservations:admin_list")
