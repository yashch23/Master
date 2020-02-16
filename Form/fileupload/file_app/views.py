from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer
from .formapp import FormApp
import json
import time
class FileView(APIView):
  parser_classes = (MultiPartParser, FormParser)
  def post(self, request, *args, **kwargs):
    file_serializer = FileSerializer(data=request.data)
    if file_serializer.is_valid():
      file_serializer.save()
      file_string = file_serializer.data
      string_ob = FormApp(file_string["file"]).mainapp()
      ob = {"data" : string_ob}
      json_ob = ob
      print(json_ob)
      return Response(json_ob, status=status.HTTP_201_CREATED, content_type="application/json")
    else:
      return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TestView(APIView):
    def post(self, request, *args, **kwargs):
        return Response("Hello World!", status=status.HTTP_201_CREATED)
