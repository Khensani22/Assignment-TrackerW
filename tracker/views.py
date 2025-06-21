from django.shortcuts import render, redirect, get_object_or_404
from .models import Assignment
from .forms import AssignmentForm
from django.utils import timezone
from datetime import date, timedelta

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib.auth.views import LoginView
from django.views.decorators.http import require_GET
from django.contrib.auth import logout
 
@login_required
def assignments_list(request):
    
    assignments = Assignment.objects.filter(user=request.user)  # Filter assignments by user

    # Count statuses
    completed_count = assignments.filter(status__iexact='Completed').count()
    in_progress_count = assignments.filter(status__iexact='In Progress').count()
    not_started_count = assignments.filter(status__iexact='Not Started').count()

    context = {
        'assignments': assignments,
        'completed_count': completed_count,
        'in_progress_count': in_progress_count,
        'not_started_count': not_started_count,
    }

    return render(request, 'addlist/assignments_list.html', context)

# Add or Update an assignment
@login_required
def add_assignment(request, assignment_id=None):
    assignment = get_object_or_404(Assignment, id=assignment_id, user=request.user) if assignment_id else None

    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.user = request.user  # Associate the assignment with the logged-in user
            assignment.save()
            return redirect('assignments_list')
    else:
        form = AssignmentForm(instance=assignment)

    return render(request, 'addlist/add_assignment.html', {'form': form})

# Delete an assignment
@login_required
def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, user=request.user)  # Ensure the assignment belongs to the user
    
    if request.method == 'POST':
        assignment.delete()
        return redirect('assignments_list')

    return render(request, 'addlist/confirm_delete.html', {'assignment': assignment})

# Filter and sort upcoming assignments
@login_required
def approaching_duedates(request):
    today = timezone.localdate()
    next_week = today + timedelta(days=7)

    assignments = Assignment.objects.filter(
        user=request.user,  # 🔒 Show only assignments for the logged-in user
        due_date__range=(today, next_week)
    ).order_by('due_date')

    nearest_due_date = None
    if assignments.exists():
        nearest_due_date = assignments.first().due_date

    for assignment in assignments:
        delta = (assignment.due_date - today).days
        assignment.days_left = delta
        assignment.is_urgent = delta <= 2
        assignment.is_nearest = assignment.due_date == nearest_due_date

        percent_remaining = max(0, min(100, int((delta / 7) * 100)))
        assignment.progress_percent = 100 - percent_remaining

    return render(request, 'addlist/approaching_duedates.html', {
        'approaching_assignments': assignments,
        'today': today
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)       # don't save yet
            user.email = request.POST.get('email')  # set email manually
            user.save()                          # save user with email
            messages.success(request, "Account created successfully. You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'addlist/register.html', {'form': form})




def homepage(request):
    return render(request, 'addlist/homepage.html')

def about(request):
    return render(request, 'addlist/about.html')



class CustomLoginView(LoginView):
    def get_initial(self):
        # Return an empty initial dictionary to prevent form repopulation
        return {}

@require_GET
def custom_logout_view(request):
    logout(request)
    return redirect('login')  # or 'home'