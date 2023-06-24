from django.shortcuts import redirect, render
from .models import Email_this
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.files.storage import FileSystemStorage
import random
import requests

def checking(request):
    id_ =  str(random.randint(1000000,999999999))
    print('Validating Mail Address...')
    url = "https://mailcheck.p.rapidapi.com/"

    for x in request.POST.get('too').split(','):
        querystring = {"domain":x}

        headers = {
            "X-RapidAPI-Key": "923a211b74msh68f1693f786b3ebp1492b4jsnf8576e78851c",
            "X-RapidAPI-Host": "mailcheck.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        if response.json()['valid'] == False:
            return render(request,"frontend.html",{"backendMessage":"1","errorMessage": x+" is invalid email address","action":"../check/check"})  
    print('Validation complete...')  
    if request.FILES.getlist('attach_file') == []:
        pass
    else:
        get_file = request.FILES.getlist('attach_file')
        print(get_file)
        for x in get_file:
            Email_this.objects.create(filee=x)
    print('Connenting to database...')
    check = Email_this()
    check.id = id_
    check.to  = request.POST.get('too')
    check.subject  = request.POST.get('subject')
    check.message = request.POST.get('message')
    if request.FILES.getlist('attach_file') == []:
        pass
    else:
        check.filee = get_file[0]
        print('Arranging File names...')
        for x in range(1,len(get_file)):
            check.filee = str(check.filee) + ',' + str(get_file[x])
    check.save()
    print('Saving data to database...')
    data = Email_this.objects.get(id = id_)
    data.to = data.to.split(',')
    print('Preparing to send mail...')
    mas = EmailMessage(
        data.subject,
        data.message,
        'dhairyaajwani2002@gmail.com',
        data.to,
        )
    if request.FILES.getlist('attach_file') == []:
        pass
    else:
        remove1 = str(data.filee).replace('(', '')
        remove2 = remove1.replace(')', '')
        change = remove2.replace(' ', '_')
        files = change.split(',')
        fs = FileSystemStorage()
        print('Attaching files...')
        for x in files:
            mas.attach_file(settings.MEDIA_ROOT+str(x))
            fs.delete(settings.MEDIA_ROOT+str(x))
    print('Sending email...')
    mas.send()
    delete = Email_this.objects.filter(to="not_null")
    delete.delete()
    print('Mail sent successfully')
    return render(request,"frontend.html",{"backendMessage":"0","action":"../check/check"})