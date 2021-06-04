# from django.http import HttpResponseRedirect
import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.defaulttags import register
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
# Create your views here.
from admin_app.models import Venue
from frontend_app.forms import EventBookForm, MessageUsForm, UserForm
from frontend_app.models import FrontendInfo, PackageType, Package, EventsOrganize, TeamMember, CheckoutInfo, EventBook, \
    PackageFood
from django.core import serializers


@register.filter
def queryset_as_json(qs):
    """
    Sample usage:
        {{user.list_tipi_movimento|queryset_as_json}}
    """
    json_data = serializers.serialize("json", qs)
    return mark_safe(json_data)


def object_as_dict(obj):
    data = {}

    for field in obj._meta.local_fields:
        # Code stolen from Serializer
        value = field.value_from_object(obj)
        # Protected types (i.e., primitives like None, numbers, dates,
        # and Decimals) are passed through as is. All other values are
        # converted to string first.
        if is_protected_type(value):
            data[field.name] = value
        else:
            data[field.name] = field.value_to_string(obj)

    # Collect ids of M2M related items
    for field in obj._meta.get_fields():
        if field.is_relation and field.many_to_many:
            data[field.name] = [str(o.id) for o in getattr(obj, field.name).all()]

    return data


@register.filter
def object_as_json(obj):
    """
    Sample usage:
        {{original|object_as_json}}
    """

    try:
        data = object_as_dict(obj)
    except:
        data = {}

    json_data = json.dumps(data, cls=DjangoJSONEncoder)
    return mark_safe(json_data)


def message_us(request):
    frontend = FrontendInfo.objects.first()
    packages = PackageType.objects.all()
    my_packages = Package.objects.all()
    events = EventsOrganize.objects.all()
    members = TeamMember.objects.all()
    form = EventBookForm()
    if request.method == 'POST':
        message_us_form = MessageUsForm(request.POST)

        # check whether it's valid:
        if message_us_form.is_valid():
            message_us_form.save()
            messages.success(request, "Thank you for contacting us.")

            return HttpResponseRedirect('/')
        else:
            return render(request, 'index.html',
                          {
                              'data': frontend, 'packages': packages, 'my_packages': my_packages,
                              'form': form, 'events': events, 'members': members, 'message_us': message_us_form
                          })


def index(request):
    frontend = FrontendInfo.objects.first()
    packages = PackageType.objects.all()
    my_packages = Package.objects.all()
    events = EventsOrganize.objects.all()
    members = TeamMember.objects.all()
    message_us_form = MessageUsForm()
    event_today = False
    if request.user.is_authenticated:
        events_book = EventBook.objects.filter(user=request.user)
        for i in events_book:
            if i.is_date_today:
                event_today = True
    if request.method == 'POST':
        print(request.POST)
        # create a form instance and populate it with data from the request:
        form = EventBookForm(request.POST)
        print(form.data)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            messages.success(request, "Event book successfully placed. We'll contact you soon")

            return HttpResponseRedirect('/')
    else:
        form = EventBookForm()

    return render(request, 'index.html',
                  {
                      'event_today': event_today,
                      'data': frontend, 'packages': packages, 'my_packages': my_packages,
                      'form': form, 'events': events, 'members': members, 'message_us': message_us_form
                  })


def loginnow(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username is not None and password is not None:

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print(request.POST.get('next'))
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('index')
            else:
                messages.error(request, 'Please provide valid information')
                return redirect('login')

    else:
        back_img = FrontendInfo.objects.first()
        return render(request, 'login.html', {'img': back_img.login_background})


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password'],
                email=request.POST['email'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
            )
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password'],
                                    )
            if new_user is not None:
                login(request, new_user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('index')
            else:
                return redirect('login')
    else:
        form = UserForm()
    back_img = FrontendInfo.objects.first()
    return render(request, 'register.html', {'form': form, 'img': back_img.login_background})


@login_required(login_url='/login/')
def checkout_now(request, package_id=None):
    venue = Venue.objects.all()
    package = Package.objects.get(pk=package_id)
    event_book = EventBookForm(initial={'package': package, 'user': request.user})
    event_dates = EventBook.objects.values('date').filter(finished=False)
    package_foods = PackageFood.objects.all()
    frontend = FrontendInfo.objects.first()
    if request.method == 'POST':
        event_book = EventBookForm(data=request.POST, initial={'package': package, 'user': request.user})
        if event_book.is_valid():
            event_save = event_book.save()

            mypayment = SSLCSession(sslc_is_sandbox=True,
                                    sslc_store_id='abc6082bde7967bf',
                                    sslc_store_pass='abc6082bde7967bf@ssl')

            mypayment.set_urls(success_url='http://127.0.0.1:8000/checkout/response/success/',
                               fail_url='http://127.0.0.1:8000/',
                               cancel_url='http://127.0.0.1:8000/', ipn_url='http://127.0.0.1:8000/')
            mypayment.set_product_integration(total_amount=Decimal(event_save.total_price), currency='BDT',
                                              product_category=package.type.name,
                                              product_name=package.title, num_of_item=1, shipping_method='YES',
                                              product_profile='None')
            # mypayment.set_product_integration(total_amount=Decimal('20.20'), currency='BDT', product_category='clothing',
            #                                   product_name='demo-product', num_of_item=2, shipping_method='YES',
            #                                   product_profile='None')

            mypayment.set_customer_info(name='tania', email='johndoe@email.com', address1='demo address',
                                        address2='demo address 2', city='Dhaka', postcode='1207', country='Bangladesh',
                                        phone='01711111111')

            mypayment.set_shipping_info(shipping_to='demo customer', address='demo address', city='Dhaka',
                                        postcode='1209',
                                        country='Bangladesh')

            # If you want to post some additional values
            mypayment.set_additional_values(value_a=request.user.email, value_b=event_save.pk, value_c='1234',
                                            value_d='uuid')

            response_data = mypayment.init_payment()
            return redirect(response_data['GatewayPageURL'])
    return render(request, 'checkout.html',
                  {
                      'img': frontend.checkout_background,
                      'venues': venue,
                      'package_foods': package_foods,
                      'package': package, 'event_books': event_book,
                      'event_dates': event_dates
                  })


@csrf_exempt
def checkout_success(request):
    if request.method == 'POST':
        user = User.objects.get(email=request.POST['value_a'])
        event_book = EventBook.objects.get(pk=request.POST['value_b'])
        CheckoutInfo.objects.create(
            user=user,
            event_book=event_book,
            tran_id=request.POST['tran_id'],
            amount=request.POST['amount'],
            cart_type=request.POST['card_type'],
            transaction_date=request.POST['tran_date'],
            bank_transaction_id=request.POST['bank_tran_id'],
        )
        messages.success(request, 'Your transaction is successfully completed')
        return redirect('index')


@login_required(login_url='/login')
def my_user(request):
    event_books = EventBook.objects.filter(user=request.user)
    return render(request, 'user.html', {'event_books': event_books})


def event_date_filter(request):
    if request.is_ajax:
        event_dates = EventBook.objects.filter(finished=False).values_list('date')
        data = list(event_dates.values())
        dates_a = []
        for i in data:
            dates_a.append(i['date'].strftime('%m/%d/%Y'))
        return JsonResponse(dates_a, safe=False)


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')
