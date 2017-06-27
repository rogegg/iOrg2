from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django.template.context import RequestContext

from user import forms


# Create your views here.
def index(request):
    return render_to_response('index.html', {})



def signup(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = forms.SignUpForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass

            # Process the data in form.cleaned_data
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]

            # At this point, user is a User object that has already been saved
            # to the database. You can continue to change its attributes
            # if you want to change other fields.
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name

            # Save new user attributes
            user.save()

            return HttpResponseRedirect(reverse('index'))  # Redirect after POST
    else:
        form = forms.SignUpForm()

    data = {
        'form': form,
    }
    return render(request, 'user/new_user.html', data)


@login_required()
def index(request):
    return render(request, 'index.html', {'user': request.user})

# @login_required()
# def logout_view(request):
#     # logout(request)
#     return HttpResponseRedirect('/datareader')
