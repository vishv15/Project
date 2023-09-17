from django.shortcuts import render
from django.http import HttpResponse
from .models import publisher,City,Category,Event,EventDetail,EventPrice,Review,RegisterUser
from .myforms import EventPriceForm
import random as rd 
from datetime import datetime
#below two classes are required to send email
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db import connection

#convert 12 hours format time into 24 hours format time 
def timeConversion(s):
    if "PM" in s:
        s=s.replace("PM","")
        t= s.split(":")
        if t[0] != '12':
            t[0]=str(int(t[0])+12)
            s= (":").join(t)
        return s
    else:
        s = s.replace("AM","")
        t= s.split(":")
        if t[0] == '12':
            t[0]='00'
            s= (":").join(t)
        return s

# Create your views here.
def index(request):
    return HttpResponse('this is sample home page')
def admin_login(request):
    return render(request,'admin/login.html')
def admin_change_password(request):
    return render(request,'admin/change-password.html')
def admin_forgot_password(request):
    return render(request,'admin/forgot-password.html')
def publisher_change_password(request):
    if request.method == "POST":
        #get vallue (id) from session 
        id = request.session.get('userid')
        #SELECT * FROM PUBLISHER WHERE ID=ID AND PASSWORD=CURRENT_PASSWORD
        result = publisher.objects.all().filter(id=id,password=request.POST['current_password'])
        size = len(result)
        if size==0: #invalid current password
            return render(request,'publisher/change-password.html',{'message':'invalid current password'})
        elif request.POST['new_password']!=request.POST['confirm_password']:
            return render(request,'publisher/change-password.html',{'message':'new password and confirm new password must be same'})
        else:
            #update password 
            publisher.objects.filter(id=id).update(password=request.POST['new_password'])
            return render(request,'publisher/change-password.html',{'message':'password changed successfully'})
    else:
        return render(request,'publisher/change-password.html')
def publisher_forgot_password(request):
    if request.method == "POST":
        email = request.POST['email']
        #select * from publisher where email = email 
        result = publisher.objects.filter(email=email)
        no_of_rows = len(result)
        if no_of_rows==1:
            #email found
            #generate 6 digit random number (password)
            random_password = str(rd.randint(10,99)) +  str(rd.randint(10,99)) +  str(rd.randint(10,99))
            
            #update publisher table
            # update publisher set password=random_password where email=email
            print(random_password)
            publisher.objects.filter(email=email).update(password=random_password)
            # send this password as email
            subject = 'Password Recovery email from Notifier'
            message =  f" your new password is  {random_password}"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]    
            send_mail( subject, message, email_from, recipient_list )    
            return render(request,'publisher/login.html',{'message':'you password is sent to you on your registered email address'})
        else:
            return render(request,'publisher/forgot-password.html',{'message':'invalid email address'})    
    else:
        return render(request,'publisher/forgot-password.html')
def publisher_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        #select * publisher where email=email and password=password
        result = publisher.objects.all().filter(email=email,password=password)
        no_of_rows = len(result)
        if no_of_rows==1:
            for row in result:
                #create session variable
                request.session['userid'] = row.id
                break
            events = Event.objects.all().filter(publisherid=request.session.get('userid'))
            return render(request,'publisher/event-management.html',{'event_table':events}) 
        else:
            return render(request,'publisher/login.html',{'message':'invalid login attempt'})    
    else:
        return render(request,'publisher/login.html')
def publisher_register(request):
    if request.method == "POST":
        #create model class object
        p1 = publisher(email=request.POST['email'],password=request.POST['password'],name=request.POST['name'],mobile=request.POST['mobile'],address=request.POST['address'],city=request.POST['city'],company=request.POST['company'],website=request.POST['website'],photo=request.FILES['photo'])
        p1.save()
        return render(request,'publisher/login.html')
    else:
        return render(request,'publisher/register.html')
def insert_event(request):
    if request.method == "POST":
        #object = Class
        event = Event(publisherid=request.session.get('userid'),title=request.POST['title'],detail=request.POST['detail'],photo=request.FILES['photo'],city=request.POST['city'],eventtype=request.POST['eventtype'],categoryid=request.POST['categoryid'])
        event.save()
        events = Event.objects.all().filter(publisherid=request.session.get('userid'))
        return render(request,'publisher/event-management.html',{'event_table':events,'message':'event has been added successfuly'})
    else:
        #fetch City
        city_table = City.objects.all()
        #fetch Category
        #select * from category
        category_table = Category.objects.all()
        return render(request,'publisher/insert-event.html',
                    {'city_table':city_table,'category_table':category_table})
        
def events(request):
    #fetch events select * from events where publisherid=
    events = Event.objects.all().filter(publisherid=request.session.get('userid'))
    return render(request,'publisher/event-management.html',{'event_table':events})
    
def delete_event(request,eventid):
    #delete from event where id=eventid
    Event.objects.filter(id=eventid).delete()
    events = Event.objects.all().filter(publisherid=request.session.get('userid'))
    return render(request,'publisher/event-management.html',{'event_table':events,'message':'event has been deleted successfuly'})

def view_event_detail(request,eventid,categoryid):
    #select * from event where id=eventid
    events = Event.objects.all().filter(id=eventid)
    
    #select * from category where id=categoryid
    category = Category.objects.all().filter(id=categoryid)
    
    #select * from event_detail where eventid=eventid
    eventdetail = EventDetail.objects.all().filter(eventid=eventid)
    
    return render(request,'publisher/event-detail.html',{'event_table':events,'category_table':category,'eventdetail_table':eventdetail})

def edit_event(request,eventid):
    #select * from events where id=eventid
    events = Event.objects.all().filter(id=eventid)
    category = Category.objects.all()
    city = City.objects.all()
    for event_row in events:
        print(event_row.title)
    return render(request,'publisher/edit-event.html',{'event':event_row,'category_table':category,'city_table':city})

def update_event(request):
    # events = Event.objects.all().filter(id=request.POST['eventid'])
    events=Event.objects.get(pk=request.POST['eventid'])
    events.title = request.POST['title']
    events.detail = request.POST['detail']
    events.photo = request.FILES['photo']
    events.city = request.POST['city']
    events.eventtype = request.POST['eventtype']
    events.categoryid = request.POST['categoryid']
    events.save()
    
    events = Event.objects.all().filter(publisherid=request.session.get('userid'))
    return render(request,'publisher/event-management.html',{'event_table':events,'message':'event has been updated successfuly'})

def insert_event_detail(request,eventid=0):
    if request.method == "POST":
        data = request.POST
        eventid = data.get('eventid')
        event_detail = EventDetail(eventid=data.get('eventid'),event_date=data.get('eventdate'),event_time=data.get('eventtime'),duration=data.get('duration'),address1=data.get('address1'),address2=data.get('address2'),contactno=data.get('contactno'),contactperson=data.get('contactperson'),is_canceled=data.get('is_canceled'))
        event_detail.save()
        events = Event.objects.all().filter(publisherid=request.session.get('userid'))
        return render(request,'publisher/event-management.html',{'event_table':events,'message':'event detail has been added successfuly'})
    else:
        return render(request,'publisher/insert_event_detail.html',{'eventid':eventid})
    
def delete_event_detail(request,event_detail_id):
    EventDetail.objects.filter(id=event_detail_id).delete()
    events = Event.objects.all().filter(publisherid=request.session.get('userid'))
    return render(request,'publisher/event-management.html',{'event_table':events,'message':'event detail has been deleted successfuly'})

def edit_event_detail(request,event_detail_id):
    table = EventDetail.objects.get(pk=event_detail_id)
    eventdate2 = datetime.strptime(str(table.event_date),'%Y-%m-%d')
    temp = str(eventdate2)[0:10]
    temp2 = timeConversion(table.event_time).strip() + ":00"
    return render(request,'publisher/edit_event_detail.html',
                  {'event_detail':table,'temp':temp,'temp2':temp2})
    
def update_event_detail(request):
    #select * from eventdetail where id= eventdetailid
    data = request.POST
    event_detail=EventDetail.objects.get(pk=data.get('eventdetailid'))
    event_detail.event_date = data.get('eventdate')
    event_detail.event_time = data.get('eventtime')
    event_detail.duration = data.get('duration')
    event_detail.address1 = data.get('address1')
    event_detail.address2 = data.get('address2')
    event_detail.contactno = data.get('contactno')
    event_detail.contactperson = data.get('contactperson')
    event_detail.is_canceled = data.get('is_canceled')
    event_detail.save()
    events = Event.objects.all().filter(publisherid=request.session.get('userid'))
    return render(request,'publisher/event-management.html',{'event_table':events,'message':'event detail has been updated successfuly'})

def insert_event_price(request,event_detail_id=0):
    if request.method == "POST":
        myform = EventPriceForm(request.POST)
        if myform.is_valid():
            myform.save()
            events = Event.objects.all().filter(publisherid=request.session.get('userid'))
            return render(request,'publisher/event-management.html',{'event_table':events,'message':'event price added successfuly'})
    else:
        myform = EventPriceForm()
        return render(request,'publisher/insert-event-price.html',{'myform':myform})
def view_price(request,event_detail_id):
    table = EventPrice.objects.all().filter(eventid=event_detail_id)
    return render(request,'publisher/event-price.html',{'table':table,'event_detail_id':event_detail_id})

def delete_event_price(request,id):
    EventPrice.objects.filter(id=id).delete()
    events = Event.objects.all().filter(publisherid=request.session.get('userid'))
    return render(request,'publisher/event-management.html',{'event_table':events,'message':'event price removed successfuly'})

def edit_event_price(request,id,event_detail_id):
    single_event_price = get_object_or_404(EventPrice,id=id);
    myform = EventPriceForm(request.POST or None,instance=single_event_price)
    if myform.is_valid():
        myform.save()
        events = Event.objects.all().filter(publisherid=request.session.get('userid'))
        return render(request,'publisher/event-management.html',{'event_table':events,'message':'event price edit successfully'})
    return render(request,'publisher/edit-event-price.html',{'myform':myform})

def publisher_logout(request):
    del request.session['userid']
    return render(request,'publisher/login.html',{'message':'logout successfull'})

def reviews(request):
    #select * from reviews
    # table = Review.objects.all()
    with connection.cursor() as cursor:
        cursor.execute("select event.title,review.title as title,review.detail as detail,rating as eventtitle from notifier_event as event, notifier_review as review where review.eventid=event.id")
        table = cursor.fetchall()
    print(table)
    return render(request,'publisher/review.html',{'table':table})