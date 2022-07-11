

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import BookSerializer, UserSerializer, RegisterSerializer
from .models import User, Book
from rest_framework.authtoken.serializers import AuthTokenSerializer
import jwt
from rest_framework import viewsets, permissions
from .custompermission import Isadmin
import datetime
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import login


class RegisterAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": RegisterSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


@api_view(['GET'])
def current_user(request):
    serializer = RegisterSerializer(request.user)
    return Response(serializer.data)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


@api_view(['GET'])
@permission_classes([Isadmin])
def apiOverview(request):

    api_urls = {
        'createbook': '/createbook/',
        'updatebook': '/updatebook/',
        'deletebook': '/deletebook/', }

    return Response(api_urls)


@api_view(['GET'])
def bookList(request):
    book = Book.objects.all().order_by('book_id')
    serializer = BookSerializer(book, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def bookDetail(request, pk):
    book = Book.objects.get(id=pk)
    serializer = BookSerializer(book)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([Isadmin])
def bookCreate(request):
    serializer = BookSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([Isadmin])
def bookUpdate(request, pk):
    book = Book.objects.get(id=pk)
    serializer = BookSerializer(instance=book, data=request.data)

    if serializer.is_valid():

        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([Isadmin])
def bookDelete(request, pk):
    book = Book.objects.get(id=pk)
    book.delete()

    return Response('Item succsesfully delete!')


@api_view(['POST'])
def bookborrow(request, pk):
    book = Book.objects.get(id=pk)
    serializer = BookSerializer(instance=book, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.validated_data['bookstatus'] = "Borrowed"
    serializer.save()

    return Response(serializer.validated_data['bookstatus'])


@api_view(['POST'])
def bookreturn(request, pk):
    book = Book.objects.get(id=pk)
    serializer = BookSerializer(instance=book, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.validated_data['bookstatus'] = "Available"
    serializer.save()

    return Response("Book returned Sucessfully!!!")
