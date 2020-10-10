from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q, Count
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    request.session.flush()
    return render(request, 'index.html')

def patient_register(request):
    if request.method =='POST':
        errors = Patient.objects.reg_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/new_patient')
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_patient = Patient.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], therapist=Therapist.objects.get(id=int(request.POST['therapist'])), email=request.POST['email'], password=hashed_pw)
        request.session['patient_id'] = new_patient.id
        return redirect('/patient_dashboard')
    return redirect('/')

def new_patient(request):
    context = {
        'all_therapists': Therapist.objects.all()
    }
    return render(request, 'new_patient.html', context)    

def login(request):
    return render(request, 'login.html')

def patient_login(request):
    if request.method == 'POST':
        errors = Patient.objects.log_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/login')
        this_patient = Patient.objects.get(email=request.POST['email'])
        request.session['patient_id'] = this_patient.id
        return redirect('/patient_dashboard')        
    return redirect('/')

def therapist_register(request):
    if request.method =='POST':
        errors = Therapist.objects.reg_validator_therapist(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/new_therapist')
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_therapist = Therapist.objects.create(title=request.POST['title'],first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashed_pw)
        request.session['therapist_id'] = new_therapist.id
        return redirect('/therapist_dashboard')
    return redirect('/')

def new_therapist(request):
    return render(request, 'new_therapist.html')

def therapist_login(request):
    if request.method == 'POST':
        errors = Therapist.objects.log_validator_therapist(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/login')
        this_therapist = Therapist.objects.get(email=request.POST['email'])
        request.session['therapist_id'] = this_therapist.id
        return redirect('/therapist_dashboard')        
    return redirect('/')

def patient_dashboard(request):
    if 'patient_id' not in request.session:
        return redirect('/')
    this_patient = Patient.objects.filter(id=request.session['patient_id'])    
    context = {
        'Patient': this_patient[0],
        'Record': this_patient[0].records.all(),
    }
    return render(request, 'patient_dashboard.html', context)

def therapist_dashboard(request):
    if 'therapist_id' not in request.session:
        return redirect('/')
    this_therapist = Therapist.objects.filter(id=request.session['therapist_id'])
    num_shared={}
    for patient in this_therapist[0].patients.all(): 
        num_shared[patient.id] = patient.records.filter(share_record=True).count()           
    context = {
        'Therapist': Therapist.objects.get(id=request.session['therapist_id']),
        'therapist_patients': this_therapist[0].patients.all(),
        'num_shared': num_shared
    }
    return render(request, 'therapist_dashboard.html', context)            

def logout(request):
    if request.method == 'POST':
        logout(request)
    return redirect('/') 

def add_a_record(request):
    if 'patient_id' not in request.session:
        return redirect('/')
    context = {
        'patient': Patient.objects.get(id=request.session['patient_id'])
    }
    return render(request, 'add_a_record.html', context)

def create(request):
    if request.method == 'POST':
        errors = Record.objects.thought_validator(request.POST)
        if len(errors) != 0:
            for (key, value) in errors.items():
                messages.error(request, value)
            return redirect('/add_a_record')

        Record.objects.create(
            situation = request.POST['situation'],
            emotion = request.POST['emotion'],
            negative_thought = request.POST['negative_thought'],
            alternative_thought = request.POST['alternative_thought'],
            action_taken = request.POST['action_taken'],
            patient_with_record = Patient.objects.get(id=request.session['patient_id'])
        )
    return redirect('/patient_dashboard')

def edit(request, Record_id):
    one_record = Record.objects.get(id=Record_id)
    context = {
        'patient': Patient.objects.get(id=request.session['patient_id']),
        'record': one_record
    }
    return render(request, 'edit.html', context)

def update(request, Record_id):
    to_update = Record.objects.get(id=Record_id)
    to_update.situation = request.POST['situation']
    to_update.emotion = request.POST['emotion']
    to_update.negative_thought = request.POST['negative_thought']
    to_update.alternative_thought = request.POST['alternative_thought']
    to_update.action_taken = request.POST['action_taken']
    to_update.save()
    return redirect('/patient_dashboard')

def cancel(request, Record_id):
    to_cancel = Record.objects.get(id=Record_id)
    to_cancel.delete()
    return redirect('/patient_dashboard')

def view(request, patient_id):
    if 'therapist_id' not in request.session:
        return redirect('/')
    context = {
        'records': Record.objects.filter(patient_with_record__id=patient_id, share_record=True)
    }   
    return render(request, 'view.html', context)    

def share_record(request, Record_id):
    share_record = Record.objects.get(id=Record_id)
    if share_record.share_record == False:   
        share_record.share_record=True
        share_record.save()
    return redirect('/patient_dashboard')

def therapist_add_message(request):
    if 'therapist_id' not in request.session:
        return redirect('/')
    if request.method == 'POST':
        errors = Message.objects.mail_validator(request.POST)
        if len(errors) != 0:
            for (key, value) in errors.items():
                messages.error(request, value)
            return redirect('/therapist_new_message')    
        Message.objects.create(
            therapist = Therapist.objects.get(id=request.session['therapist_id']),
            patient = Patient.objects.get(id=int(request.POST['patient'])),
            subject = request.POST['subject'],
            message_content = request.POST['message_content'],  
        ) 
    return redirect('/therapist_mailbox')       


def therapist_new_message (request):
    if 'therapist_id' not in request.session:
        return redirect('/')
    this_therapist = Therapist.objects.filter(id=request.session['therapist_id'])
    context = {
        'therapist_patients': this_therapist[0].patients.all(),
    } 
    return render(request, 'therapist_new_message.html', context)

def patient_add_message(request):
    if 'patient_id' not in request.session:
        return redirect('/')
    if request.method == 'POST':
        errors = Message.objects.mail_validator(request.POST)
        if len(errors) != 0:
            for (key, value) in errors.items():
                messages.error(request, value)
            return redirect('/patient_new_message')    
        Message.objects.create(
            therapist = Therapist.objects.get(id=int(request.POST['therapist'])),
            patient = Patient.objects.get(id=request.session['patient_id']),
            subject = request.POST['subject'],
            message_content = request.POST['message_content'],  
        ) 
    return redirect('/patient_mailbox')       


def patient_new_message (request):
    if 'patient_id' not in request.session:
        return redirect('/')  
    context = {
        "this_patient":Patient.objects.all()
    } 
    return render(request, 'patient_new_message.html', context)    

def our_mission(request):
    return render(request, 'our_mission.html')

def patient_mailbox(request):
    if 'patient_id' not in request.session:
        return redirect('/')
    context = {
        'patient': Patient.objects.get(id=request.session['patient_id'])
    }    
    return render(request, 'patient_mailbox.html', context)

def therapist_mailbox(request):
    if 'therapist_id' not in request.session:
        return redirect('/')
    context = {
        'Therapist': Therapist.objects.get(id=request.session['therapist_id']),
    }    
    return render(request, 'therapist_mailbox.html', context)

def patient_delete(request, msg_id):
    to_delete = Message.objects.get(id=msg_id)
    to_delete.delete()
    return redirect('/patient_mailbox')

def contact(request):
    return render(request, 'contact.html')
