from typing import Any
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, ListView

from authentication.decorators import email_not_verified
from authentication.models import SubscriptionSetup, UserPrograms
from dashboard.models import Circuit, Equipment, Exercise, Program, Workout


@method_decorator(login_required, name='dispatch')
@method_decorator(email_not_verified, name='dispatch')
class DashboardView(ListView):
    model = Program
    template_name = 'dashboard.html'
    context_object_name = 'programs'

    def get_queryset(self):

        return Program.objects.filter(published=True)

    def get_context_data(self, **kwargs):

        context = super(DashboardView, self).get_context_data(**kwargs)
        context['user_program'] = UserPrograms.objects.filter(active=True, user=self.request.user).all()
        context['workout'] = Workout.objects.all()
        return context


@method_decorator(login_required, name='dispatch')
class WorkoutDetailView(DetailView):
    model = Workout
    template_name = 'workout.html'

    def get_context_data(self, **kwargs):
        context = super(WorkoutDetailView, self).get_context_data(**kwargs)
        context['circuits'] = Circuit.objects.filter(workout=self.object).all()
        context['exercises'] = Exercise.objects.all()
        context['equipments'] = Equipment.objects.all()

        return context


class PricingView(ListView):
    template_name = "pricing.html"
    queryset = SubscriptionSetup.objects.order_by('amount')
    context_object_name = 'subscriptions'

    def get_context_data(self, **kwargs):
        context = super(PricingView, self).get_context_data(**kwargs)
        return context


# class ProgramDetails(View):
#     def get(self, request):
#         return render(request, 'programDetail.html')


class ProgramDetailsView(DetailView):
    model = Program
    template_name = 'programDetail.html'
    context_object_name = 'program'

    def get_context_data(self, **kwargs):

        context = super(ProgramDetailsView, self).get_context_data(**kwargs)
        context['workout'] = Workout.objects.all()

        return context
