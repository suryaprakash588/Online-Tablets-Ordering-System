from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from .models import Medicine, CartItem, Cart, Prescription, Order, OrderItem, Product, Address
from .forms import AddressForm, PrescriptionForm
from django.utils import timezone
from django.contrib.auth import logout



def home(request):
    medicines = Medicine.objects.all()[:10] 
    return render(request, 'store/home.html', {'medicines': medicines})

def products(request):
    products = Product.objects.all()
    return render(request, 'store/products.html', {'products': products})

def product_detail(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    return render(request, 'store/product_detail.html', {'medicine': medicine})


def search_medicines(request):
    query = request.GET.get('q', '')
    medicines = Medicine.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'store/search_results.html', {'medicines': medicines, 'query': query})


@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('medicine')

    subtotal = sum(item.medicine.price * item.quantity for item in cart_items)
    delivery_charge = 0 if subtotal >= 500 else 50
    discount = 0  
    total = subtotal + delivery_charge - discount

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'delivery_charge': delivery_charge,
        'discount': discount,
        'total': total
    })




@login_required
def add_to_cart(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    
    
    cart, created = Cart.objects.get_or_create(user=request.user)

    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, medicine=medicine)

    if not created:
        cart_item.quantity += 1
    cart_item.save()

    messages.success(request, f"{medicine.name} added to cart")
    return redirect('cart') 



@login_required
def confirm_order(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart, medicine__isnull=False)

    if not cart_items.exists():
        return redirect('cart')

    # Create the Order
    order = Order.objects.create(user=request.user)


    # Add cart items to OrderItem
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            medicine=item.medicine,
            quantity=item.quantity,
            price=item.medicine.price
        )

    # Clear the cart
    cart_items.delete()

    return redirect('order_success')

 


@login_required
def upload_prescription(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, request.FILES)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.user = request.user  
            prescription.save()
            return redirect('prescription_success')  
    else:
        form = PrescriptionForm()
    return render(request, 'store/upload_prescription.html', {'form': form})


def upload_success(request):
    return render(request, 'store/upload_success.html')


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = UserCreationForm()
    return render(request, 'store/signup.html', {'form': form})


@login_required
def update_cart(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                item_id = key.split('_')[1]
                try:
                    item = CartItem.objects.get(id=item_id)
                    item.quantity = int(value)
                    item.save()
                except:
                    continue
    return redirect('cart')


def set_pincode(request):
    pincode = request.GET.get('pincode')
    if pincode:
        request.session['user_pincode'] = pincode
    return redirect(request.META.get('HTTP_REFERER', '/'))


def search_view(request):
    query = request.GET.get('q')
    medicines = []
    if query:
        medicines = Medicine.objects.filter(name__icontains=query)
    return render(request, 'store/search_results.html', {'medicines': medicines, 'query': query})


def medicine_detail(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    return render(request, 'store/medicine_detail.html', {'medicine': medicine})


def search(request):
    query = request.GET.get('q')
    medicine = Medicine.objects.filter(name__icontains=query).first()
    if medicine:
        return redirect('medicine_detail', pk=medicine.pk)
    return render(request, 'store/search_results.html', {'query': query})


def view_cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price})
    else:
        return redirect('login')



@login_required
def address_list(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'store/addresses_list.html', {'addresses': addresses})

@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            
            
            if address.is_default:
                Address.objects.filter(user=request.user).update(is_default=False)
            
            address.save()
            return redirect('addresses_list')
    else:
        form = AddressForm()
    
    return render(request, 'store/address_form.html', {'form': form, 'title': 'Add Address'})

@login_required
def edit_address(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():

            if form.cleaned_data['is_default']:
                Address.objects.filter(user=request.user).exclude(pk=pk).update(is_default=False)
            form.save()
            return redirect('address_list')
    else:
        form = AddressForm(instance=address)
    
    return render(request, 'store/address_form.html', {'form': form, 'title': 'Edit Address'})

@login_required
def delete_address(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    if request.method == 'POST':
        address.delete()
        return redirect('address_list')
    return render(request, 'store/address_confirm_delete.html', {'address': address})


def prescription_success(request):
    return render(request, 'store/prescription_success.html')



@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart')


def custom_logout(request):
    logout(request)
    return redirect('home')

def seed_medicines(request):
    if Medicine.objects.exists():
        return HttpResponse("Medicines already seeded.")

    sample_medicines = [
        {
            "name": "Paracetamol",
            "description": "Used to relieve mild to moderate pain and reduce fever.",
            "price": 25.00,
        },
        {
            "name": "Amoxicillin",
            "description": "Antibiotic for bacterial infections like pneumonia and bronchitis.",
            "price": 75.00,
        },
        {
            "name": "Ibuprofen",
            "description": "NSAID used to reduce pain, fever, and inflammation.",
            "price": 50.00,
        },
        {
            "name": "Metformin",
            "description": "Used to treat type 2 diabetes by controlling blood sugar.",
            "price": 90.00,
        },
        {
            "name": "Azithromycin",
            "description": "Antibiotic used for respiratory, skin, and ear infections.",
            "price": 120.00,
        },
        {
            "name": "Dolo 650",
            "description": "Brand of paracetamol used to relieve fever and pain.",
            "price": 30.00,
        },
    ]

    for med in sample_medicines:
        Medicine.objects.create(
            name=med["name"],
            description=med["description"],
            price=med["price"],
            mrp=med["price"] + 10  
        )

    return HttpResponse("Sample medicines seeded successfully.")


@login_required
def order_success(request):
    return render(request, 'store/order_success.html')
