from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView
from django.utils import timezone
from .models import Session, Attendance, Evaluation
from .forms import SessionForm, EvaluationForm

class SessionListView(ListView):
    model = Session
    template_name = 'training/session_list.html'
    context_object_name = 'sessions'
    ordering = ['-date']

class SessionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Session
    form_class = SessionForm
    template_name = 'training/session_form.html'
    
    def test_func(self):
        return self.request.user.user_type in ['admin', 'trainer']

class SessionDetailView(LoginRequiredMixin, DetailView):
    model = Session
    template_name = 'training/session_detail.html'
    context_object_name = 'session'

@login_required
def mark_attendance(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    attendance, created = Attendance.objects.get_or_create(
        session=session,
        participant=request.user,
        defaults={'is_present': True, 'check_in_time': timezone.now()}
    )
    return redirect('training:session_detail', pk=session_id)

@login_required
def submit_evaluation(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.session = session
            evaluation.participant = request.user
            evaluation.save()
            return redirect('training:session_detail', pk=session_id)
    else:
        form = EvaluationForm()
    return render(request, 'training/evaluation_form.html', {'form': form})