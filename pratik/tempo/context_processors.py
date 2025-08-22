from .models import Customer

def customer_context(request):
    if "login_id" in request.session:
        try:
            customer = Customer.objects.get(id=request.session['login_id'])
            return {'customer': customer}
        except Customer.DoesNotExist:
            return {}
    return {}
