from django.db import models
import re
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
import bcrypt


# Create your models here.
class PatientManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if len(postData['first_name']) == 0:
            errors['first_name'] = "First name is required"
        elif len(postData['first_name']) < 2 or postData['first_name'].isalpha() != True:
            errors['first_name'] = "First name must be at least 2 letters long, letters only"
        if len(postData['last_name']) == 0:
            errors['last_name'] = "Last name is required"
        elif len(postData['last_name']) < 2 or postData['last_name'].isalpha() != True:
            errors['first_name'] = "Last name must be at least 2 letters long, letters only"
        if len(postData['email']) == 0:
            errors['email'] = "Email is required"
        elif not email_regex.match(postData['email']):          
            errors['email'] = ("Invalid email format")
        existing_patient = Patient.objects.filter(email=postData['email'])
        if len(existing_patient) > 0:
            errors['email'] = "Email already in use"   
        if len(postData['password']) == 0:
            errors['password'] = "Password is required"
        elif len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        elif postData['password'] != postData['confirm_pw']:
            errors['password'] = "Password and Confirm Password inputs must match"
        return errors        

    def log_validator(self, postData):
        errors = {}
        if len(postData['email']) == 0:
            errors['email'] = "Email is required"
        elif not email_regex.match(postData['email']):          
            errors['email'] = ("Invalid email format")
        existing_patient = Patient.objects.filter(email=postData['email'])
        if len(existing_patient) != 1:
            errors['email'] = "Patient not found"    
        if len(postData['password']) == 0:
            errors['password'] = "Password is required"
        elif len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        elif bcrypt.checkpw(postData['password'].encode(), existing_patient[0].password.encode()) != True:
            errors['email'] = "Email and Password do not match"
        return errors

class TherapistManager(models.Manager):
    def reg_validator_therapist(self, postData):
        errors = {}
        if len(postData['title']) == 0:
            errors['title'] = " A title is required"
        elif len(postData['title']) < 2:
            errors['title'] = "Title must be at least 2 characters long"    
        if len(postData['first_name']) == 0:
            errors['first_name'] = "First name is required"
        elif len(postData['first_name']) < 2 or postData['first_name'].isalpha() != True:
            errors['first_name'] = "First name must be at least 2 letters long, letters only"
        if len(postData['last_name']) == 0:
            errors['last_name'] = "Last name is required"
        elif len(postData['last_name']) < 2 or postData['last_name'].isalpha() != True:
            errors['first_name'] = "Last name must be at least 2 letters long, letters only"
        if len(postData['email']) == 0:
            errors['email'] = "Email is required"
        elif not email_regex.match(postData['email']):          
            errors['email'] = ("Invalid email format")
        existing_therapist = Therapist.objects.filter(email=postData['email'])
        if len(existing_therapist) > 0:
            errors['email'] = "Email already in use"   
        if len(postData['password']) == 0:
            errors['password'] = "Password is required"
        elif len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        elif postData['password'] != postData['confirm_pw']:
            errors['password'] = "Password and Confirm Password inputs must match"
        return errors        

    def log_validator_therapist(self, postData):
        errors = {}
        if len(postData['email']) == 0:
            errors['email'] = "Email is required"
        elif not email_regex.match(postData['email']):          
            errors['email'] = ("Invalid email format")
        existing_therapist = Therapist.objects.filter(email=postData['email'])
        if len(existing_therapist) != 1:
            errors['email'] = "Therapist not found"    
        if len(postData['password']) == 0:
            errors['password'] = "Password is required"
        elif len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        elif bcrypt.checkpw(postData['password'].encode(), existing_therapist[0].password.encode()) != True:
            errors['email'] = "Email and Password do not match"
        return errors
    
class RecordManager(models.Manager):
    def thought_validator(self, postData):
        errors = {}
        if len(postData['situation']) == 0:
            errors['situation'] = "Situation cannot be left blank"
        if len(postData['emotion']) == 0:
            errors['emotion'] = "Emotion cannot be left blank"
        if len(postData['negative_thought']) == 0:
            errors['negative_thought'] = "Negative thought cannot be left blank"
        if len(postData['alternative_thought']) == 0:
            errors['alternative_thought'] = "Alternative thought cannot be left blank"
        if len(postData['action_taken']) == 0:
            errors['action_taken'] = "Action taken cannot be left blank"    
        return errors

class MessageManager(models.Manager):
    def mail_validator(self, postData):
        errors = {}
        if len(postData['subject']) == 0:
            errors['subject'] = "Subject cannot be left blank"
        if len(postData['message_content']) == 0:
            errors['message_content'] = "Message cannot be left blank"    
        return errors 

class Therapist(models.Model):
    title = models.CharField(max_length=60)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    practice_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TherapistManager()

class Patient(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    therapist = models.ForeignKey(Therapist, related_name='patients', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = PatientManager()

class Record(models.Model):
    situation = models.TextField(null = True)
    emotion = models.TextField(null = True)
    negative_thought = models.TextField(null = True)
    alternative_thought = models.TextField(null = True)
    action_taken = models.TextField(null = True)
    share_record = models.BooleanField(default=False)
    patient_with_record = models.ForeignKey(Patient, related_name='records', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = RecordManager()

class Message(models.Model):
    therapist = models.ForeignKey(Therapist, related_name="therapist_message", on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, related_name="patient_message", on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message_content = models.TextField(null = True)
    unread = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = MessageManager()
