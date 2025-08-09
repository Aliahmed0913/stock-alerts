from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterUserSerializer
from django.contrib.auth import get_user_model

# Create your views here.  IsAuthenticated
user = get_user_model()
@api_view(['POST','GET'])
def register_user(request):
    if request.method == 'POST':
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'User created successfully',
                             'user':serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
   
    else:
        serializer = RegisterUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
           