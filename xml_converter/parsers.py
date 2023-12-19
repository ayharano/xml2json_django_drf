"""
Adapted from https://github.com/encode/django-rest-framework/blob/3.14.0/rest_framework/parsers.py
to provide a XMLParser based on the existing JSONParser.

[XML parsing is not secure against maliciously constructed data](https://docs.python.org/3/library/xml.html#xml-vulnerabilities),
so ideally we would be using third-party libraries.
Given that there is a restriction to not use external libraries other than
Django and DRF, for this solution, we are using a Python standard library XML parser.
"""
import codecs
import xml.etree.ElementTree as ET

from django.conf import settings
from rest_framework import renderers
from rest_framework.exceptions import ParseError
from rest_framework.parsers import BaseParser


def element_to_dict(element_object):
    """
    Using a depth-first traversal using an Element
    as its current root node to generate a dictionary.
    """
    tag = element_object.tag
    from_children = []

    for child in element_object:
        from_children.append(element_to_dict(child))

    if from_children:
        value = from_children
    elif element_object.text:
        value = element_object.text
    else:
        value = ''

    return {tag: value}


class XMLParser(BaseParser):
    """
    Parses XML-serialized data.
    """
    media_type = 'application/xml'  # From https://www.rfc-editor.org/rfc/rfc7303.html section 4.1
    renderer_class = renderers.JSONRenderer  # For this solution, we will be converting XML to JSON
    strict = False

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Parses the incoming bytestream as XML and returns the resulting data.
        """
        parser_context = parser_context or {}
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)

        try:
            decoded_stream = codecs.getreader(encoding)(stream)
            tree = ET.parse(decoded_stream)
            element_tree_root = tree.getroot()
            return element_to_dict(element_tree_root)
        except (ValueError, ET.ParseError) as exc:
            raise ParseError('XML parse error - %s' % str(exc))
