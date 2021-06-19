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

from backend_brain_pipeline import process_pipeline
from pet import output
from ecg import prediction
from xray import xray_pred

class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name

def mripredict(request):
    context={}
    paths = []
#    fs = OverwriteStorage()
    print("*******************************")
    fs = OverwriteStorage()
    for count, x in enumerate(request.FILES.getlist("filelocation1")):
            def process(f):
                with open('/content/capstoneproj/Dashboard//media/file_' + str(count), 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
                        print("1") 
            process(x)
    # process_pipeline(paths, fname='dash_app/static/assets/img/mriout.gif')
    context['a'] = 'The Results for MRI Scans are'
    context['b'] = 'Coloured regions indicate abnormality'
    context['c'] = 'static/assets/img/out.gif'
    
    return render(request, 'index.html', context)


def petpredict(request):
    
    fs=FileSystemStorage()

    fileObj = request.FILES['filelocation5']
    filePathName5 = fs.save(fileObj.name, fileObj)
    filePathName5 = fs.url(fileObj.name)
    path = filePathName5
    print(filePathName5)
    
    print(path)

    a = output(path)
    context={}
    context['a'] = 'The Results for PET Scans are '
    if(a==0):
        context['b'] = 'Normal as per Ai'
        context['c'] = 'static/assets/img/normalpet.gif'
    else:
      context['b'] = 'AbNormal as per Ai'
      context['c'] = 'static/assets/img/abnormalpet.gif'
    
    path = '/content/capstoneproj/Dashboard/' + path
    context['c'] = path
    return render(request, 'index.html', context)


def xraypredict(request):

    fs=FileSystemStorage()

    fileObj = request.FILES['filelocation6']
    filePathName6 = fs.save(fileObj.name, fileObj)
    filePathName6 = fs.url(fileObj.name)
    path = filePathName6
    print(filePathName6)
    
    print(path)
    a = xray_pred(path)
    context={}
    context['a'] = 'The prediction for the XRay Image is '
    if(a==0):
      context['b'] = 'Normal Xray, no Pneumonia found by Ai'
    else:
      context['b'] = 'AbNormal Xray, Pneumonia found by Ai'
      
    path2 = '/content/capstoneproj/Dashboard/' + path
    context['c'] = path
    context['d'] = path2
    return render(request, 'index.html', context)


def ecgpredict(request):
    fs=FileSystemStorage()

    fileObj = request.FILES['filelocation7']
    filePathName7 = fs.save(fileObj.name, fileObj)
    filePathName7 = fs.url(fileObj.name)
    path = filePathName7
    print(filePathName7)
    
    print(path)
    a = prediction(path)
    context={}
    context['a'] = 'The Results for ECG are '
    if(a[0][0]==0):
      context['b'] = 'Non-ectopic Beats'
      context['c'] = 'static/assets/img/ecg0.jpg'
    elif(a[0][1]==0):
      context['b'] = 'Fusion Beats '
      context['c'] = 'static/assets/img/ecg1.jpg'
    elif(a[0][2]==0):
      context['b'] = 'AbNormal '
    elif(a[0][3]==0):
      context['b'] = 'AbNormal '
    elif(a[0][4]==0):
      context['b'] = 'AbNormal '    
    return render(request, 'index.html', context)






