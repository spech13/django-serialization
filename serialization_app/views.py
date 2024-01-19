import json
from http import HTTPMethod, HTTPStatus

from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import get_object_or_404, render

from serialization_app.models import HexNut
from serialization_app.serializers import HexNutSerializer

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
