import json
from http import HTTPMethod, HTTPStatus

from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import get_object_or_404, render
from rest_framework.exceptions import ValidationError

from serialization_app.models import HexNut, Product, Store, WorkStation
from serialization_app.serializers import (
    HexNutSerializer,
    ProductSerializer,
    StoreSerializer,
    WorkStationSerializer,
)

# pylint: disable=unused-argument


def get_hex_nuts(request):
    return JsonResponse(
        HexNutSerializer(HexNut.objects.all(), many=True).data, safe=False
    )


def get_hex_nut(request, **kwargs):
    return JsonResponse(
        HexNutSerializer(get_object_or_404(HexNut, id=kwargs["id"])).data
    )


def create_hex_nut(request):
    if request.method == HTTPMethod.GET:
        return render(request, template_name="serialization_app/create_hex_nuts.html")

    json_data = QueryDict(request.body)["json_data"]

    try:
        json_data_loads = json.loads(json_data)
    except json.decoder.JSONDecodeError:
        return HttpResponse(
            f"Failed data loads: {json_data}", status=HTTPStatus.BAD_REQUEST
        )

    hex_nuts_serializer = HexNutSerializer(data=json_data_loads, many=True)
    if hex_nuts_serializer.is_valid():
        hex_nuts_serializer.save()
    else:
        return HttpResponse(
            f"Data is not valid: {json_data}", status=HTTPStatus.BAD_REQUEST
        )

    return HttpResponse(f"Successful request: {json_data}", status=HTTPStatus.OK)


def update_hex_nut(request):
    if request.method == HTTPMethod.GET:
        return render(request, template_name="serialization_app/update_hex_nut.html")

    request_body = QueryDict(request.body)

    nut_id = int(request_body["nut_id"])
    json_data = request_body["json_data"]

    try:
        json_data_loads = json.loads(json_data)
    except json.decoder.JSONDecodeError:
        return HttpResponse(
            f"Failed data loads: {json_data}", status=HTTPStatus.BAD_REQUEST
        )

    hex_nut_serializer = HexNutSerializer(
        get_object_or_404(HexNut, id=nut_id), data=json_data_loads
    )

    if hex_nut_serializer.is_valid():
        hex_nut_serializer.save()
    else:
        return HttpResponse(
            f"Data is not valid: {json_data}", status=HTTPStatus.BAD_REQUEST
        )

    return HttpResponse(f"Successful reques: {json_data}", status=HTTPStatus.OK)


def get_workstations(request):
    if request.method != HTTPMethod.GET:
        return HttpResponse(f"Method {request.method} is forbinded")

    return JsonResponse(
        WorkStationSerializer(WorkStation.objects.all(), many=True).data, safe=False
    )


def get_workstation(request, **kwargs):
    if request.method != HTTPMethod.GET:
        return HttpResponse(f"Method {request.method} is forbinded")

    return JsonResponse(
        WorkStationSerializer(get_object_or_404(WorkStation, id=kwargs["id"])).data
    )


def create_workstation(request):
    if request.method != HTTPMethod.POST:
        return HttpResponse(f"Method {request.method} is forbinded")

    try:
        data = json.loads(request.body.decode())
    except json.decoder.JSONDecodeError:
        return HttpResponse(
            f"Json decode error for {request.body.decode()}",
            status=HTTPStatus.BAD_REQUEST,
        )

    workstaion_serializer = WorkStationSerializer(data=data)

    try:
        workstaion_serializer.is_valid(raise_exception=True)
    except ValidationError as validation_error:
        return JsonResponse(
            {
                "validation_errors": {
                    key: str(value[0]) for key, value in validation_error.detail.items()
                }
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    workstaion_serializer.save()
    return HttpResponse(status=HTTPStatus.CREATED)


def update_workstation(request, **kwargs):
    if request.method != HTTPMethod.PATCH:
        return HttpResponse(f"Method {request.method} is forbinded")

    try:
        data = json.loads(request.body.decode())
    except json.decoder.JSONDecodeError:
        return HttpResponse(
            f"Json decode error for {request.body.decode()}",
            status=HTTPStatus.BAD_REQUEST,
        )

    workstaion_serializer = WorkStationSerializer(
        get_object_or_404(WorkStation, id=kwargs["id"]), data=data
    )

    try:
        workstaion_serializer.is_valid(raise_exception=True)
    except ValidationError as validation_error:
        return JsonResponse(
            {
                "validation_errors": {
                    key: str(value[0]) for key, value in validation_error.detail.items()
                }
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    workstaion_serializer.save()
    return HttpResponse(status=HTTPStatus.NO_CONTENT)


def create_store(request):
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

    store_serializer = StoreSerializer(data=data)

    try:
        store_serializer.is_valid(raise_exception=True)
    except ValidationError as validation_error:
        return JsonResponse(
            {
                "validation_errors": {
                    key: str(value[0]) for key, value in validation_error.detail.items()
                }
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    store_serializer.save()
    return JsonResponse({}, status=HTTPStatus.CREATED)


def update_store(request, **kwargs):
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

    store_serializer = StoreSerializer(
        get_object_or_404(Store, id=kwargs["id"]), data=data
    )

    try:
        store_serializer.is_valid(raise_exception=True)
    except ValidationError as validation_error:
        return JsonResponse(
            {
                "validation_errors": {
                    key: str(value[0]) for key, value in validation_error.detail.items()
                }
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    store_serializer.save()
    return JsonResponse({}, status=HTTPStatus.NO_CONTENT)


def partial_update_store(request, **kwargs):
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

    store_serializer = StoreSerializer(
        get_object_or_404(Store, id=kwargs["id"]), data=data, partial=True
    )

    try:
        store_serializer.is_valid(raise_exception=True)
    except ValidationError as validation_error:
        return JsonResponse(
            {
                "validation_errors": {
                    key: str(value[0]) for key, value in validation_error.detail.items()
                }
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    store_serializer.save()
    return JsonResponse({}, status=HTTPStatus.NO_CONTENT)


def create_product(request):
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

    product_serializer = ProductSerializer(data=data)

    try:
        product_serializer.is_valid(raise_exception=True)
    except ValidationError as validation_error:
        return JsonResponse(
            {
                "validation_errors": {
                    key: str(value[0]) for key, value in validation_error.detail.items()
                }
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    product_serializer.save()
    return JsonResponse({}, status=HTTPStatus.CREATED)


def update_product(request, **kwargs):
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

    product_serializer = ProductSerializer(
        get_object_or_404(Product, id=kwargs["id"]), data=data
    )

    try:
        product_serializer.is_valid(raise_exception=True)
    except ValidationError as validation_error:
        return JsonResponse(
            {
                "validation_errors": {
                    key: str(value[0]) for key, value in validation_error.detail.items()
                }
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    product_serializer.save()
    return JsonResponse({}, status=HTTPStatus.NO_CONTENT)
