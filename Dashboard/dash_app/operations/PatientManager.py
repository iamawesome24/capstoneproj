from django.http import QueryDict


class PatientManager(object):
    def __init__(self, patient_details):
        self.patient_details = patient_details

    def all_required_fields_present(self):
        required_patient_details = {}
        if self.patient_details['name'] and self.patient_details['gender'] and self.patient_details['date_of_birth'] and \
           self.patient_details['email'] and self.patient_details['phone_number'] and self.patient_details['birth_place'] \
                and self.patient_details['country']:
            required_patient_details = dict(self.patient_details.lists())
            required_patient_details.pop('csrfmiddlewaretoken')
            return required_patient_details
        return required_patient_details