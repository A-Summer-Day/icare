from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, UserUpdateForm, UserLoginForm
from django.contrib.auth import login, authenticate
from django.contrib import messages

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('myhealth:dashboard')
    else:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username = username, password = password)
                login(request, user)
                return redirect('myhealth:dashboard')
                #user_can_register = salesforce.user_can_register(email=email)
                # if(user_can_register['can_register']):
                #     user = form.save(commit=False)
                #     first_name = user_can_register['first_name']
                #     last_name = user_can_register['last_name']
                #     contact_id = user_can_register['contact_id']
                #     user.first_name = first_name
                #     user.last_name = last_name
                #     user.contact_id = contact_id
                #     if(user_can_register['record_type'] == 'Business Partner'):
                #         user.is_business_partner = True
                #     elif(user_can_register['record_type'] == 'Client profile for Household Account-based model'):
                #         user.is_client = True
                #     elif(user_can_register['record_type'] == 'Axess Law Staff Member'):
                #         user.is_employee = True
                #     else:
                #         pass
                #     user.save()

                #     # context = {

                #     # }

                #     # html_body = render_to_string('users/email_templates/register_success.html', context)

                #     # message =  EmailMultiAlternatives(
                #     #     subject = 'Client Portal Account Created!',
                #     #     body = "Email testing",
                #     #     from_email ='autoemail@axesslaw.com',
                #     #     to = [email]
                #     # )

                #     # message.attach_alternative(html_body, "text/html")
                #     # message.send(fail_silently=False)

                #     # context_2 = {
                #     #     'email_address': email
                #     # }

                #     # html_body_2 = render_to_string('users/email_templates/new_user_alert.html', context_2)
                #     # message_2 =  EmailMultiAlternatives(
                #     #     subject = 'New User Alert!',
                #     #     body = "Email testing",
                #     #     from_email ='autoemail@axesslaw.com',
                #     #     to = ['sle@axesslaw.com', 'smammadov@axesslaw.com']
                #     # )

                #     # message_2.attach_alternative(html_body_2, "text/html")
                #     # message_2.send(fail_silently=False)

                #     messages.success(
                #         request, f'Account successfuly created! Please log in!')
                #     return redirect('login')
                # else:
                #     messages.error(
                #         request, f'Email address does not exist in our Database!')
         
        else:
            form  = UserRegisterForm()
    
        return render(request, 'users/register.html', {
            'form': form
        })


def user_login(request):
    if request.user.is_authenticated:
        return redirect('myhealth:dashboard')
    else:
        if request.method == 'POST':
            form = UserLoginForm(request.POST)
            # username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password')
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('myhealth:dashboard')
                # has_portal_access = salesforce.user_has_portal_access(user.contact_id)
                # if(has_portal_access):
                #     login(request, user)
                #     return redirect('client_portal:dashboard')
                # else:
                #     messages.error(
                #         request, f'You do not have access to the client portal. Please <a href="mailto:happytohelp@axesslaw.com" class="text-white"><i class="ri-mail-add-fill fs-6 me-1" style="position: relative; top: 4px;"></i></a> or <a href="tel:+1-877-402-4207" class="text-white"><i class="ri-phone-fill fs-6 me-1" style="position: relative; top: 4px;"></i></a> us for help.')
            else:
                messages.error(
                        request, f'Please enter a correct username and password. Note that both fields may be case-sensitive.')
        else:
            form = UserLoginForm()

        return render(request, 'users/login.html', {
            'form': form
        })
