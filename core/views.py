from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile

# Register View
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        role = request.POST['role']
        company = request.POST.get('company', '')

        # Create User
        user = User.objects.create_user(username=username, password=password, email=email)

        # Ensure UserProfile is created automatically (via signal or manually here)
        if not hasattr(user, 'userprofile'):
            UserProfile.objects.create(user=user)

        profile = user.userprofile
        profile.role = role
        profile.phone = phone
        if role == 'recruiter':
            profile.company = company
        profile.save()

        login(request, user)
        return redirect('dashboard')

    return render(request, 'core/register.html')

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Dashboard View
@login_required
def dashboard_view(request):
    profile = request.user.userprofile
    return render(request, 'core/dashboard.html', {'profile': profile})

def home_view(request):
    return render(request, 'core/home.html')



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Resume, Job
from utils.pdf_parser import extract_pdf_content
from utils.resume_improvements import suggest_improvements
from utils.job_matching import match_resume_to_job

@login_required
def upload_resume_view(request):
    """Handle resume upload, parsing, suggestions, and job recommendations."""
    current_resume = Resume.objects.filter(user=request.user).first()

    if request.method == 'POST':
        # Handle the action (upload or delete)
        action = request.POST.get('action')

        if action == 'delete':
            if current_resume:
                current_resume.delete()
                messages.success(request, "Resume deleted successfully.")
            return redirect('upload_resume')  # Stay on the upload page after delete

        elif action == 'upload':
            # Handle resume upload
            file = request.FILES.get('resume')

            if not file:
                messages.error(request, "Please upload a resume.")
            elif not file.name.endswith('.pdf'):
                messages.error(request, "Only PDF files are allowed.")
            else:
                # If there’s an existing resume, delete the old one
                if current_resume:
                    current_resume.delete()

                # Save the new resume entry
                new_resume = Resume.objects.create(user=request.user, file=file)

                # Extract text from the newly uploaded resume
                resume_text = extract_pdf_content(new_resume.file.path)

                # Generate improvement suggestions based on parsed resume
                suggestions = suggest_improvements(resume_text)

                # Fetch job descriptions from the database
                job_descriptions = Job.objects.values_list('description', flat=True)

                # If no job descriptions are found, display a message
                if not job_descriptions:
                    messages.error(request, "No job descriptions available for recommendations.")

                # Ensure there are job descriptions before proceeding
                if job_descriptions:
                    # Get job recommendations based on the resume content
                    similarity_scores = match_resume_to_job(resume_text, job_descriptions)

                    # Sort jobs by similarity score
                    recommended_jobs = sorted(zip(Job.objects.all(), similarity_scores), key=lambda x: x[1], reverse=True)

                    return render(request, 'core/upload_resume.html', {
                        'resume': new_resume,
                        'suggestions': suggestions,
                        'recommended_jobs': recommended_jobs[:5],  # Top 5 recommendations
                    })
                else:
                    return render(request, 'core/upload_resume.html', {
                        'resume': new_resume,
                        'suggestions': suggestions,
                    })

    return render(request, 'core/upload_resume.html', {'resume': current_resume})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm  # You need to create this form

@login_required
def update_profile(request):
    profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')  # Redirect to profile view after update
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'core/update_profile.html', {'form': form})
