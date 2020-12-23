from django.contrib import admin
from app.models import (
    Type,
    Size,
    Topping,
    Pizza,
    PizzaTopping,
)

# Register your models here.
# admin.site.register([Type, Size, Pizza, Topping, PizzaTopping])


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "type",
        "not_deleted",
        "created_at"
    )


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "size",
        "not_deleted",
        "created_at"
    )


@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "topping",
        "not_deleted",
        "created_at"
    )


@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "type",
        "size",
        "not_deleted",
        "created_at",
        "updated_at"
    )


@admin.register(PizzaTopping)
class PizzaToppingAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "pizza",
        "topping",
        "not_deleted",
        "created_at",
        "updated_at"
    )
