from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import render

def load_frontend(request):
    return render(request,'frontend.html',{"action":"check/check"})

def send_maile(request):
    try:
        file_send = request.FILES.get('fi')
        print(file_send)
        mas = EmailMessage(
        'THIS IS MESSAGE FROM DJANGO',
        'THIS MESSAGE IS SEND BY DJANGO',
        'dhairyaajwani2002@gmail.com',
        ['postviral75@gmail.com'],
        )
        mas.attach_file(file_send)
        mas.send()
        return HttpResponse("DONE")
    except Exception as e:
        print(e)
        return HttpResponse(e)