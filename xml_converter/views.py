from django.http import JsonResponse
from django.shortcuts import render

from xml_converter.forms import UploadFileForm
from xml_converter.parsers import ParseError, XMLParser


def upload_page(request):
    form = UploadFileForm()

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if not form.is_valid():
            return JsonResponse({'detail': form.errors}, status=400)

        try:
            data = XMLParser().parse(request.FILES['file'].open())
        except ParseError as exc:
            return JsonResponse({'detail': str(exc)}, status=400)

        return JsonResponse(data)

    return render(request, "upload_page.html", {"form": form})
