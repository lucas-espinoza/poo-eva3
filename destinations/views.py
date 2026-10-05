from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import DestinationForm
from .models import Destination


@staff_member_required
def destination_list(request):
    return render(request, "destinations/list.html", {"destinations": Destination.objects.all()})


@staff_member_required
def destination_create(request):
    form = DestinationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("destinations:list")
    return render(request, "destinations/form.html", {"form": form})


@staff_member_required
def destination_edit(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    form = DestinationForm(request.POST or None, instance=destination)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("destinations:list")
    return render(request, "destinations/form.html", {"form": form, "destination": destination})


@staff_member_required
@require_POST
def destination_remove(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if destination.package_links.exists():
        destination.is_available = False
        destination.save(update_fields=["is_available", "updated_at"])
    else:
        destination.delete()
    return redirect("destinations:list")
