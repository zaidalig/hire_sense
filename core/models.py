from django.db import models
from django.contrib.auth.models import User

# Extended user profile with role support
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('job_seeker', 'Job Seeker'),
        ('recruiter', 'Recruiter'),
        ('admin', 'Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=200, blank=True)  # For recruiters
    address = models.TextField(blank=True, null=True)  # Add this line for address field

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# Job post model
class Job(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('pending', 'Pending Approval'),
        ('suspended', 'Suspended'),
        ('closed', 'Closed'),
        ('saved', 'Saved'),
    ]

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    salary = models.CharField(max_length=100, blank=True)
    skills_required = models.TextField(help_text="Comma-separated skills")
    experience_required = models.IntegerField(default=0)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company}"


# Resume model for uploads and AI parsing
class Resume(models.Model):
    RESUME_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('flagged', 'Flagged'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    parsed_skills = models.TextField(blank=True)
    parsed_education = models.TextField(blank=True)
    parsed_experience = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=RESUME_STATUS, default='pending')

    def __str__(self):
        return f"Resume of {self.user.username}"


# Job application by job seekers
class Application(models.Model):
    APP_STATUS = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
        ('withdrawn', 'Withdrawn'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(default=0.0)  # AI matching score
    status = models.CharField(max_length=20, choices=APP_STATUS, default='submitted')

    def __str__(self):
        return f"{self.applicant.username} applied to {self.job.title}"
