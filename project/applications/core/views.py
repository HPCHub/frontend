from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_xml.renderers import XMLRenderer
from serializers import SamplePayloadSerializer


class BaseTextPayloadViewSet(viewsets.ViewSet):

    serializer_class = SamplePayloadSerializer

    def list(self, request):
        serializer = SamplePayloadSerializer.generate()
        serializer.is_valid()
        return Response(serializer.data)


class JsonPayloadViewSet(BaseTextPayloadViewSet):
    """
    Get sample payload in JSON format
    ---
    list:
        serializer: SamplePayloadSerializer
    """
    pass


class XmlPayloadViewSet(BaseTextPayloadViewSet):
    """
    Get sample payload in XML format
    ---
    list:
        serializer: SamplePayloadSerializer
    """
    renderer_classes = (XMLRenderer, )

