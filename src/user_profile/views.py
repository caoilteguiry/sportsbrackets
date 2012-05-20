from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from forms import UserRegistrationForm, MyProfileForm
from django.conf import settings
from django.core.mail import EmailMessage
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

import logging
logger = logging.getLogger("debugger")

def register(request):
    """This view handles user registration."""
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        user = User.objects.create_user(username=form.cleaned_data["username"],
                                        email=form.cleaned_data["email"],
                                        password=form.cleaned_data["password1"],
                                        )
        user.first_name = form.cleaned_data["first_name"]
        user.last_name = form.cleaned_data["last_name"]
        user.save()
        # XXX: email i18n?!
        email_subject = "Registration for %s" % settings.SITE_NAME
        email_body = ("A new user has registered for %s.\n"
                      "username: %s\n"
                      "email: %s\n"
                      "first_name: %s\n"
                      "last_name: %s\n" % \
                      (settings.SITE_NAME, form.cleaned_data["username"], form.cleaned_data["email"],
                       form.cleaned_data["first_name"], form.cleaned_data["last_name"]))
        email_message = EmailMessage(subject=email_subject, body=email_body, from_email=settings.WEB_EMAIL, 
                                     to=[admin[1] for admin in settings.ADMINS], 
                                     headers={"Reply-To":settings.NOREPLY_EMAIL})
        email_message.send()
        return redirect("/register_success")
    
    c = {"form":form}
    c.update(csrf(request))
    c.update(locals())
    return render_to_response("register.html", c, context_instance=RequestContext(request))

def register_success(request):
    """Simple view to tell the user that their registration was successful."""
    return render_to_response("register_success.html", locals(), context_instance=RequestContext(request))


def login(request):
    """Login view."""
    return render_to_response("login.html", locals(), context_instance=RequestContext(request))

@login_required
def my_profile(request):
    """View to allow user to view and edit their profile."""
    user = request.user
    form = MyProfileForm(request.POST or None, 
                         initial={"share_predictions":user.get_profile().share_predictions})
    if form.is_valid():
        profile = request.user.get_profile()
        profile.share_predictions = form.cleaned_data["share_predictions"]
        profile.save()
    c = {"form":form}
    c.update(csrf(request))
    c.update(locals())    
    
    
    return render_to_response("my_profile.html", c, context_instance=RequestContext(request))
