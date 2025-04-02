from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from customer.models import Orders
from .models import Menu
from .forms import MenuForm, UpdateMenuForm


@login_required(login_url="/login")
@staff_member_required
def add_menu_item(request):
    """This view is to add any dish item"""
    if request.method == "POST":
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("management:view_menu")
    else:
        form = MenuForm()

    return render(request, "management/add_menu_item.html", {"form": form})


@login_required(login_url="/login")
@staff_member_required
def view_menu(request):
    """This is to view the whole menu"""
    menu_items = Menu.objects.all()
    paginator = Paginator(menu_items, 5)
    page = request.GET.get("page")

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return render(request, "management/view_menu.html", {"menu_items": items})


@login_required(login_url="/login")
@staff_member_required
def specific_view_menu(request):
    """This is to view specific menu"""
    q = Q(item_price__gt=500) | Q(item_name__contains="a")
    menu_items = Menu.objects.filter(q)
    return render(request, "management/view_menu.html", {"menu_items": menu_items})


@login_required(login_url="/login")
@staff_member_required
def update_menu(request, item_id):
    """This is to update the menu item"""

    menu_item = get_object_or_404(Menu, item_id=item_id)
    form = UpdateMenuForm(instance=menu_item)
    if request.method == "POST":
        form = UpdateMenuForm(request.POST, request.FILES, instance=menu_item)
        if form.is_valid():
            form.save()
            return redirect("management:view_menu")
    return render(request, "management/add_menu_item.html", {"form": form})


@login_required(login_url="/login")
@staff_member_required
def remove_menu_item(request, item_id):
    """This view is to remove any added menu item"""

    item = get_object_or_404(Menu, item_id=item_id)

    if request.method == "POST":
        item.delete()
        messages.info(request, "The item has been deleted successfully!")
        return redirect("management:view_menu")

    return render(request, "management/remove_menu_item.html", {"item": item})


@login_required(login_url="/login")
@staff_member_required
def show_orders(request):
    """This is to show all the orders of the user"""

    orders = Orders.objects.select_related("user").all()
    if request.method == "POST":
        specific_orders = request.POST.get("specific", "")
        if specific_orders:
            orders = Orders.objects.select_related("user").filter(
                order_status=specific_orders
            )
        else:
            orders = Orders.objects.select_related("user").all()
    return render(request, "management/show_orders.html", {"orders": orders})


@login_required(login_url="/login")
@staff_member_required
def approve_order(request, order_id):
    """This is to approve order to approve"""

    myorder = Orders.objects.get(order_id=order_id)
    if request.method == "POST":
        updated_status = request.POST["Updated status"]
        myorder.order_status = updated_status
        messages.info(request, "The order status has been changed successfully!")
        myorder.save()

    return render(request, "management/approve_order.html", {"order": myorder})
