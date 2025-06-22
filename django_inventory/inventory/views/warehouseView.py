from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, reverse
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework import authentication, permissions
# from inventory.serializers.itemsSerializer import *
# from inventory.serializers.orderSerializer import *
from inventory.models import *

