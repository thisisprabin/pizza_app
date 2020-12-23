from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import Type, Size, Topping, Pizza, PizzaTopping
from app.serializers import TypeSerializer, SizeSerializer, ToppingSerializer
from utility.constants import (
    RESPONSE_DATA,
    DATA_FETCH_SUCCESS_MSG,
    NO_DATA_FOUND_MSG,
    SERVER_ERR_MSG, TYPE_NOT_FOUND, SIZE_NOT_FOUND, TOPPINGS_NOT_FOUND, ERR_IN_ADD_PIZZA, PIZZA_ADD_SUCCESS_MSG,
    PIZZA_NOT_FOUND, PIZZA_UPDATE_SUCCESS_MSG, PIZZA_UPDATE_ERR_MSG, PIZZA_DEL_SUCCESS_MSG, SCHEMA_PIZZA_CREATE,
    INPUT_VALIDATION_ERROR, SCHEMA_PIZZA_UPDATE
)
from django.db import transaction

from utility.json_schema import JsonSchemaValidator
from utility.util import get_date_time_stamp

# Create your views here.


class PizzaTypesAPI(APIView):

    def get(self, request):

        response_data = RESPONSE_DATA.copy()
        try:
            se_data = TypeSerializer(Type.objects.filter(not_deleted=True), many=True)
            if se_data.data:
                response_data.update(
                    {
                        "message": DATA_FETCH_SUCCESS_MSG,
                        "status_code": status.HTTP_200_OK,
                        "data": se_data.data,
                        "success": True
                    }
                )
            else:
                response_data.update(
                    {
                        "message": NO_DATA_FOUND_MSG,
                        "status_code": status.HTTP_404_NOT_FOUND,
                        "success": False
                    }
                )
            response = Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)

            response_data.update(
                {
                    "message": SERVER_ERR_MSG,
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "success": False
                }
            )
            response = Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response


class PizzaSizeAPI(APIView):

    def get(self, request):

        response_data = RESPONSE_DATA.copy()
        try:
            se_data = SizeSerializer(Size.objects.filter(not_deleted=True), many=True)
            if se_data.data:
                response_data.update(
                    {
                        "message": DATA_FETCH_SUCCESS_MSG,
                        "status_code": status.HTTP_200_OK,
                        "data": se_data.data,
                        "success": True
                    }
                )
            else:
                response_data.update(
                    {
                        "message": NO_DATA_FOUND_MSG,
                        "status_code": status.HTTP_404_NOT_FOUND,
                        "success": False
                    }
                )
            response = Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)

            response_data.update(
                {
                    "message": SERVER_ERR_MSG,
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "success": False
                }
            )
            response = Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response


class PizzaToppingAPI(APIView):

    def get(self, request):

        response_data = RESPONSE_DATA.copy()
        try:
            se_data = ToppingSerializer(Topping.objects.filter(not_deleted=True), many=True)
            if se_data.data:
                response_data.update(
                    {
                        "message": DATA_FETCH_SUCCESS_MSG,
                        "status_code": status.HTTP_200_OK,
                        "data": se_data.data,
                        "success": True
                    }
                )
            else:
                response_data.update(
                    {
                        "message": NO_DATA_FOUND_MSG,
                        "status_code": status.HTTP_404_NOT_FOUND,
                        "success": False
                    }
                )
            response = Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)

            response_data.update(
                {
                    "message": SERVER_ERR_MSG,
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "success": False
                }
            )
            response = Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response


class PizzaAPIUtil:

    @classmethod
    @transaction.atomic
    def create(cls, data):

        response_data = RESPONSE_DATA.copy()
        # Save point
        s_point = transaction.savepoint()

        try:
            type_obj = Type.objects.filter(pk=data.get("type"), not_deleted=True)
            size_obj = Size.objects.filter(pk=data.get("size"), not_deleted=True)
            toppings_obj = Topping.objects.filter(pk__in=data.get("toppings"), not_deleted=True)

            if type_obj.exists() and size_obj.exists() and len(data.get("toppings")) == len(toppings_obj):
                type_obj = type_obj[0]
                size_obj = size_obj[0]

                _objs = {"type": type_obj, "size": size_obj}
                pizza = Pizza.objects.create(**_objs)

                if pizza:
                    pizza_toppings_objs = [PizzaTopping(topping=i, pizza=pizza) for i in toppings_obj]
                    _ack = PizzaTopping.objects.bulk_create(pizza_toppings_objs)

                    if len(_ack) == len(pizza_toppings_objs):
                        # Commit point
                        transaction.savepoint_commit(s_point)
                        response_data.update(
                            {
                                "message": PIZZA_ADD_SUCCESS_MSG,
                                "status_code": status.HTTP_200_OK,
                                "success": True
                            }
                        )
                        response = Response(response_data, status=status.HTTP_200_OK)
                    else:
                        # Rollback point
                        transaction.set_rollback(rollback=True)
                        response_data.update(
                            {
                                "message": ERR_IN_ADD_PIZZA,
                                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                                "success": False
                            }
                        )
                        response = Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    # Rollback point
                    transaction.set_rollback(rollback=True)
                    response_data.update(
                        {
                            "message": ERR_IN_ADD_PIZZA,
                            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                            "success": False
                        }
                    )
                    response = Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                if not type_obj.exists():
                    response_data.update(
                        {
                            "message": TYPE_NOT_FOUND,
                            "status_code": status.HTTP_404_NOT_FOUND,
                            "success": False
                        }
                    )
                    response = Response(response_data, status=status.HTTP_404_NOT_FOUND)

                elif not size_obj.exists():
                    response_data.update(
                        {
                            "message": SIZE_NOT_FOUND,
                            "status_code": status.HTTP_404_NOT_FOUND,
                            "success": False
                        }
                    )
                    response = Response(response_data, status=status.HTTP_404_NOT_FOUND)

                else:
                    response_data.update(
                        {
                            "message": TOPPINGS_NOT_FOUND,
                            "status_code": status.HTTP_404_NOT_FOUND,
                            "success": False
                        }
                    )
                    response = Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)

            response_data.update(
                {
                    "message": SERVER_ERR_MSG,
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "success": False
                }
            )
            response = Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response

    @classmethod
    @transaction.atomic
    def update(cls, data):
        response_data = RESPONSE_DATA.copy()
        # Save point
        s_point = transaction.savepoint()

        try:
            pizza = Pizza.objects.filter(pk=data.get("id"), not_deleted=True)
            if pizza.exists():
                pizza = pizza[0]

                toppings_obj = Topping.objects.filter(pk__in=data.get("toppings"), not_deleted=True)
                if len(data.get("toppings")) == len(toppings_obj):

                    _param = {"not_deleted": False, "updated_at": get_date_time_stamp()}
                    _ack_p = PizzaTopping.objects.filter(pizza=pizza, not_deleted=True).update(**_param)
                    if _ack_p:
                        pizza_toppings_objs = [PizzaTopping(topping=i, pizza=pizza) for i in toppings_obj]
                        _ack = PizzaTopping.objects.bulk_create(pizza_toppings_objs)

                        if len(_ack) == len(pizza_toppings_objs):
                            # Commit point
                            transaction.savepoint_commit(s_point)
                            response_data.update(
                                {
                                    "message": PIZZA_UPDATE_SUCCESS_MSG,
                                    "status_code": status.HTTP_200_OK,
                                    "success": True
                                }
                            )
                            response = Response(response_data, status=status.HTTP_200_OK)
                        else:
                            # Rollback point
                            transaction.set_rollback(rollback=True)
                            response_data.update(
                                {
                                    "message": PIZZA_UPDATE_ERR_MSG,
                                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    "success": False
                                }
                            )
                            response = Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:
                        # Rollback point
                        transaction.set_rollback(rollback=True)
                        response_data.update(
                            {
                                "message": PIZZA_UPDATE_ERR_MSG,
                                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                                "success": False
                            }
                        )
                        response = Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    response_data.update(
                        {
                            "message": TOPPINGS_NOT_FOUND,
                            "status_code": status.HTTP_404_NOT_FOUND,
                            "success": False
                        }
                    )
                    response = Response(response_data, status=status.HTTP_404_NOT_FOUND)
            else:
                response_data.update(
                    {
                        "message": PIZZA_NOT_FOUND,
                        "status_code": status.HTTP_404_NOT_FOUND,
                        "success": False
                    }
                )
                response = Response(response_data, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(e)

            response_data.update(
                {
                    "message": SERVER_ERR_MSG,
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "success": False
                }
            )
            response = Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response


class PizzaAPI(APIView):
    def get(self, request, pk):

        response_data = RESPONSE_DATA.copy()
        try:
            response_data = RESPONSE_DATA.copy()

            values = ["id", "type__type", "size__size"]

            pizza = Pizza.objects.filter(pk=pk, not_deleted=True).values(*values)
            if pizza.exists():
                pizza = pizza[0]
                toppings = [{"topping": i.get("topping__topping")} for i in PizzaTopping.objects.filter(pizza__id=pizza.get("id"), not_deleted=True).values("topping__topping")]
                data = {
                    "id": pizza.get("id"),
                    "type": pizza.get("type__type"),
                    "size": pizza.get("size__size")
                }
                data.update({"toppings": toppings})

                response_data.update(
                    {
                        "message": DATA_FETCH_SUCCESS_MSG,
                        "status_code": status.HTTP_200_OK,
                        "success": True,
                        "data": data
                    }
                )
                response = Response(response_data, status=status.HTTP_200_OK)

            else:
                response_data.update(
                    {
                        "message": PIZZA_NOT_FOUND,
                        "status_code": status.HTTP_404_NOT_FOUND,
                        "success": False
                    }
                )
                response = Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)

            response_data.update(
                {
                    "message": SERVER_ERR_MSG,
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "success": False
                }
            )
            response = Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response

    def post(self, request):

        response_data = RESPONSE_DATA.copy()
        data = request.data
        errors = JsonSchemaValidator.validate(instance=data, schema=SCHEMA_PIZZA_CREATE)
        if not errors:
            response = PizzaAPIUtil.create(data=data)
        else:
            response_data.update(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": INPUT_VALIDATION_ERROR,
                    "error_details": [{"errMsg": e} for e in errors],
                    "success": False
                }
            )
            response = Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        return response

    def patch(self, request):

        response_data = RESPONSE_DATA.copy()
        data = request.data
        errors = JsonSchemaValidator.validate(instance=data, schema=SCHEMA_PIZZA_UPDATE)
        if not errors:
            response = PizzaAPIUtil.update(data=data)
        else:
            response_data.update(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": INPUT_VALIDATION_ERROR,
                    "error_details": [{"errMsg": e} for e in errors],
                    "success": False
                }
            )
            response = Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        return response

    def delete(self, request, pk):

        response_data = RESPONSE_DATA.copy()
        try:
            response_data = RESPONSE_DATA.copy()

            pizza = Pizza.objects.filter(pk=pk, not_deleted=True)
            if pizza.exists():
                pizza = pizza[0]
                _param = {"not_deleted": False, "updated_at": get_date_time_stamp()}
                PizzaTopping.objects.filter(pizza=pizza, not_deleted=True).update(**_param)
                Pizza.objects.filter(pk=pk, not_deleted=True).update(**_param)

                response_data.update(
                    {
                        "message": PIZZA_DEL_SUCCESS_MSG,
                        "status_code": status.HTTP_200_OK,
                        "success": True,
                    }
                )
                response = Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data.update(
                    {
                        "message": PIZZA_NOT_FOUND,
                        "status_code": status.HTTP_404_NOT_FOUND,
                        "success": False
                    }
                )
                response = Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)

            response_data.update(
                {
                    "message": SERVER_ERR_MSG,
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "success": False
                }
            )
            response = Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response
