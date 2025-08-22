from django.db import models


# Create your models here.
class Customer(models.Model):
    customer_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    customer_mobile = models.CharField(max_length=100, default=None, blank=True, null=True)
    customer_gst = models.CharField(max_length=100, default=None, blank=True, null=True)
    customer_email = models.EmailField(unique=True)
    customer_photo = models.ImageField(upload_to='static/', default=None)
    customer_password = models.CharField(max_length=100)

    def __str__(self):
        return self.customer_name

class Party(models.Model):
    party_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20, default=None, blank=True, null=True)
    email = models.EmailField(default=None)
    address = models.CharField(max_length=200)
    gst_no = models.CharField(max_length=40)
    def __str__(self):
        return self.party_name
    
class Vehicle(models.Model):
    vehicle_number = models.CharField(max_length=20, default=None)
    party_name = models.CharField(max_length=100, default=None)
    contact_number = models.CharField(max_length=20, default=None)
    address = models.CharField(max_length=200, default=None)
    vehicle_type = models.CharField(max_length=20, default=None)
    ownership = models.CharField(max_length=10, default=None)
    def __str__(self):
        return self.vehicle_number
    
class Master(models.Model):
    city = models.CharField(max_length=30,default=None)
    def __str__(self):
        return self.city

class Booking(models.Model):
    booking_number = models.PositiveIntegerField(unique=True, blank=True, null=True)
    booking_date = models.DateField()
    our_gst = models.CharField(max_length=30)
    is_deleted = models.BooleanField(default=False)
    party = models.ForeignKey("tempo.Party", on_delete=models.CASCADE)
    vehicle = models.ForeignKey("tempo.Vehicle", on_delete=models.CASCADE)
    from_city = models.ForeignKey("tempo.Master", on_delete=models.CASCADE, related_name='bookings_as_from_city',default=None)
    to_city = models.ForeignKey("tempo.Master", on_delete=models.CASCADE, related_name='bookings_as_to_city',default=None)
    
    total_hire = models.IntegerField()
    advance = models.DecimalField(max_digits=10, decimal_places=2)
    hamali = models.DecimalField(max_digits=10, decimal_places=2)
    tds = models.DecimalField(max_digits=10, decimal_places=2)
    st_charges = models.DecimalField(max_digits=10, decimal_places=2)
    commission = models.DecimalField(max_digits=10, decimal_places=2)
    other_charges = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    myExpense = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profit = models.IntegerField()
    remark = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.booking_number:
            last_booking = Booking.objects.all().order_by("id").last()
            if last_booking:
                new_number = last_booking.booking_number + 1
            else:
                new_number = 1
            self.booking_number = new_number
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.booking_number)

    
    