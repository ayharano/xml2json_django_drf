from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from xml_converter.parsers import ParseError, XMLParser


class ConverterViewSet(ViewSet):
    # Note this is not a restful API
    # We still use DRF to assess how well you know the framework
    parser_classes = [MultiPartParser]

    @action(methods=["POST"], detail=False, url_path="convert")
    def convert(self, request, **kwargs):
        try:
            data = XMLParser().parse(request.FILES['file'].open())
        except ParseError as exc:
            return Response(
                {'detail': str(exc)},
                status=400,
            )

        return Response(data)
