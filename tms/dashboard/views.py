# dashboard/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Avg, Q
from training.models import Session, Attendance, Evaluation
from django.db.models.functions import ExtractMonth
from accounts.models import CustomUser
from django.utils import timezone

# Permission checks
def is_admin(user):
    return user.user_type == 'admin'

def is_trainer(user):
    return user.user_type == 'trainer'

def is_participant(user):
    return user.user_type == 'participant'

# Existing admin_dashboard view...

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Overall system statistics
    total_users = CustomUser.objects.count()
    total_trainers = CustomUser.objects.filter(user_type='trainer').count()
    total_participants = CustomUser.objects.filter(user_type='participant').count()
    total_sessions = Session.objects.count()

    # Recent sessions
    recent_sessions = Session.objects.select_related('trainer').order_by('-date')[:5]
    
    # Upcoming sessions
    upcoming_sessions = Session.objects.select_related('trainer').filter(
        date__gte=timezone.now()
    ).order_by('date')[:5]

    # Sessions by month
    sessions_by_month = (
        Session.objects
        .annotate(month=ExtractMonth('date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    # Average ratings
    avg_ratings = Evaluation.objects.aggregate(
        avg_content=Avg('content_rating'),
        avg_trainer=Avg('trainer_rating')
    )

    # Attendance statistics
    total_attendance = Attendance.objects.filter(is_present=True).count()
    attendance_rate = (
        (total_attendance / (total_participants * total_sessions) * 100)
        if total_participants and total_sessions 
        else 0
    )

    # Top rated trainers
    top_trainers = (
        CustomUser.objects.filter(user_type='trainer')
        .annotate(
            avg_rating=Avg('session__evaluation__trainer_rating'),
            session_count=Count('session')
        )
        .filter(session_count__gt=0)
        .order_by('-avg_rating')[:5]
    )

    context = {
        'total_users': total_users,
        'total_trainers': total_trainers,
        'total_participants': total_participants,
        'total_sessions': total_sessions,
        'recent_sessions': recent_sessions,
        'upcoming_sessions': upcoming_sessions,
        'sessions_by_month': sessions_by_month,
        'avg_ratings': avg_ratings,
        'attendance_rate': attendance_rate,
        'top_trainers': top_trainers,
    }

    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
@user_passes_test(is_trainer)
def trainer_dashboard(request):
    # Get trainer's sessions
    trainer_sessions = Session.objects.filter(trainer=request.user)
    
    # Recent and upcoming sessions
    recent_sessions = trainer_sessions.filter(date__lt=timezone.now()).order_by('-date')[:5]
    upcoming_sessions = trainer_sessions.filter(date__gte=timezone.now()).order_by('date')[:5]
    
    # Session statistics
    total_sessions = trainer_sessions.count()
    # Fix: Use attendance_records instead of participants
    total_participants = sum(
        session.attendance_records.count() 
        for session in trainer_sessions
    )
    
    # Average ratings for trainer
    trainer_ratings = Evaluation.objects.filter(session__trainer=request.user).aggregate(
        avg_content=Avg('content_rating'),
        avg_trainer=Avg('trainer_rating')
    )
    
    # Attendance statistics
    attendance_stats = Attendance.objects.filter(
        session__trainer=request.user,
        is_present=True
    ).count()

    context = {
        'total_sessions': total_sessions,
        'total_participants': total_participants,
        'recent_sessions': recent_sessions,
        'upcoming_sessions': upcoming_sessions,
        'trainer_ratings': trainer_ratings,
        'attendance_stats': attendance_stats,
    }
    
    return render(request, 'dashboard/trainer_dashboard.html', context)

@login_required
@user_passes_test(is_participant)
def participant_dashboard(request):
    # Get participant's enrolled sessions through attendance records
    enrolled_sessions = Session.objects.filter(
        attendances__participant=request.user  # Changed from attendance_records to attendances
    ).distinct()
    
    # Upcoming sessions
    upcoming_sessions = enrolled_sessions.filter(
        date__gte=timezone.now()
    ).order_by('date')[:5]
    
    # Completed sessions
    completed_sessions = enrolled_sessions.filter(
        date__lt=timezone.now()
    ).order_by('-date')
    
    # Attendance statistics
    attendance_stats = Attendance.objects.filter(
        participant=request.user,
        is_present=True
    ).count()
    
    # Session progress
    total_enrolled = enrolled_sessions.count()
    completed_count = completed_sessions.count()
    completion_rate = (completed_count / total_enrolled * 100) if total_enrolled > 0 else 0
    
    # Recent evaluations
    recent_evaluations = Evaluation.objects.filter(
        participant=request.user
    ).order_by('-created_at')[:5]
    
    context = {
        'upcoming_sessions': upcoming_sessions,
        'completed_sessions': completed_sessions,
        'attendance_stats': attendance_stats,
        'total_enrolled': total_enrolled,
        'completion_rate': completion_rate,
        'recent_evaluations': recent_evaluations,
    }
    
    return render(request, 'dashboard/participant_dashboard.html', context)