from dash_app.models import Patient


class Details(object):
    def __init__(self, request):
        self.request = request

    def get_patient_doctor_details(self):
        patients = Patient.objects.all().order_by('-last_interaction')
        user_name = self.request.user
        details = {'username': user_name, 'patients': patients}
        return details