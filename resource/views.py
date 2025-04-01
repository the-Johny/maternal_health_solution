from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from myapp.models import Doctor
from .forms import EducationalResourceForm
from .models import EducationalResource


def resource_list(request):
    """
    View to display all educational resources, with optional filtering by category.
    """
    category = request.GET.get('category')
    if category and category != 'all':
        resources = EducationalResource.objects.filter(category=category).order_by('-created_at')
    else:
        resources = EducationalResource.objects.all().order_by('-created_at')

    # Get unique categories for the filter
    categories = EducationalResource.objects.values_list('category', flat=True).distinct()

    context = {
        'resources': resources,
        'categories': categories,
        'current_category': category or 'all',
    }
    return render(request, 'resources/resource_list.html', context)


def resource_detail(request, resource_id):
    """
    View to display a single educational resource in detail.
    """
    resource = get_object_or_404(EducationalResource, id=resource_id)
    context = {
        'resource': resource,
    }
    return render(request, 'resources/resource_detail.html', context)


@login_required
def add_resource(request):
    """
    View to add a new educational resource.
    Only doctors can add resources.
    """
    # Check if the user is a doctor
    if not request.user.is_doctor:
        messages.error(request, "Only doctors can create educational resources.")
        return redirect('resource_list')

    try:
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        messages.error(request, "Doctor profile not found.")
        return redirect('resource_list')

    if request.method == 'POST':
        form = EducationalResourceForm(request.POST)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.author = doctor
            resource.save()
            messages.success(request, "Educational resource created successfully.")
            return redirect('resource_detail', resource_id=resource.id)
    else:
        form = EducationalResourceForm()

    context = {
        'form': form,
    }
    return render(request, 'resources/add_resource.html', context)


@login_required
def edit_resource(request, resource_id):
    """
    View to edit an existing educational resource.
    Only the author can edit their own resources.
    """
    resource = get_object_or_404(EducationalResource, id=resource_id)

    # Check if the user is a doctor
    if not request.user.is_doctor:
        messages.error(request, "Only doctors can edit resources.")
        return redirect('resource_detail', resource_id=resource.id)

    try:
        doctor = request.user.doctor_profile
        if doctor != resource.author:
            messages.error(request, "You can only edit your own resources.")
            return redirect('resource_detail', resource_id=resource.id)
    except Doctor.DoesNotExist:
        messages.error(request, "Doctor profile not found.")
        return redirect('resource_detail', resource_id=resource.id)

    if request.method == 'POST':
        form = EducationalResourceForm(request.POST, instance=resource)
        if form.is_valid():
            form.save()
            messages.success(request, "Resource updated successfully.")
            return redirect('resource_detail', resource_id=resource.id)
    else:
        form = EducationalResourceForm(instance=resource)

    context = {
        'form': form,
        'resource': resource,
    }
    return render(request, 'resources/edit_resource.html', context)