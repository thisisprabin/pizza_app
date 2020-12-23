from django.db import migrations


pizza_type_master_data = [
    {"type": "Regular"},
    {"type": "Square"}
]

pizza_size_master_data = [
    {"size": "Small"},
    {"size": "Medium"},
    {"size": "Large"}
]

pizza_topping_master_data = [
    {"topping": "Onion"},
    {"topping": "Tomato"},
    {"topping": "Corn"},
    {"topping": "Capsicum"},
    {"topping": "Cheese"},
    {"topping": "Jalapeno"},
]


def add_pizza_type_master_data(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Type = apps.get_model("app", "Type")

    _new_data = []
    for d in pizza_type_master_data:
        _new_data.append(Type(type=d.get("type")))

    Type.objects.using(db_alias).bulk_create(_new_data)


def add_pizza_size_master_data(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Size = apps.get_model("app", "Size")

    _new_data = []
    for d in pizza_size_master_data:
        _new_data.append(Size(size=d.get("size")))

    Size.objects.using(db_alias).bulk_create(_new_data)


def add_pizza_topping_master_data(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Topping = apps.get_model("app", "Topping")

    _new_data = []
    for d in pizza_topping_master_data:
        _new_data.append(Topping(topping=d.get("topping")))

    Topping.objects.using(db_alias).bulk_create(_new_data)


class Migration(migrations.Migration):
    dependencies = [
        ('app', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(add_pizza_type_master_data),
        migrations.RunPython(add_pizza_size_master_data),
        migrations.RunPython(add_pizza_topping_master_data),
    ]
