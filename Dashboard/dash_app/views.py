from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import os
from django.templatetags.static import static
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.

# display homepage

from .models import Doctor, Patient
from .operations.PatientManager import PatientManager
from .operations.details import Details


def homepage(request):
    details_obj = Details(request=request)
    details = details_obj.get_patient_doctor_details()
    return render(request, "dashboard.html", details)


def results(request):
    details_obj = Details(request=request)
    details = details_obj.get_patient_doctor_details()

    '''
    The bottom code is temporary.
    '''
    patients = details.get('patients')
    details['patient'] = patients[0] 
    ''''''
    return render(request, "results.html", details)


def profile(request):
    details_obj = Details(request=request)
    details = details_obj.get_patient_doctor_details()

    '''
    The bottom code is temporary.
    '''
    patients = details.get('patients')
    details['patient'] = patients[0]
    ''''''
    print("PATIENT ", details)
    return render(request, "profile.html", details)

@csrf_exempt
def signin(request):
    print("Signing in user get")
    if request.method == 'POST':
        if request.POST['password_input_type'] and request.POST['email_input_type']:
            try:
                user_email = request.POST['email_input_type']
                password = request.POST['password_input_type']
                print(user_email, password)
                user = User.objects.filter(email=user_email, password=password)
                if user:
                    print('Logging in user: ', user)
                    login(request, user)
                    return HttpResponseRedirect('homepage/dashboard/')
            except Exception as e:
                print("Error while logging ing a user: {}".format(e))
    return render(request, "sign-in.html")


@csrf_exempt
def signup(request):
    print('Signing up user GET')
    if request.method == 'POST':
        """
        Sign up a new user
        """
        if request.POST['password_input_type'] and request.POST['email_input_type'] and request.POST['name_input_type']:
            user_name = request.POST['name_input_type']
            user_email = request.POST['email_input_type']
            password = request.POST['password_input_type']
            try:
                user = User.objects.create_user(username=user_name, email=user_email, password=password)
                user.save()
                doctor = Doctor().create(name=user_name, email=user_email, phone_number=1234567899)
                doctor.save()
                login(request, user)
                return HttpResponseRedirect('homepage/dashboard/')
            except Exception as e:
                print("Error while signing up a user: {}".format(e))
    return render(request, "sign-up.html")


def addpatient(request):

    if request.method == 'POST':
        patient_manager_obj = PatientManager(patient_details=request.POST)
        required_patient_details = patient_manager_obj.all_required_fields_present()
        if required_patient_details:
            patient = Patient().create(
                *required_patient_details
            )
            patient.save()
            # return HttpResponseRedirect('homepage/dashboard/')
    return render(request, "addPatient.html")


import sys
sys.path.insert(1, 'dl/model')

#from backend_brain_pipeline import process_pipeline

class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name
from pet import output
def predict(request):
    context={'a':1}
    #print(request)
    #print(request.POST.dict)
    paths = []
    
    fs = OverwriteStorage()
 
    fileObj = request.FILES['filelocation1']
    filePathName1 = fs.save(fileObj.name, fileObj)
    filePathName1 = fs.url(fileObj.name)
    paths.append("."+filePathName1)

    print(output())
    # fileObj = request.FILES['filelocation2']
    # filePathName2 = fs.save(fileObj.name, fileObj)
    # filePathName2 = fs.url(fileObj.name)
    # paths.append("."+filePathName2)

    # fileObj = request.FILES['filelocation3']
    # filePathName3 = fs.save(fileObj.name, fileObj)
    # filePathName3 = fs.url(fileObj.name)
    # paths.append("."+filePathName3)

    # fileObj = request.FILES['filelocation4']
    # filePathName4 = fs.save(fileObj.name, fileObj)
    # filePathName4 = fs.url(fileObj.name)
    # paths.append("."+filePathName4)

    #process_pipeline(paths, fname='dash_app/static/assets/img/out.gif')
    return render(request, 'index.html', context)





def run(request):
    print("??")
    fs = OverwriteStorage()
    fileObj = request.FILES['petfilelocation']
    filePathName5 = fs.save(fileObj.name, fileObj)
    filePathName5 = fs.url(fileObj.name)
    print("Till here")
    print(filePathName5)
    path = 'Dashboard' + filePathName5
    content = {'a':output(path)}
    return render(request, 'index.html', content)



