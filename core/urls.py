from django.urls import path

from .views import base, user, staff
# from accounts import views as acv

app_name = 'core'

urlpatterns = [
    path('', base.HomePageView.as_view(), name='index'),
    
    # User urls
    path('dashboard/', user.UserDashboard.as_view(), name='user_dashboard'),
    path('profile/', user.UserProfile.as_view(), name='user_profile'),
    path('create-appointment/', user.appointment, name='appointment'),
    path('appointments/', user.AppointmentListView.as_view(), name='appointment_list'),
    path('delete/<int:id>/', user.app_delete_view, name='delete_appointment'),
    path('donate-history/', user.donate_history, name='donate_history'),
    path('learn-more/', user.LearnMoreView.as_view(), name='learn_more'),


    #Staff
    path('staff-dashboard/', staff.StaffDashboard.as_view(), name='staff_dashboard'),
    path('manage-donor/', staff.manage_donor, name='manage_donor'),
    path('create-donor/', staff.create_donor, name='create_donor'),
    path('delete-donor/<int:id>/', staff.remove_donor, name='delete_donor'),
    path('edit_donor/<int:id>/', staff.edit_donor, name='edit_donor'),
    path('donor-detail/<int:id>/', staff.donor_detail, name='donor_detail'),
    path('blood-donations/', staff.BloodDonationList.as_view(), name='blood_donation_list'),
    path('create-donation/<int:id>/', staff.blood_donation, name='create_donation'),
    path('pending-donations/', staff.PendingDonation.as_view(), name='pending_donations'),
    path('hospital-list/', staff.HospitalList.as_view(), name='hospital_list'),
    path('delete-hospital/<int:id>/', staff.delete_hospital, name='delete_hospital'),
    path('add-hospital/', staff.HospitalCreateView.as_view(), name='hospital_create'),
    path('hospital-detail/<int:id>/', staff.hospital_detail, name='hospital_detail'),
    path('edit-hospital/<int:pk>/', staff.HospitalUpdate.as_view(), name='hospital_edit'),
    path('blood-requests/', staff.bloodrequest, name='bloodrequest_list'),
    path('completed-request/', staff.completed_request, name='completed_request'),
    path('create_request/', staff.CreateRequest.as_view(), name='create_request'),
    path('delete_request/<int:id>/', staff.delete_request, name='delete_request'),
    path('blood-request/detail/<int:id>/', staff.bloodrequest_detail, name='bloodrequest_detail'),
    path('withdraw/<int:id>/', staff.confirm_withdraw, name='withdraw'),
    path('stock/', staff.StockList.as_view(), name='stock_list'),
    path('delete-stock/<id>', staff.delete_stock, name='delete_stock'),
    path('delete-pending-donation/<id>/', staff.delete_pending_donation, name='delete_pending_donation'),

]
