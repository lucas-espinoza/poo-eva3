from datetime import date
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import PackageForm
from .models import Package
from .services import publish_package, save_draft


@login_required
def catalog(request):
    offers = Package.objects.filter(status=Package.Status.PUBLISHED, is_enabled=True, departure_date__gt=date.today())
    return render(request, "packages/catalog.html", {"packages": offers})


@login_required
def customer_detail(request, pk):
    package = get_object_or_404(Package, pk=pk, status=Package.Status.PUBLISHED, is_enabled=True, departure_date__gt=date.today())
    return render(request, "packages/detail.html", {"package": package})


@staff_member_required
def package_list(request):
    return render(request, "packages/list.html", {"packages": Package.objects.all()})


@staff_member_required
def package_create(request):
    form = PackageForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        package = form.save(commit=False)
        try:
            save_draft(package, form.cleaned_data["destinations"])
        except ValidationError as error:
            form.add_error(None, error)
        else:
            return redirect("packages:staff_detail", pk=package.pk)
    return render(request, "packages/form.html", {"form": form})


@staff_member_required
def package_edit(request, pk):
    package = get_object_or_404(Package, pk=pk)
    if package.status == Package.Status.PUBLISHED:
        raise Http404
    form = PackageForm(request.POST or None, instance=package)
    if request.method == "POST" and form.is_valid():
        try:
            save_draft(form.save(commit=False), form.cleaned_data["destinations"])
        except ValidationError as error:
            form.add_error(None, error)
        else:
            return redirect("packages:staff_detail", pk=package.pk)
    return render(request, "packages/form.html", {"form": form, "package": package})


@staff_member_required
def staff_detail(request, pk):
    package = get_object_or_404(Package, pk=pk)
    return render(request, "packages/staff_detail.html", {"package": package, "preview": package.current_price})


@staff_member_required
@require_POST
def publish(request, pk):
    package = get_object_or_404(Package, pk=pk)
    try:
        publish_package(package)
    except ValidationError:
        pass
    return redirect("packages:staff_detail", pk=pk)


@staff_member_required
@require_POST
def toggle_enabled(request, pk):
    package = get_object_or_404(Package, pk=pk)
    if package.status == Package.Status.PUBLISHED:
        package.is_enabled = not package.is_enabled
        package.save(update_fields=["is_enabled", "updated_at"])
    return redirect("packages:staff_detail", pk=pk)
