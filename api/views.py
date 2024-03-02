from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from rest_framework import status


class View(APIView):
    def get(self, request):
        data = {'twoja stara': 'kurwa stara'}
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        print(request.data)
        return HttpResponseRedirect('/api/view')