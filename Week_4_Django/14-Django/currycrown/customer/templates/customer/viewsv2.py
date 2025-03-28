from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist

def place_order(request):
    if request.method == "POST":
        menu_items = []
        quantities = []
        
        # Get all valid menu items once to avoid repeated database queries
        valid_menu_items = {item.item_name: item.item_price for item in Menu.objects.all()}
        
        for key, value in request.POST.items():
            if key == "csrfmiddlewaretoken":
                continue  # Skip CSRF token
            if value != '0':  # value is a string in request.POST, so check if it's not '0'
                try:
                    menu_item = Menu.objects.get(item_id=key)  # Query the Menu object once
                    menu_items.append(menu_item.item_name)
                    quantities.append(int(value))  # Convert quantity to integer

                except ObjectDoesNotExist:
                    messages.error(request, f"Menu item with ID {key} not found.")
                    return redirect("customer:place_order")

        # Validate quantities and check if menu items are valid
        total = 0
        for item_name, quantity in zip(menu_items, quantities):
            # Validate quantity
            if not (1 <= quantity <= 5):
                messages.error(
                    request,
                    f"Invalid quantity for {item_name}. Please enter a whole number between 1 and 5.",
                )
                return redirect("customer:place_order")

            # Check if item is valid
            if item_name not in valid_menu_items:
                messages.error(request, f"Invalid menu item: {item_name}.")
                return redirect("customer:place_order")

            # Accumulate total price for the order
            total += valid_menu_items[item_name] * quantity

        # Assuming you would proceed with order placement here
        # You can create the order or further processing here
        messages.success(request, f"Order placed successfully. Total: ${total:.2f}")
        return redirect("customer:order_confirmation")

    return render(request, "customer/place_order.html")

from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist

def place_order(request):
    if request.method == "POST":
        menu_items = []
        quantities = []
        
        # Get all valid menu items once
        valid_menu_items = {item.item_name: item.item_price for item in Menu.objects.all()}
        
        for key, value in request.POST.items():
            if key == "csrfmiddlewaretoken" or value == '0':
                continue  # Skip CSRF token or zero quantities

            try:
                # Query Menu item and add to lists
                menu_item = Menu.objects.get(item_id=key)
                menu_items.append(menu_item.item_name)
                quantities.append(int(value))  # Convert quantity to int

            except ObjectDoesNotExist:
                messages.error(request, f"Menu item with ID {key} not found.")
                return redirect("customer:place_order")

        # Validate quantities and check if menu items are valid
        for item_name, quantity in zip(menu_items, quantities):
            if not (1 <= quantity <= 5):  # Quantity validation
                messages.error(request, f"Invalid quantity for {item_name}. Enter a number between 1 and 5.")
                return redirect("customer:place_order")

            if item_name not in valid_menu_items:  # Item existence check
                messages.error(request, f"Invalid menu item: {item_name}.")
                return redirect("customer:place_order")

        # You could add order creation or further processing here
        messages.success(request, "Order placed successfully!")
        return redirect("customer:order_confirmation")

    return render(request, "customer/place_order.html")
