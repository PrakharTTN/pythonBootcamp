from django.shortcuts import render, redirect, get_object_or_404
from .models import Orders
from management.models import Menu
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def view_menu(request):
    menu_items = Menu.objects.all()
    return render(request, "customer/view_menu.html", {"menu_items": menu_items})


# TODO: Handle exceptions:
    # ValueError - When quantity is not a valid integer or is out of range not between 1 and 5.
    # KeyError- When an invalid menu item not in the valid_menu_items is selected.
    # Empty order- When no valid menu items are selected or quantities are provided.
@login_required
def place_order(request):
    if request.method == "POST":
        menu_items = request.POST.getlist("menu_items")
        quantities = request.POST.getlist("quantities")

        valid_items = []
        total = 0

        valid_menu_items = {item.item_name: item.item_price for item in Menu.objects.all()}

        for item_name, quantity in zip(menu_items, quantities):
            try:
                quantity = int(quantity)  
                if quantity < 1 or quantity > 5:
                    raise ValueError 

            except ValueError:
                messages.error(request, f"Invalid quantity for {item_name}. Please enter a whole number between 1 and 5.")
                return redirect("customer:place_order")

            if item_name not in valid_menu_items:
                messages.error(request, "Invalid menu item detected.")
                return redirect("customer:place_order")

            valid_items.append((item_name, quantity))
            total += valid_menu_items[item_name] * quantity  

        if not valid_items:
            messages.error(request, "Please select at least one valid menu item with a valid quantity.")
            return redirect("customer:place_order")

        order_details = [{"item_name": item_name, "quantity": quantity} for item_name, quantity in valid_items]

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

    orders = Orders.objects.filter(user=request.user)
    return render(request, "customer/show_orders.html", {"orders": orders})
