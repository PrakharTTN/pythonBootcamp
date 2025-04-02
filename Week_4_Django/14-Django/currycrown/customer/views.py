from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import Orders
from management.models import Menu
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render


@login_required
def view_menu(request):
    menu_items = Menu.objects.all()
    paginator = Paginator(menu_items, 5)
    page = request.GET.get("page")

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return render(request, "customer/view_menu.html", {"menu_items": items})


@login_required
def place_order(request):
    if request.method == "POST":
        menu_items = []
        quantities = []
        valid_items = []
        total = 0
        valid_menu_items = {
            item.item_name: item.item_price for item in Menu.objects.all()
        }

        for key, value in request.POST.items():
            if key == "csrfmiddlewaretoken" or value == "0":
                continue  # Skip CSRF token or zero quantities

            try:
                menu_item = Menu.objects.get(item_id=key)
                menu_items.append(menu_item.item_name)
                quantities.append(int(value))

            except ObjectDoesNotExist:
                messages.error(request, f"Menu item with ID {key} not found.")
                return redirect("customer:place_order")

        # Validate quantities and check if menu items are valid
        for item_name, quantity in zip(menu_items, quantities):
            if not (1 <= quantity <= 5):
                messages.error(
                    request,
                    f"Invalid quantity for {item_name}. Enter a number between 1 and 5.",
                )
                return redirect("customer:place_order")

            if item_name not in valid_menu_items:
                messages.error(request, f"Invalid menu item: {item_name}.")
                return redirect("customer:place_order")

            valid_items.append((item_name, quantity))
            total += valid_menu_items[item_name] * quantity

        order_details = [
            {"item_name": item_name, "quantity": quantity}
            for item_name, quantity in valid_items
        ]

        order = Orders.objects.create(
            user=request.user, order_details=order_details, total_price=total
        )

        messages.success(request, "Order placed successfully!")
        return redirect("customer:order_confirmation", order_id=order.order_id)

    menu_items = Menu.objects.all()
    return render(request, "customer/place_order.html", {"menu_items": menu_items})


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Orders, order_id=order_id)
    return render(request, "customer/order_confirmation.html", {"order": order})


@login_required
def view_orders(request, user_id):
    if request.user.id != user_id:
        return redirect("customer:view_menu")

    orders = Orders.objects.select_related("user").filter(user=request.user)
    return render(request, "customer/show_orders.html", {"orders": orders})
