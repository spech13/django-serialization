import json
from http import HTTPMethod, HTTPStatus

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from serialization_app.models import (
    Department,
    Employee,
    HexNut,
    Product,
    Store,
    User,
    WorkStation,
)
from serialization_app.serializers import (
    DepartmentSerializer,
    EmployeeSerializer,
    HexNutSerializer,
    ProductSerializer,
    StoreSerializer,
    UserSerializer,
    WorkStationSerializer,
)

# pylint: disable=unused-argument


def get_object(request, obj, serializer_class):
    if request.method != HTTPMethod.GET:
        return JsonResponse(
            {"error_message": f"Method {request.method} is forbinded"},
            status=HTTPStatus.BAD_REQUEST,
        )

    return JsonResponse(serializer_class(obj).data)


def get_objects(request, queryset, serializer_class):
    if request.method != HTTPMethod.GET:
        return JsonResponse(
            {"error_message": f"Method {request.method} is forbinded"},
            status=HTTPStatus.BAD_REQUEST,
        )

    return JsonResponse(serializer_class(queryset, many=True).data, safe=False)


def create(request, serializer_class):
    if request.method != HTTPMethod.POST:
        return JsonResponse(
            {"error_message": f"Method {request.method} is forbinded"},
            status=HTTPStatus.BAD_REQUEST,
        )

    data = request.body.decode()

    try:
        data = json.loads(data)
    except json.decoder.JSONDecodeError:
        return JsonResponse(
            {"error_message": f"Json decode error for {data}"},
            status=HTTPStatus.BAD_REQUEST,
        )

    serializer = serializer_class(data=json.loads(request.body.decode()))

    try:
        serializer.is_valid(raise_exception=True)
    except ValidationError as validation_error:
        return JsonResponse(
            {
                "validation_errors": {
                    key: str(value[0]) for key, value in validation_error.detail.items()
                }
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    serializer.save()
    return JsonResponse({}, status=HTTPStatus.CREATED)


def update(request, obj, serializer_class, partial=False):
    if request.method != HTTPMethod.PATCH:
        return JsonResponse(
            {"error_message": f"Method {request.method} is forbinded"},
            status=HTTPStatus.BAD_REQUEST,
        )

    data = request.body.decode()

    try:
        data = json.loads(data)
    except json.decoder.JSONDecodeError:
        return JsonResponse(
            {"error_message": f"Json decode error for {data}"},
            status=HTTPStatus.BAD_REQUEST,
        )

    serializer = serializer_class(
        obj, data=json.loads(request.body.decode()), partial=partial
    )

    try:
        serializer.is_valid(raise_exception=True)
    except ValidationError as validation_error:
        return JsonResponse(
            {
                "validation_errors": {
                    key: str(value[0]) for key, value in validation_error.detail.items()
                }
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    serializer.save()
    return JsonResponse({}, status=HTTPStatus.NO_CONTENT)


def get_hex_nuts(request):
    return get_objects(request, HexNut.objects.all(), HexNutSerializer)


def get_hex_nut(request, **kwargs):
    return get_object(
        request, get_object_or_404(HexNut, id=kwargs["id"]), HexNutSerializer
    )


def create_hex_nut(request):
    return create(request, HexNutSerializer)


def update_hex_nut(request, **kwargs):
    return update(request, get_object_or_404(HexNut, id=kwargs["id"]), HexNutSerializer)


def get_workstations(request):
    return get_objects(request, WorkStation.objects.all(), WorkStationSerializer)


def get_workstation(request, **kwargs):
    return get_object(
        request, get_object_or_404(WorkStation, id=kwargs["id"]), WorkStationSerializer
    )


def create_workstation(request):
    return create(request, WorkStationSerializer)


def update_workstation(request, **kwargs):
    return update(
        request, get_object_or_404(WorkStation, id=kwargs["id"]), WorkStationSerializer
    )


def get_stores(request):
    return get_objects(request, Store.objects.all(), StoreSerializer)


def get_store(request, **kwargs):
    return get_object(
        request, get_object_or_404(Store, id=kwargs["id"]), StoreSerializer
    )


def create_store(request):
    return create(request, StoreSerializer)


def update_store(request, **kwargs):
    return update(request, get_object_or_404(Store, id=kwargs["id"]), StoreSerializer)


def partial_update_store(request, **kwargs):
    return update(
        request,
        get_object_or_404(Store, id=kwargs["id"]),
        StoreSerializer,
        partial=True,
    )


def get_products(request):
    return get_objects(request, Product.objects.all(), ProductSerializer)


def get_product(request, **kwargs):
    return get_object(
        request, get_object_or_404(Product, id=kwargs["id"]), ProductSerializer
    )


def create_product(request):
    return create(request, ProductSerializer)


def update_product(request, **kwargs):
    return update(
        request, get_object_or_404(Product, id=kwargs["id"]), ProductSerializer
    )


def create_department(request):
    return create(request, DepartmentSerializer)


def update_department(request, **kwargs):
    return update(
        request, get_object_or_404(Department, id=kwargs["id"]), DepartmentSerializer
    )


def create_employee(request):
    return create(request, EmployeeSerializer)


def update_employee(request, **kwargs):
    return update(
        request, get_object_or_404(Employee, id=kwargs["id"]), EmployeeSerializer
    )


def get_users(request):
    return get_objects(request, User.objects.all(), UserSerializer)


def get_user(request, **kwargs):
    return get_object(request, get_object_or_404(User, id=kwargs["id"]), UserSerializer)


def create_user(request):
    return create(request, UserSerializer)


def update_user(request, **kwargs):
    return update(request, get_object_or_404(User, id=kwargs["id"]), UserSerializer)
