from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from django.views.generic import View, TemplateView, ListView, CreateView, UpdateView

from accounts.forms import (
    UserForm, 
    UserProfileForm,
)

from ..models import (
    Appointment,
    Hospital,
    BloodRequest,
    BloodDonation,
    Stock,
    Withdraw,
)
from ..forms import (
    UserProfileEditForm, 
    UserEditForm, 
    BloodDonationForm, 
    StockForm,
)


User = get_user_model()

class StaffDashboard(View):
    def get(self, request, *args, **kwargs):
        appointments = Appointment.objects.all()[:3]
        hospitals = Hospital.objects.all()[:3]
        requests = BloodRequest.objects.all()[:3]
        donations = BloodDonation.objects.all()[:3]
        
        stock_type_count = {
            'A': Stock.objects.filter(blood_type='A-').count() + Stock.objects.filter(blood_type='A+').count(),
            'B': Stock.objects.filter(blood_type='B-').count() + Stock.objects.filter(blood_type='B+').count(),
            'AB': Stock.objects.filter(blood_type='AB-').count() + Stock.objects.filter(blood_type='AB+').count(),
            'O': Stock.objects.filter(blood_type='O-').count() + Stock.objects.filter(blood_type='O+').count()
        }

        context = {
            'appointments': appointments,
            'hospitals': hospitals,
            'requests': requests,
            'donations': donations,
            'stock_num': stock_type_count,
        }

        return render(request, 'core/staff/staff_dashboard.html', context)


def manage_donor(request):
    users = User.objects.filter(is_normalUser=True)
    # user_id = user.id + '00' + (str(int(100 + user.id)))

    context = {
        'users': users,
        # 'user_id': user_id,
    }
    
    return render(request, 'core/staff/manage_donor.html', context)

def create_donor(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.is_normalUser = True
            user.save()
            profile = User.objects.get(username=user.username)
            
            profile.userprofile.gender = profile_form.cleaned_data.get('gender')
            profile.userprofile.age = profile_form.cleaned_data.get('age')
            profile.userprofile.blood_group = profile_form.cleaned_data.get('blood_group')
            profile.userprofile.phone = profile_form.cleaned_data.get('phone')
            profile.userprofile.address = profile_form.cleaned_data.get('address')

            profile.userprofile.save()

            return redirect('core:manage_donor')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'core/staff/create_donor.html', context)

def remove_donor(request, id):
    donor = User.objects.get(id=id)
    donor.delete()
    return redirect('core:manage_donor')

def edit_donor(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        user_form = UserEditForm(instance=user, data=request.POST)
        userprofile_form = UserProfileEditForm(instance=user.userprofile, data=request.POST)

        if user_form.is_valid() and userprofile_form.is_valid():
            user_form.save()
            userprofile_form.save()

            return redirect('core:manage_donor')

    else:
        user_form = UserEditForm(instance=user)
        userprofile_form = UserProfileEditForm(instance=user.userprofile)

    context = {
        'user_form': user_form,
        'userprofile_form': userprofile_form,
    }
    return render(request, 'core/staff/edit_donor.html', context)

def donor_detail(request, id):
    donor = User.objects.get(id=id)
    blood_donations = BloodDonation.objects.filter(user=donor)

    context = {
        'donor': donor,
        'blood_donations': blood_donations,
    }

    return render(request, 'core/staff/donor_detail.html', context)

class BloodDonationList(ListView):
    model = BloodDonation
    template_name = 'core/staff/blood_donation_list.html'
    
def blood_donation(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        donation_form = BloodDonationForm(request.POST)
        stock_form = StockForm(request.POST)

        if donation_form.is_valid() and stock_form.is_valid():
            donation = donation_form.save(commit=False)
            donation.user = user
            stock = Stock.objects.create(
                # blood_type=stock_form.changed_data.get('blood_type'),
                # blood_volume=stock_form.cleaned_data.get('blood_volume'),
                expire_date=stock_form.cleaned_data.get('expire_date')
            )
            stock.blood_type = stock_form.cleaned_data.get('blood_type')
            stock.blood_volume = stock_form.cleaned_data.get('blood_volume')
            stock.expire_date = stock_form.cleaned_data.get('expire_date')
            stock.expire_status = False
            stock.save()

            donation.stock = stock

            donation.save()

            return redirect('core:blood_donation_list')

    else:
        donation_form = BloodDonationForm()
        stock_form = StockForm()
    
    context = {
        'donation_form': donation_form,
        'stock_form': stock_form,
    }

    return render(request, 'core/staff/blood_donation.html', context)

class PendingDonation(ListView):
    model = Appointment
    template_name = 'core/staff/pending_donations.html'

class HospitalList(ListView):
    model = Hospital
    template_name = 'core/staff/hospital_list.html'

def delete_hospital(request, id):
    hospital = Hospital.objects.get(id=id)
    hospital.delete()
    
    return redirect('core:hospital_list')

class HospitalCreateView(CreateView):
    model = Hospital
    fields = '__all__'
    template_name = 'core/staff/hospital_create.html'
    context_object_name = 'form'
    success_url = reverse_lazy('core:hospital_list')

def hospital_detail(request, id):
    hospital = Hospital.objects.get(id=id)
    requested_blood = BloodRequest.objects.filter(hospital=hospital)

    context = {
        'hospital': hospital,
        'requested_blood': requested_blood,
    }

    return render(request, 'core/staff/hospital_detail.html', context)

class HospitalUpdate(UpdateView):
    model = Hospital
    template_name = 'core/staff/edit_hospital.html'
    fields = '__all__'


def bloodrequest(request):
    # bloodrequests = BloodRequest.objects.all()
    pending_requests = BloodRequest.objects.filter(status='P')
    failed_requests = BloodRequest.objects.filter(status='F')

    context = {
        'pending_requests': pending_requests,
        'failed_requests': failed_requests,
    }

    return render(request, 'core/staff/bloodrequest_list.html', context)

def completed_request(request):
    completed_requests = BloodRequest.objects.filter(status='C')

    context = {
        'completed_requests': completed_requests,
    }
    return render(request, 'core/staff/completed_request.html', context)

class CreateRequest(CreateView):
    model = BloodRequest
    template_name = 'core/staff/create_request.html'
    fields = ['hospital', 'blood_type', 'stock', 'withdraw_date', 'request_amount']
    success_url = reverse_lazy('core:bloodrequest_list')

def bloodrequest_detail(request, id):
    bloodrequest = BloodRequest.objects.get(id=id)

    context = {
        'bloodrequest': bloodrequest,
    }

    return render(request, 'core/staff/bloodrequest_detail.html', context)

def delete_request(request, id):
    item = BloodRequest.objects.get(id=id)
    item.delete()
    return redirect('core:bloodrequest_list')

def confirm_withdraw(request, id):
    current_request = BloodRequest.objects.get(id=id)
    stock_count = Stock.objects.filter(blood_type=current_request.blood_type).count()

    if stock_count and stock_count > current_request.request_amount:
        stocks = Stock.objects.filter(
            blood_type=current_request.blood_type
            )[:current_request.request_amount]
    else:
        stocks = Stock.objects.filter(
            blood_type=current_request.blood_type
            )[:stock_count]
    
    for stock in stocks:
        withdrawal = Withdraw.objects.create(
            hospital=current_request.hospital,
            stock=stock,
            blood_request=current_request,
            blood_type=current_request.blood_type,
            withdraw_date=current_request.withdraw_date
        )
    withdrawal.save()
    current_request.status = 'C'
    current_request.save()

    return redirect('core:bloodrequest_list')

class StockList(ListView):
    model = Stock
    template_name = 'core/staff/stock_list.html'

def delete_stock(request, id):
    item = Stock.objects.get(id=id)
    item.delete()
    return redirect('core:stock_list')

def delete_pending_donation(request, id):
    item = Appointment.objects.get(id=id)
    item.delete()

    return redirect('core:pending_donations')