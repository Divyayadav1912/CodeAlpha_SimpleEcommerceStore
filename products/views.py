

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Product

from django.db import transaction
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



def product_list(request):
    products = Product.objects.all()
    return render(request, "products/product_list.html", {
        "products": products
    })



def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get("cart", {})
    product_key = str(product_id)
    current_quantity = int(cart.get(product_key, 0))

    if product.stock > current_quantity:
        cart[product_key] = current_quantity + 1
        request.session["cart"] = cart
        request.session.modified = True

    return redirect("view_cart")



def view_cart(request):
    cart = request.session.get("cart", {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.objects.filter(id=product_id).first()

        if product:
            subtotal = product.price * quantity
            cart_items.append({
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            })
            total += subtotal

    return render(request, "products/cart.html", {
        "cart_items": cart_items,
        "total": total,
    })


@login_required
def checkout(request):
    from .models import Order, OrderItem

    cart = request.session.get("cart", {})
    cart_items = []
    total = 0

    def build_cart_items():
        items = []
        amount = 0

        for product_id, quantity in cart.items():
            try:
                quantity = int(quantity)
                product = Product.objects.filter(id=product_id).first()
            except (ValueError, TypeError):
                continue

            if product and quantity > 0:
                subtotal = product.price * quantity
                items.append({
                    "product": product,
                    "quantity": quantity,
                    "subtotal": subtotal,
                })
                amount += subtotal

        return items, amount

    cart_items, total = build_cart_items()

    if not cart_items:
        return redirect("view_cart")

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()
        city = request.POST.get("city", "").strip()
        pincode = request.POST.get("pincode", "").strip()

        if (
            not full_name or not address or not city
            or len(phone) != 10 or not phone.isdigit()
            or len(pincode) != 6 or not pincode.isdigit()
        ):
            messages.error(
                request, "Please enter valid delivery details."
            )
        else:
            order = None
            stock_error = None

            with transaction.atomic():
                product_ids = sorted(int(pid) for pid in cart.keys())

                locked_products = {
                    product.id: product
                    for product in Product.objects.select_for_update()
                    .filter(id__in=product_ids)
                    .order_by("id")
                }

                validated_items = []
                current_total = 0

                for product_id, quantity in cart.items():
                    try:
                        product_id = int(product_id)
                        quantity = int(quantity)
                    except (ValueError, TypeError):
                        stock_error = "Invalid cart item. Please review your cart."
                        break

                    product = locked_products.get(product_id)

                    if not product or quantity <= 0:
                        stock_error = "A product in your cart is unavailable."
                        break

                    if product.stock < quantity:
                        stock_error = (
                            f"Insufficient stock for {product.name}. "
                            f"Available stock: {product.stock}."
                        )
                        break

                    subtotal = product.price * quantity
                    validated_items.append((product, quantity))
                    current_total += subtotal

                if stock_error:
                    messages.error(request, stock_error)
                else:
                    order = Order.objects.create(
    user=request.user if request.user.is_authenticated else None,
    full_name=full_name,
    phone=phone,
    address=address,
    city=city,
    pincode=pincode,
    total_amount=current_total,
)

                    for product, quantity in validated_items:
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=quantity,
                            price=product.price,
                        )

                        product.stock -= quantity
                        product.save(update_fields=["stock"])

            if order:
                request.session["cart"] = {}
                request.session.modified = True

                return render(
                    request,
                    "products/order_success.html",
                    {"order": order},
                )

            # Refresh the cart after a stock validation failure.
            cart_items, total = build_cart_items()

    return render(request, "products/checkout.html", {
        "cart_items": cart_items,
        "total": total,
    })



def increase_quantity(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        cart = request.session.get("cart", {})
        key = str(product_id)
        quantity = cart.get(key, 0)

        if quantity < product.stock:
            cart[key] = quantity + 1
            request.session["cart"] = cart

    return redirect("view_cart")


@require_POST
def decrease_quantity(request, product_id):
    cart = request.session.get("cart", {})
    key = str(product_id)

    if key in cart:
        quantity = int(cart[key])

        if quantity > 1:
            cart[key] = quantity - 1
        else:
            cart.pop(key)

        request.session["cart"] = cart
        request.session.modified = True

    return redirect("view_cart")

@require_POST
def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    cart.pop(str(product_id), None)
    request.session["cart"] = cart
    return redirect("view_cart")

def signup(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not all([full_name, username, email, password, confirm_password]):
            messages.error(request, "Please fill in all fields.")

        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")

        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")

        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")

        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=full_name,
            )
            login(request, user)
            return redirect("product_list")

    return render(request, "products/signup.html")





def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            next_url = request.POST.get("next") or request.GET.get("next")

            if next_url and next_url.startswith("/") and not next_url.startswith("//"):
                return redirect(next_url)

            return redirect("product_list")

        messages.error(request, "Invalid username or password.")

    return render(request, "products/login.html", {
        "next": request.GET.get("next", "")
    })




def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect("product_list")

    return redirect("product_list")


@login_required
def my_orders(request):
    from .models import Order

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "products/my_orders.html",
        {"orders": orders}
    )
