from django.contrib import admin
from .models import User
from myhealth.models import Cycle, Mood, Appointment, Intercourse, Contact, PhysicalActivity, Sleep

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_filter = ('username', 'email', 'first_name', 'last_name')
    list_display = ('username', 'email', 'first_name', 'last_name')


class CycleAdmin(admin.ModelAdmin):
    list_filter = ('date', 'user')
    list_display = ('date', 'user')
    ordering = ('-date',)


class MoodAdmin(admin.ModelAdmin):
    list_filter = ('date', 'user', 'mood')
    list_display = ('date', 'user', 'mood')
    ordering = ('-date',)


class AppointmentAdmin(admin.ModelAdmin):
    list_filter = ('date', 'user', 'title', 'type','location', 'doctor')
    list_display = ('date', 'user', 'title', 'type', 'location', 'doctor')
    ordering = ('-date',)


class IntercourseAdmin(admin.ModelAdmin):
    list_filter = ('date', 'user', 'notes', 'protection_used', 'contraception_method', 'with_whom')
    list_display = ('date', 'user', 'notes', 'protection_used', 'contraception_method', 'with_whom')
    ordering = ('-date',)



class ContactAdmin(admin.ModelAdmin):
    list_filter = ('first_name', 'last_name', 'email', 'phone_number', 'address', 'notes')
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'address', 'notes')



class PhysicalActivityAdmin(admin.ModelAdmin):
    list_filter = ('date', 'specific_activity', 'activity_type', 'duration_minutes', 'calories_burned', 'user', 'notes')
    list_display = ('date', 'specific_activity', 'activity_type', 'duration_minutes', 'calories_burned', 'user', 'notes')
    ordering = ('-date',)
    


class SleepAdmin(admin.ModelAdmin):
    list_filter = ('date', 'total_hours', 'quality', 'user', 'notes')
    list_display = ('date', 'total_hours', 'quality', 'user', 'notes')
    ordering = ('-date',)




admin.site.register(User, UserAdmin)
admin.site.register(Cycle, CycleAdmin)
admin.site.register(Mood, MoodAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Intercourse, IntercourseAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(PhysicalActivity, PhysicalActivityAdmin)
admin.site.register(Sleep, SleepAdmin)

# from django.contrib.auth import get_user_model
# User = get_user_model()
# user = User.objects.get(username=<superuser's username>) #or email=<email>
# user.first_name = 'first_name'
# user.last_name = 'last_name'
# user.username = 'username' #make sure it is unique
# user.save()
