from django.shortcuts import render, redirect, reverse
from .models import Orders
from management.models import Menu
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def view_menu(request):
    menu_items = Menu.objects.all()
    return render(request, "customer/view_menu.html", {"menu_items": menu_items})


@login_required(login_url="/login")
def place_order(request):
    if request.method == "POST":
        order_details = []
        menu_items = request.POST.getlist("menu_items")
        quantities = request.POST.getlist("quantities")
        quantities = [i for i in quantities if i != "0"]
        print(menu_items)
        print(quantities)
        if menu_items and quantities:
            total = 0
            for item_name, quantity in zip(menu_items, quantities):
                if quantity == 0:
                    continue
                order_details.append(
                    {
                        "item_name": item_name,
                        "quantity": quantity,
                    }
                )

                total += int(
                    Menu.objects.values_list("item_price", flat=True).get(
                        item_name=item_name
                    )
                ) * int(quantity)

            order = Orders.objects.create(
                user=request.user, order_details=order_details, total_price=total
            )
            return redirect("customer:order_confirmation", order_id=order.order_id)
        return redirect("customer:place_order")

    menu_items = Menu.objects.all()
    return render(request, "customer/place_order.html", {"menu_items": menu_items})


@login_required(login_url="/login")
def order_confirmation(request, order_id):
    order = Orders.objects.get(order_id=order_id)
    return render(request, "customer/order_confirmation.html", {"order": order})


def view_orders(request, user_id):
    user = User.objects.get(id=user_id)
    orders = Orders.objects.filter(user=user)

    return render(request, "customer/show_orders.html", {"orders": orders})
