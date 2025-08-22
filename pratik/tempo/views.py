from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.db.models import Sum
from decimal import Decimal
from .models import Party,Vehicle,Master,Booking,Customer


def home(req):
    if "login_id" in req.session:
        customer = Customer.objects.get(id=req.session['login_id'])
        active_bookings = Booking.objects.filter(is_deleted=False)

        total_parties = Party.objects.count()
        total_vehicles = Vehicle.objects.count()
        total_bookings = active_bookings.count()
        total_amount = active_bookings.aggregate(total=Sum('total_hire'))['total'] or 0
        total_profit = active_bookings.aggregate(total=Sum('profit'))['total'] or 0
        total_pending = active_bookings.aggregate(total=Sum('balance'))['total'] or 0

        obj = {
            
            'total_parties': total_parties,
            'total_vehicles': total_vehicles,
            'total_bookings': total_bookings,
            'total_amount': total_amount,
            'total_profit': total_profit,
            'total_pending': total_pending,
        }
        return render(req, "index.html", obj)
    else:
        return redirect("/login/")

def register(req):
    return render(req,"register.html")

def register_now(req):
    return redirect("/register/")


def save_account(req):
    cust = Customer(
        customer_name = req.POST['customer_name'],
        customer_mobile = req.POST['customer_mobile'],
        customer_email = req.POST['customer_email'],
        customer_gst = req.POST['customer_gst'],
        customer_photo = req.FILES['customer_photo'],
        customer_password = req.POST['customer_password'],
    )
    cust.save()
    return redirect("/")

def customers(req):
    customers = Customer.objects.all()
    obj = {"customers":customers}
    return render(req,"customers.html",obj)

def edit_customers(req):
    old_info = Customer.objects.get(id = req.GET['id'])
    obj = {"old_info": old_info}
    return render(req,"edit_customers.html",obj) 

def update_account(req):
    print(req.POST)
    cust = Customer.objects.get(id = req.POST['id'])
    cust.customer_name = req.POST['customer_name']
    cust.customer_mobile = req.POST['customer_mobile']
    cust.customer_email = req.POST['customer_email']
    cust.customer_gst = req.POST['customer_gst'],
    cust.customer_password = req.POST['customer_password']
    cust.save()
    return redirect("/customers/")


def profile(req):
    active_bookings = Booking.objects.filter(is_deleted=False)
    
    total_parties = Party.objects.count()
    total_vehicles = Vehicle.objects.count()
    total_bookings = active_bookings.count()
    total_amount = active_bookings.aggregate(total=Sum('total_hire'))['total'] or 0
    total_profit = active_bookings.aggregate(total=Sum('profit'))['total'] or 0
    total_pending = active_bookings.aggregate(total=Sum('balance'))['total'] or 0

    obj = {
            
        'total_parties': total_parties,
        'total_vehicles': total_vehicles,
        'total_bookings': total_bookings,
        'total_amount': total_amount,
        'total_profit': total_profit,
        'total_pending': total_pending,
    }
    return render(req,"profile.html",obj)
def login(req):
    return render(req,"login.html")

def do_login(req):
    customer =Customer.objects.filter(
        customer_email = req.POST['customer_email'],
        customer_password = req.POST['customer_password']
    )
    if len(customer)>0:
        req.session['login_id'] = customer[0].id
        return redirect("/")
    else:
        return HttpResponse("Login Failed")
def logout(req):
    del req.session['login_id']
    return redirect("/login")


def ready_dashboard(req):
    return render(req,"index.html")

def dashboard(req):
    active_bookings = Booking.objects.filter(is_deleted=False)
    return render(req,"dashboard.html")

def booking(req):
    if "login_id" in req.session:
        login_id = req.session["login_id"]

        # Fetch the logged-in customer using the login_id
        customer = Customer.objects.get(id=login_id)
        parties = Party.objects.all()
        vehicles = Vehicle.objects.all()
        cities = Master.objects.all()

        # ✅ Get last booking and generate next booking number
        last_booking = Booking.objects.order_by('-id').first()
        if last_booking:
            next_booking_no = last_booking.booking_number + 1
        else:
            next_booking_no = 1

        context = {
            "parties": parties,
            "vehicles": vehicles,
            "cities": cities,
            "next_booking_no": next_booking_no,  # pass to template
        }

        return render(req, "tempo/booking/booking.html", context)
    else:
        return redirect("/login/")

def party(req):
    return render(req,"tempo/party/party.html")

def vehicle(req):
    return render(req,"tempo/vehicle/vehicle.html")

def master(req):
    return render(req,"tempo/master/master.html")

def save_party(req):
    pty = Party(
        party_name = req.POST['party_name'],
        contact_number = req.POST['contact_number'],
        email = req.POST['email'],
        address = req.POST['address'],
        gst_no = req.POST['gst_no'],
    )
    pty.save()
    return redirect("/tempo/party/party")


def save_vehicle(req):
    pty = Vehicle(
        vehicle_number = req.POST['vehicle_number'],
        party_name = req.POST['party_name'],
        contact_number = req.POST['contact_number'],
        address = req.POST['address'],
        vehicle_type = req.POST['vehicle_type'],
        ownership = req.POST['ownership'],
    )
    pty.save()
    return redirect("/tempo/vehicle/vehicle")

def save_master(req):
    mast = Master(
        city = req.POST['city'],
    )
    mast.save()
    return redirect("/tempo/master/master")

def master_list(req):
    mast = Master.objects.all()
    obj = {"master": mast}
    return render(req,"tempo/master/master_list.html",obj)

def edit_master(req):
    old_data = Master.objects.get(id=req.GET['id'])
    obj = {"old_data":old_data}
    return render(req,"tempo/master/edit_master.html",obj)

def update_master(req):
    emp = Master.objects.get(id = req.POST['id'])
    emp.city = req.POST['city']

    emp.save()
    return redirect("/tempo/master/master_list/")

def delete_master(req):
    Master.objects.get(id = req.GET['id']).delete()
    return redirect("/tempo/master/master_list/")





def party_list(req):
    mast = Party.objects.all()
    obj = {"party": mast}
    return render(req,"tempo/party/party_list.html",obj)

def edit_party(req):
    old_data = Party.objects.get(id=req.GET['id'])
    obj = {"old_data":old_data}
    return render(req,"tempo/party/edit_party.html",obj)

def update_party(req):
    pty = Party.objects.get(id = req.POST['id'])
    pty.party_name = req.POST['party_name']
    pty.contact_number = req.POST['contact_number']
    pty.email = req.POST['email']
    pty.address = req.POST['address']
    pty.gst_no = req.POST['gst_no']

    pty.save()
    return redirect("/tempo/party/party_list/")

def delete_party(req):
    Party.objects.get(id = req.GET['id']).delete()
    return redirect("/tempo/party/party_list/")

def vehicle_list(req):
    mast = Vehicle.objects.all()
    obj = {"vehicle": mast}
    return render(req,"tempo/vehicle/vehicle_list.html",obj)

def edit_vehicle(req):
    old_data = Vehicle.objects.get(id=req.GET['id'])
    obj = {"old_data":old_data}
    return render(req,"tempo/vehicle/edit_vehicle.html",obj)

def update_vehicle(req):
    pty = Vehicle.objects.get(id = req.POST['id'])
    pty.vehicle_number = req.POST['vehicle_number']
    pty.party_name = req.POST['party_name']
    pty.contact_number = req.POST['contact_number']
    pty.address = req.POST['address']
    pty.vehicle_type = req.POST['vehicle_type']
    pty.ownership = req.POST['ownership']

    pty.save()
    return redirect("/tempo/vehicle/vehicle_list/")

def delete_vehicle(req):
    Vehicle.objects.get(id = req.GET['id']).delete()
    return redirect("/tempo/vehicle/vehicle_list/")

def booking_list(req):
    bookings = Booking.objects.filter(is_deleted=False)
    return render(req, "tempo/booking/booking_list.html", {"bookings": bookings})

def recover_booking(request, id):
    booking = get_object_or_404(Booking, id=id)
    booking.is_deleted = False
    booking.save()
    return redirect('deleted_bookings')

def save_booking(req):
    if req.method == "POST":
        pty = Booking(
            booking_number = req.POST.get('booking_number'),
            booking_date = req.POST.get('booking_date'),
            our_gst = req.POST.get('our_gst'),
            party = Party.objects.get(id=req.POST.get('party_id')),             
            vehicle = Vehicle.objects.get(id=req.POST.get('vehicle_id')),       
            from_city = Master.objects.get(id=req.POST.get('from_city')),       
            to_city = Master.objects.get(id=req.POST.get('to_city')),           
            total_hire = Decimal(req.POST.get('total_hire', 0)),
            advance = Decimal(req.POST.get('advance', 0)),
            hamali = Decimal(req.POST.get('hamali', 0)),
            tds = Decimal(req.POST.get('tds', 0)),
            st_charges = Decimal(req.POST.get('st_charges', 0)),
            commission = Decimal(req.POST.get('commission', 0)),
            other_charges = Decimal(req.POST.get('other_charges', 0)),
            balance = Decimal(req.POST.get('balance', 0)),
            myExpense = Decimal(req.POST.get('myExpense', 0)),
            profit = Decimal(req.POST.get('profit', 0)),
            remark = req.POST.get('remark', '')
        )
        pty.save()
        return redirect("/tempo/booking/booking")
    return HttpResponse("Method not allowed", status=405)

def delete_booking(request, id):
    booking = get_object_or_404(Booking, id=id)
    booking.is_deleted = True
    booking.save()
    return redirect('/tempo/booking/deleted_bookings/')

def deleted_bookings(request):
    deleted_list = Booking.objects.filter(is_deleted=True)
    print("Deleted list count:", deleted_list.count()) 
    return render(request, "tempo/booking/deleted_bookings.html", {"deleted_list": deleted_list})

def update_booking(req, id):
    booking = Booking.objects.get(id=id)
    parties = Party.objects.all()
    vehicles = Vehicle.objects.all()
    cities = Master.objects.all()

    if req.method == "POST":
        booking.booking_number = req.POST.get('booking_number')
        booking.booking_date = req.POST.get('booking_date')
        booking.our_gst = req.POST.get('our_gst')
        
        booking.party = Party.objects.get(id=req.POST.get('party_id'))
        booking.vehicle = Vehicle.objects.get(id=req.POST.get('vehicle_id'))
        booking.from_city = Master.objects.get(id=req.POST.get('from_city'))
        booking.to_city = Master.objects.get(id=req.POST.get('to_city'))
        booking.total_hire = Decimal(req.POST.get('total_hire', 0))
        booking.advance = Decimal(req.POST.get('advance', 0))
        booking.hamali = Decimal(req.POST.get('hamali', 0))
        booking.tds = Decimal(req.POST.get('tds', 0))
        booking.st_charges = Decimal(req.POST.get('st_charges', 0))
        booking.commission = Decimal(req.POST.get('commission', 0))
        booking.other_charges = Decimal(req.POST.get('other_charges', 0))
        booking.balance = Decimal(req.POST.get('balance', 0))
        booking.myExpense = Decimal(req.POST.get('myExpense', 0))
        booking.profit = Decimal(req.POST.get('profit', 0))
        booking.remark = req.POST.get('remark', '')
        booking.save()

        return redirect("/tempo/booking/booking_list")

    context = {
        "booking": booking,
        "parties": parties,
        "vehicles": vehicles,
        "cities": cities,
    }
    return render(req, "tempo/booking/update_booking.html", context)

