import json
import math
import calendar as cl
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .models import Cycle, Mood, Appointment, Intercourse, Contact, Sleep, PhysicalActivity
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta
from django.db.models import Count, Q, CharField
from django.db.models.functions import TruncMonth, Cast
from celery import Celery
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from myhealth.tasks import send_email_task
from django.forms.models import model_to_dict


# Create your views here.


@login_required
def dashboard(request):
    context = {}
    return render(request, 'myhealth/index.html', context)


@login_required
def calendar(request):
    current_user = auth.get_user(request)
    cycles = Cycle.objects.filter(user_id=current_user.id)
    # json.dumps(list(cycles.values()))
    context = {
        'cycles': cycles
    }

    return render(request, 'myhealth/calendar.html', context)


@login_required
def get_cycles(request):
    current_user = auth.get_user(request)
    cycles = list(Cycle.objects.filter(user_id=current_user.id).values())

    return JsonResponse({'cycles': cycles})


@login_required
def get_mood(request):
    current_user = auth.get_user(request)
    # mood = list(Mood.objects.filter(user_id=current_user.id).values())
    mood = Mood.objects.filter(user_id=current_user.id)
    # mood = Mood.objects.filter(user_id=current_user.id).values()

    mood = list(mood.values())

    return JsonResponse({'mood': mood})


@login_required
def get_appointments(request):
    current_user = auth.get_user(request)
    appointments = list(Appointment.objects.filter(
        user_id=current_user.id).order_by('date').values())

    return JsonResponse({'appointments': appointments})


@login_required
def appointments(request):
    current_user = auth.get_user(request)
    appointments = Appointment.objects.filter(user_id=current_user.id)
    context = {
        'appointments': appointments
    }

    return render(request, 'myhealth/appointments.html', context)


@login_required
def save_appointment(request):
    if request.method == 'POST':
        current_user = auth.get_user(request)
        # print(dict(request.POST.items()))
        # print(list(request.POST.items()))
        new_appointment = Appointment.objects.create(date=request.POST['date'], doctor=request.POST['doctor'],
                                                     location=request.POST['location'], title=request.POST['title'], time=request.POST['time'], user=current_user)
        return JsonResponse({
            'success': True,
            'message': 'Appointment added.'
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Request method not allowed.'
        })


@login_required
def update_appointment(request):
    if request.method == 'POST':
        current_user = auth.get_user(request)
        # print(dict(request.POST.items()))
        # print(list(request.POST.items()))
        if request.POST['id']:
            appointmentFound = Appointment.objects.filter(
                id=request.POST['id']).first()
            if appointmentFound:
                appointmentFound.doctor = request.POST['doctor']
                appointmentFound.title = request.POST['title']
                appointmentFound.location = request.POST['location']
                appointmentFound.date = request.POST['date']
                # print(appointmentFound)
                appointmentFound.save()
            message = 'Appointment updated.'
        else:
            new_appointment = Appointment.objects.create(
                date=request.POST['date'], doctor=request.POST['doctor'], location=request.POST['location'], title=request.POST['title'], user=current_user)
            message = 'Appointment added.'

        return JsonResponse({
            'success': True,
            'message': message
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Request method not allowed.'
        })


@login_required
def cancel_appointment(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('id', None)
        cancel_reason = request.POST.get('cancel_reason', '')

        if appointment_id is not None:
            appointment = get_object_or_404(Appointment, pk=appointment_id)
            appointment.status = 'canceled'
            appointment.cancel_reason = cancel_reason
            appointment.save()

            response_data = {
                'success': True,
                'message': 'Appointment canceled successfully.',
            }
            return JsonResponse(response_data)

    response_data = {
        'success': False,
        'message': 'Request method not allowed.',
    }
    return JsonResponse(response_data)


@login_required
def update_date_details(request):
    if request.method == 'POST':
        current_user = auth.get_user(request)
        # print(dict(request.POST.items()))
        # print(list(request.POST.items()))
        date = request.POST['date']
        logPeriod = request.POST['logPeriod']
        moodToLog = request.POST['moodToLog']
        cycleFound = Cycle.objects.filter(date=date, user=current_user).first()
        moodFound = Mood.objects.filter(date=date, user=current_user).first()

        if logPeriod == 'true':
            if not cycleFound:
                Cycle.objects.create(date=date, user=current_user)

        elif logPeriod == 'false':
            if cycleFound:
                cycleFound.delete()

        if moodToLog:
            if not moodFound:
                Mood.objects.create(
                    date=date, user=current_user, mood=moodToLog)
            else:
                if moodToLog != moodFound.mood:
                    moodFound.mood = moodToLog
                    moodFound.save()

        elif not moodToLog:
            if moodFound:
                moodFound.delete()

        return JsonResponse({
            'success': True,
            'message': 'Date details updated.'
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Request method not allowed.'
        })


@login_required
def delete_appointment(request, appointment_id):
    if request.method == 'DELETE':
        appointment = Appointment.objects.filter(id=appointment_id).first()
        if appointment:
            appointment.delete()
        return JsonResponse({
            'success': True,
            'message': 'Appointment deleted.'
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Request method not allowed.'
        })


@login_required
def reminders(request):
    context = {}
    return render(request, 'myhealth/reminders.html', context)


@login_required
def identify_first_days_of_cycles(request, period_dates):
    first_days_of_cycles = [period_dates[0]]  # Initialize with the first date

    for i in range(1, len(period_dates)):
        current_date = datetime.strptime(period_dates[i], "%Y-%m-%d")
        previous_date = datetime.strptime(period_dates[i - 1], "%Y-%m-%d")

        # Check if the next date is right after the current date
        if current_date != previous_date + timedelta(days=1):
            # Found the first day of a new cycle
            first_days_of_cycles.append(period_dates[i])

    return first_days_of_cycles


@login_required
def calculate_average_cycle_length(request, period_dates):
    # if len(start_dates) < 2:
    #     print("Insufficient data to calculate average cycle length.")
    #     return None
    start_dates = identify_first_days_of_cycles(request, period_dates)
    cycle_lengths = []

    for i in range(1, len(start_dates)):
        current_date = datetime.strptime(start_dates[i], "%Y-%m-%d")
        previous_date = datetime.strptime(start_dates[i - 1], "%Y-%m-%d")
        cycle_length = (current_date - previous_date).days
        cycle_lengths.append(cycle_length)
    if not cycle_lengths:
        return 0
    else:
        average_cycle_length = sum(cycle_lengths) / len(cycle_lengths)
        return math.ceil(average_cycle_length)


@login_required
def calculate_average_period_duration(request, period_dates):

    # if len(period_dates) < 2:
    #     print("Insufficient data to calculate average period duration.")
    #     return None

    cycle_start_dates = [period_dates[0]]
    cycle_end_dates = []

    for i in range(1, len(period_dates)):
        current_date = datetime.strptime(period_dates[i], "%Y-%m-%d")
        previous_date = datetime.strptime(period_dates[i - 1], "%Y-%m-%d")

        # Check if the next date is right after the current date
        if current_date != previous_date + timedelta(days=1):
            # Found the first day of a new cycle
            cycle_start_dates.append(period_dates[i])
            # Previous date is the end date of the previous cycle
            cycle_end_dates.append(period_dates[i - 1])

    # Add the end date of the last cycle
    cycle_end_dates.append(period_dates[-1])
    print(cycle_start_dates)
    print(cycle_end_dates)

    period_durations = [(datetime.strptime(end, "%Y-%m-%d") - datetime.strptime(
        start, "%Y-%m-%d")).days + 1 for start, end in zip(cycle_start_dates, cycle_end_dates)]

    average_period_duration = sum(period_durations) / len(period_durations)
    return math.ceil(average_period_duration)


def calculate_average_period_length(request, period_dates):
    # if len(period_dates) < 2:
    #     print("Insufficient data to calculate average period length.")
    #     return None

    cycle_start_dates = [period_dates[0]]
    cycle_end_dates = []

    for i in range(1, len(period_dates)):
        current_date = datetime.strptime(period_dates[i], "%Y-%m-%d")
        previous_date = datetime.strptime(period_dates[i - 1], "%Y-%m-%d")

        # Check if the next date is right after the current date
        if current_date != previous_date + timedelta(days=1):
            # Found the first day of a new cycle
            cycle_start_dates.append(period_dates[i])
            # Previous date is the end date of the previous cycle
            cycle_end_dates.append(period_dates[i - 1])

    # Add the end date of the last cycle
    cycle_end_dates.append(period_dates[-1])
    print("Cycle Start Dates:", cycle_start_dates)
    print("Cycle End Dates:", cycle_end_dates)

    period_lengths = [(datetime.strptime(cycle_start_dates[i], "%Y-%m-%d") - datetime.strptime(
        cycle_end_dates[i-1], "%Y-%m-%d")).days for i in range(1, len(cycle_start_dates))]

    if not len(period_lengths):
        return 0
    else:
        average_period_length = sum(period_lengths) / len(period_lengths)
        return math.ceil(average_period_length)

# Extended Example usage
# period_dates = [
#     '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05',
#     '2023-02-01', '2023-02-02', '2023-02-03', '2023-02-04', '2023-02-05',
#     '2023-03-01', '2023-03-02', '2023-03-03', '2023-04-01',
#     '2023-04-02', '2023-04-03', '2023-04-04', '2023-04-05',
#     '2023-05-01', '2023-05-02', '2023-05-03', '2023-05-04', '2023-05-05'
# ]

# average_length = calculate_average_period_length(period_dates)

# if average_length is not None:
#     print(f"The average period length is approximately {average_length} days.")


@login_required
def get_mood_data_for_chart(request, year):
    today = datetime.now()
    if not year:
        year = today.year

    # year = today.year
    # month = today.month
    # day = today.day
    current_user = auth.get_user(request)
    result = Mood.objects.filter(user=current_user, date__year=year).annotate(month=TruncMonth('date'),).values('month').annotate(total_entries=Count(
        'id'), total_happy=Count('id', filter=Q(mood='HAPPY')), total_sad=Count('id', filter=Q(mood='SAD')), total_neutral=Count('id', filter=Q(mood='NEUTRAL')))

    result = list(result)
    happy = {
        'name': 'Happy',
        'data': []
    }
    sad = {
        'name': 'Sad',
        'data': []
    }
    neutral = {
        'name': 'Neutral',
        'data': []
    }

    categories = []

    happytest = {
        'name': 'Happy',
        'data': [0] * 12
    }
    sadtest = {
        'name': 'Sad',
        'data': [0] * 12
    }
    neutraltest = {
        'name': 'Neutral',
        'data': [0] * 12
    }
    test = []
    for i in range(1, 13):
        test.append(cl.month_name[i])
    for el in result:
        index = el['month']
        index = index.month - 1

        happytest['data'][index] = el['total_happy']
        sadtest['data'][index] = el['total_sad']
        neutraltest['data'][index] = el['total_neutral']

    for el in result:
        categories.append(el['month'].strftime("%B"))
        happy['data'].append(el['total_happy'])
        sad['data'].append(el['total_sad'])
        neutral['data'].append(el['total_neutral'])

    series = [happy, sad, neutral]
    seriestest = [happytest, sadtest, neutraltest]

    return JsonResponse({
        'success': True,
        'data': result,
        # 'categories': categories,
        # 'series': series
        'categories': test,
        'series': seriestest
    })


@login_required
def get_period_data_for_chart(request):
    current_user = auth.get_user(request)
    cast_expr = Cast('date', output_field=CharField())
    test = list(Cycle.objects.filter(user_id=current_user.id).annotate(
        dt_as_str=cast_expr).values_list('dt_as_str', flat=True))
    cycles = list(Cycle.objects.filter(
        user_id=current_user.id).values_list('date', flat=True))
    period_dates = []

    average_period_duration = calculate_average_period_duration(request, test)
    average_cycle_length = calculate_average_cycle_length(request, test)
    average_period_length = calculate_average_period_length(request, test)

    return JsonResponse({
        'success': True,
        'average_period_duration': average_period_duration,
        'average_cycle_length': average_cycle_length,
        'average_period_length': average_period_length
    })


@login_required
def get_appointment_data_for_chart(request):
    current_user = auth.get_user(request)
    today = datetime.today()
    # appointments = Appointment.objects.filter(user_id = current_user.id, date__gte = today).order_by('-date')[:5]
    # appointments = Appointment.objects.filter(user_id = current_user.id, date__gte = today).order_by('date')[:5]
    # appointments = Appointment.objects.filter(
    #     Q(time__isnull=False, user=current_user, date__gte=today, time__gte=datetime.now()) | Q(time__isnull=True, user=current_user, date__gte=today)).order_by('date')[:5]
    appointments = Appointment.objects.filter(
        Q(date__gt=today, user=current_user) |
        Q(date=today, time__gte=datetime.now(), user=current_user)
    ).order_by('date', 'time')[:5]
    # appointments = reversed(appointments)
    appointments = list(appointments.values())

    # pk = primary key
    stats = Appointment.objects.aggregate(total_personal=Count('pk', filter=Q(type='PERSONAL', user=current_user)), total_medical=Count(
        'pk', filter=Q(type='MEDICAL', user=current_user)), total_work=Count('pk', filter=Q(type='WORK', user=current_user)))

    print(appointments)

    return JsonResponse({
        'success': True,
        'appointments': appointments,
        'stats': stats
    })


@login_required
def fetch_appointments_for_today(request):
    today = datetime.now().date()
    current_user = auth.get_user(request)
    # Fetch appointments for the current day based on the 'date' field
    appointments = Appointment.objects.filter(
        date=today, user_id=current_user.id)

    # Convert queryset to a list of dictionaries for easy handling
    appointments_list = [
        {'email': current_user.email, 'date': appointment.date, 'time': appointment.time}
        for appointment in appointments
    ]

    return appointments_list


@login_required
def send_email(request):
    emails = ['norah137@gmail.com', 'norah137@yahoo.com']

    to_email = emails
    print('To emails:', to_email)
    context = {
        'message': 'From django'
    }

    html_body = render_to_string(
        'myhealth/email_templates/appointment.html', context)

    message = EmailMultiAlternatives(
        subject='Hello, SendGrid!',
        body="Email testing",
        from_email='ha.le.developer@protonmail.com',
        to=to_email
    )

    message.attach_alternative(html_body, "text/html")
    message.send(fail_silently=False)

    return JsonResponse({'success': True})


@login_required
def get_intercourses(request):
    current_user = auth.get_user(request)
    # intercourses = list(Intercourse.objects.filter(
    #     user_id=current_user.id).order_by('date').values())
    # print(intercourses)

    # return JsonResponse({'intercourses': intercourses})

    intercourses = list(
        Intercourse.objects.filter(user_id=current_user.id)
        .order_by('date')
        .select_related('with_whom')  # Include related Contact fields
        .values()
    )

    for intercourse in intercourses:
        if 'with_whom_id' in intercourse:
            contact_id = intercourse.pop('with_whom_id')  # Remove 'with_whom_id' key
            intercourse['with_whom'] = model_to_dict(
                Contact.objects.get(id=contact_id)
            )
    
    return JsonResponse({'intercourses': intercourses})


@login_required
def intercourses(request):
    current_user = auth.get_user(request)
    intercourse = Intercourse.objects.filter(user_id=current_user.id)
    

    context = {
        'intercourses': intercourses
    }

    return render(request, 'myhealth/intercourses.html', context)


@login_required
def save_intercourse(request):
    if request.method == 'POST':
        current_user = auth.get_user(request)

        with_whom_id = request.POST.get('with_whom')
        with_whom = Contact.objects.filter(id=with_whom_id).first()
        print(with_whom)

        new_intercourse = Intercourse.objects.create(
            date=request.POST['date'],
            notes=request.POST['notes'],
            protection_used=(request.POST['protection_used'] == 'true'),
            contraception_method=request.POST['contraception_method'],
            with_whom=with_whom,
            user=current_user
        )
        return JsonResponse({
            'success': True,
            'message': 'Intercourse added.'
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Request method not allowed.'
        })


@login_required
def delete_intercourse(request, intercourse_id):
    if request.method == 'DELETE':
        intercourse = Intercourse.objects.filter(id=intercourse_id).first()
        if intercourse:
            intercourse.delete()
        return JsonResponse({
            'success': True,
            'message': 'Intercourse deleted.'
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Request method not allowed.'
        })


@login_required
def update_intercourse(request):
    if request.method == 'POST':
        current_user = auth.get_user(request)
        with_whom_id = request.POST.get('with_whom')
        with_whom = Contact.objects.filter(id=with_whom_id).first()
        if request.POST['id']:
            intercourseFound = Intercourse.objects.filter(id=request.POST['id']).first()
            print(intercourseFound) 
            if intercourseFound:
                intercourseFound.notes = request.POST['notes']
                intercourseFound.protection_used = request.POST['protection_used'] == 'true'
                intercourseFound.contraception_method = request.POST['contraception_method']
                intercourseFound.date = request.POST['date']
                intercourseFound.with_whom = with_whom
                intercourseFound.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Intercourse updated.'
                })
        return JsonResponse({
                'success': False,
                'message': 'Record not found.'
            })    
            
    else:
        return JsonResponse({
            'success': False,
            'message': 'Request method not allowed.'
        })



@login_required
def contacts(request):
    current_user = auth.get_user(request)
    contacts = Contact.objects.filter(user_id=current_user.id)

    context = {
        'contacts': contacts
    }

    return render(request, 'myhealth/contacts.html', context)



@login_required
def get_contacts(request):
    current_user = auth.get_user(request)
    contacts = list(Contact.objects.filter(user_id=current_user.id).values())

    return JsonResponse({'contacts': contacts})


@login_required
def save_contact(request):
    if request.method == 'POST':
        current_user = auth.get_user(request)

        new_contact = Contact.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], notes=request.POST['notes'], email=request.POST['email'], phone_number=request.POST['phone_number'], address=request.POST['address'], user=current_user)
        return JsonResponse({
            'success': True,
            'message': 'Contact added.'
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Request method not allowed.'
        })


@login_required
def delete_contact(request, contact_id):
    if request.method == 'DELETE':
        contact = Contact.objects.filter(id=contact_id).first()
        if contact:
            contact.delete()
        return JsonResponse({
            'success': True,
            'message': 'Contact deleted.'
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Request method not allowed.'
        })


@login_required
def update_contact(request):
    if request.method == 'POST':
        current_user = auth.get_user(request)
        if request.POST['id']:
            contactFound = Contact.objects.filter(id=request.POST['id']).first()
            if contactFound:
                contactFound.first_name = request.POST['first_name'] 
                contactFound.last_name = request.POST['last_name']
                contactFound.email = request.POST['email']
                contactFound.phone_number = request.POST['phone_number']
                contactFound.address = request.POST['address']
                contactFound.notes = request.POST['notes']
                print(contactFound)
                contactFound.save()

                return JsonResponse({
                    'success': True,
                    'message': 'Contact updated.'
                })
        
        return JsonResponse({
            'success': False,
            'message': 'Record not found.'
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Request method not allowed.'
        })
    


@login_required
def sleep(request):
    current_user = auth.get_user(request)
    sleep = Sleep.objects.filter(user_id=current_user.id)
    

    context = {
        'sleep': sleep
    }

    return render(request, 'myhealth/sleep.html', context)


@login_required
def physical_activities(request):
    current_user = auth.get_user(request)
    physical_activities = PhysicalActivity.objects.filter(user_id=current_user.id)
    

    context = {
        'physical_activities': physical_activities
    }

    return render(request, 'myhealth/physical_activities.html', context)



@login_required
def get_sleep(request):
    current_user = auth.get_user(request)
    sleep = list(Sleep.objects.filter(user_id=current_user.id).order_by('date').values())

    return JsonResponse({'sleep': sleep})


@login_required
def get_physical_activities(request):
    current_user = auth.get_user(request)
    physical_activities = list(PhysicalActivity.objects.filter(user_id=current_user.id).values())

    return JsonResponse({'physical_activities': physical_activities})