from django.urls import path
from . import views

urlpatterns = [
    path('',  views.dashboard, name='dashboard'),
    path('calendar/',  views.calendar, name='calendar'),
    path('update_date_details/', views.update_date_details, name='update_date_details'),

    path('get_cycles/', views.get_cycles, name='get_cycles'),
    path('get_mood/', views.get_mood, name='get_mood'),
    path('get_intercourses/', views.get_intercourses, name='get_intercourses'),
    path('get_appointments/', views.get_appointments, name='get_appointments'),
    path('get_contacts/', views.get_contacts, name='get_contacts'),
    path('get_sleep/', views.get_sleep, name='get_sleep'),
    path('get_physical_activities/', views.get_physical_activities, name='get_physical_activities'),
    
    path('appointments/',  views.appointments, name='appointments'),
    path('save_appointment/', views.save_appointment, name='save_appointment'),
    path('cancel_appointment/', views.cancel_appointment, name='cancel_appointment'),
    path('update_appointment/', views.update_appointment, name='update_appointment'),
    path('delete_appointment/<int:appointment_id>', views.delete_appointment, name='delete_appointment'),

    path('intercourses/', views.intercourses, name='intercourses'),
    path('save_intercourse/', views.save_intercourse, name='save_intercourse'),
    path('update_intercourse/', views.update_intercourse, name='update_intercourse'),
    path('delete_intercourse/<int:intercourse_id>', views.delete_intercourse, name='delete_intercourse'),

    path('contacts/', views.contacts, name='contacts'),
    path('save_contact/', views.save_contact, name='save_contact'),
    path('update_contact/', views.update_contact, name='update_contact'),
    path('delete_contact/<int:contact_id>', views.delete_contact, name='delete_contact'),

    path('sleep/', views.sleep, name='sleep'),

    path('physical_activities/', views.physical_activities, name='physical_activities'),

    path('get_mood_data_for_chart/<int:year>', views.get_mood_data_for_chart, name='get_mood_data_for_chart'),
    path('get_period_data_for_chart/', views.get_period_data_for_chart, name='get_period_data_for_chart'),
    path('get_appointment_data_for_chart/', views.get_appointment_data_for_chart, name='get_appointment_data_for_chart'),

]

