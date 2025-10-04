from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import BloodCamp
from blood_requests.models import BloodRequest
from .forms import BloodCampForm

@login_required
def create_camp(request):
    if request.method == "POST":
        form = BloodCampForm(request.POST)
        if form.is_valid():
            camp = form.save(commit=False)
            camp.organizer = request.user
            camp.save()
            messages.success(request, "✅ Blood camp created successfully!")
            return redirect("blood_camp:camp_list")
        else:
            messages.error(request, "❌ Please correct the errors below.")
    else:
        form = BloodCampForm()

    return render(request, "blood_camp/create_camp.html", {"form": form})

@login_required
def camp_list(request):
    """
    List all upcoming blood camps and today's camps.
    Automatically deletes camps older than yesterday.
    """
    yesterday = timezone.now().date() - timedelta(days=1)
    BloodCamp.objects.filter(date__lt=yesterday).delete()

    camps = BloodCamp.objects.filter(date__gte=yesterday).order_by("date")
    return render(request, "blood_camp/camp_list.html", {"camps": camps})

@login_required
def dashboard(request):
    """
    Dashboard showing stats, recent camps, and recent requests.
    """
    yesterday = timezone.now().date() - timedelta(days=1)
    BloodCamp.objects.filter(date__lt=yesterday).delete()

    # Camps
    all_camps = BloodCamp.objects.filter(date__gte=yesterday).order_by("date")
    total_camps = BloodCamp.objects.count()
    upcoming_camps = all_camps.count()
    recent_camps = all_camps.order_by("-created_at")[:5]  # latest 5

    # Requests
    all_requests = BloodRequest.objects.all().order_by("-created_at")
    total_requests = all_requests.count()
    recent_requests = all_requests[:5]

    # Accepted requests (assuming accepted_donors exists and is ManyToManyField)
    accepted_requests = [r for r in all_requests if r.accepted_donors.exists()]

    context = {
        "total_camps": total_camps,
        "upcoming_camps": upcoming_camps,
        "total_requests": total_requests,
        "recent_camps": recent_camps,
        "recent_requests": recent_requests,
        "accepted_requests": accepted_requests,
    }
    return render(request, "blood_camp/dashboard.html", context)

@login_required
def delete_camp(request, camp_id):
    camp = get_object_or_404(BloodCamp, id=camp_id)
    if request.user != camp.organizer:
        return HttpResponseForbidden("❌ You cannot delete this camp.")
    if request.method == "POST":
        camp.delete()
        messages.success(request, "✅ Camp deleted successfully.")
        return redirect("blood_camp:camp_list")
    return render(request, "blood_camp/confirm_delete.html", {"camp": camp})





def edit_camp(request, pk):
    camp = get_object_or_404(BloodCamp, pk=pk)
    if request.method == "POST":
        form = BloodCampForm(request.POST, instance=camp)
        if form.is_valid():
            form.save()
            return redirect('blood_camp:camp_list')
    else:
        form = BloodCampForm(instance=camp)
    return render(request, 'blood_camp/edit_camp.html', {'form': form, 'camp': camp})
