from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView, ListView, View

from ..forms import AppForm
from ..models import Appointment, BloodDonation


class UserDashboard(View):

    def get(self, request, *args, **kwargs):
        blood_donations = BloodDonation.objects.filter(user=request.user)[:3]

        context = {
            'blood_donations': blood_donations,
        }

        return render(request, 'core/user/user_dashboard.html', context)

class UserProfile(TemplateView):
    template_name = 'core/user/user_profile.html'

class AppointmentListView(ListView):
    model = Appointment
    template_name = 'core/user/appointment_list.html'


def appointment(request):
    User = get_user_model()

    if request.method == 'POST':
        app_form = AppForm(request.POST)
        
        if app_form.is_valid():
            user = User.objects.get(id=request.user.id)
            donation_app = Appointment.objects.create(user=user, donate_date=app_form.cleaned_data.get('donate_date'))
            donation_app.save()

            return redirect('core:appointment_list')
    else:
        app_form = AppForm()
    
    context = {
        'app_form': app_form
    }
    return render(request, 'core/user/app_form.html', context)

def app_delete_view(request, id):
    item = Appointment.objects.get(id=id)
    item.delete()
    return redirect('core:appointment_list')


def donate_history(request):
    donate_history = BloodDonation.objects.filter(user=request.user)

    context = {
        'donate_history': donate_history,
    }
    return render(request, 'core/user/donate_history.html', context)

class LearnMoreView(TemplateView):
    template_name = 'core/user/learn_more.html'