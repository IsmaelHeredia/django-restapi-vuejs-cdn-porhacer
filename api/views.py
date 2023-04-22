# pip3 install djangorestframework
# pip install django-cors-headers

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models import Tarea
from .serializers import TareaSerializer
from rest_framework import permissions
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
import requests

class TareaListApiView(APIView):

    def get(self, request, *args, **kwargs):
        tareas = Tarea.objects.all()
        serializer = TareaSerializer(tareas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'titulo': request.data.get('titulo'), 
            'estado': request.data.get('estado'), 
        }
        serializer = TareaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class TareaDetailApiView(APIView):

    def get_object(self, tarea_id):
        try:
            return Tarea.objects.get(id=tarea_id)
        except Tarea.DoesNotExist:
            return None

    def get(self, request, tarea_id, *args, **kwargs):
        tarea_instance = self.get_object(tarea_id)
        if not tarea_instance:
            return Response(
                {"res": "El registro con ese ID no existe"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TareaSerializer(tarea_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, tarea_id, *args, **kwargs):
        tarea_instance = self.get_object(tarea_id)
        if not tarea_instance:
            return Response(
                {"res": "El registro con ese ID no existe"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'titulo': request.data.get('titulo'), 
            'estado': request.data.get('estado'), 
        }
        serializer = TareaSerializer(instance = tarea_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, tarea_id, *args, **kwargs):
        tarea_instance = self.get_object(tarea_id)
        if not tarea_instance:
            return Response(
                {"res": "El registro con ese ID no existe"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        tarea_instance.delete()
        return Response(
            {"res": "Registro borrado"},
            status=status.HTTP_200_OK
        )

@api_view(['POST'])
def enviarTareas(request):
    
    token_telegram = ""
    chat_id = ""

    api_url = f"https://api.telegram.org/bot{token_telegram}/sendMessage"

    mensaje = ""

    tareas = Tarea.objects.filter(estado=1)

    for tarea in tareas:
        titulo = tarea.titulo
        mensaje = mensaje + titulo + "\n"

    try:
        response = requests.post(api_url, json={'chat_id': chat_id, 'text': mensaje})
        print(response.text)
    except Exception as e:
        print(e)

    return Response(
        {"res": "Registros enviados"},
        status=status.HTTP_200_OK
    )