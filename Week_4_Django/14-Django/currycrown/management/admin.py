from django.contrib import admin
from customer.models import Orders
from .models import Menu
import csv
from django.http import HttpResponse
from django.contrib.auth import get_user

admin.site.site_header = "CurryCrown Admin Dashboard"
admin.site.index_title = f"Welcome to CurryCrown Admin"


@admin.action(description="Mark Completed")
def mark_complete(model_admin, request, queryset):
    queryset.update(order_status="complete")
    for q in queryset:
        q.save()


@admin.action(description="Download CSV")
def download_csv(model_admin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="Items.csv"'
    writer = csv.writer(response)

    headers = ["Item", "Price", "Rating"]
    writer.writerow(headers)

    data = [
        [model.item_name, model.item_price, model.item_rating] for model in queryset
    ]
    writer.writerows(data)

    return response


class MenuItemPriceFilter(admin.SimpleListFilter):
    title = "Price Range"
    parameter_name = "price"

    def lookups(self, request, model_admin):
        return (
            ("0-100", "0-100 Rs"),
            ("100-200", "100-200 Rs"),
            ("200-500", "200-500 Rs"),
            ("500<=", "500 and above Rs"),
        )

    def queryset(self, request, queryset):
        if self.value() == "0-100":
            return queryset.filter(item_price__lte=50)
        if self.value() == "100-200":
            return queryset.filter(item_price__range=(50, 100))
        if self.value() == "200-500":
            return queryset.filter(item_price__range=(100, 200))
        if self.value() == "500<=":
            return queryset.filter(item_price__gte=500)


@admin.register(Menu)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("item_id", "item_name", "item_price", "item_rating")
    search_fields = ("item_name",)
    list_filter = (MenuItemPriceFilter,)
    actions = [download_csv]


@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_id", "order_details", "order_status", "order_time")
    search_fields = ("order_id",)
    actions = [mark_complete]
