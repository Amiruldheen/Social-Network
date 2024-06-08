from django.shortcuts import render

from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from django.contrib.auth import authenticate, get_user_model
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle


from django.db.models import Q

from .serializers import UserSerializer, LoginSerializer, FriendRequestSerializer
from .models import FriendRequest




# import logging

# logger = logging.getLogger(__name__)


# Create your views here.
User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email'].lower()
        password = serializer.validated_data['password']

        # logger.debug(f"Attempting login with email: {email}")

        user = authenticate(request, username=email, password=password)
        # print(user)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            # logger.debug("Login successful")
            return Response({'token': token.key})
        return Response({'error': 'Invalid Credentials'}, status=400)


class UserSearchPagination(PageNumberPagination):
    page_size = 10

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = UserSearchPagination

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        if '@' in query:
            return User.objects.filter(email__iexact=query)
        return User.objects.filter(username__icontains=query)


class FriendRequestThrottle(UserRateThrottle):
    rate = '3/min'


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([FriendRequestThrottle])
def send_friend_request(request):
    to_user_id = request.data.get('to_user_id')
    to_user = User.objects.get(id=to_user_id)
    friend_request, created = FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user, status='pending')
    if created:
        return Response({'status': 'Friend request sent'}, status=status.HTTP_201_CREATED)
    return Response({'status': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respond_to_friend_request(request):
    request_id = request.data.get('request_id')
    status1 = request.data.get('status')
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.to_user == request.user:
        friend_request.status = status1
        friend_request.save()
        return Response({'status': f'Friend request {status1}'}, status=status.HTTP_200_OK)
    return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_friends(request):
    friends = FriendRequest.objects.filter(Q(from_user=request.user, status='accepted') | Q(to_user=request.user, status='accepted'))
    friends_list = [frd.to_user if frd.from_user == request.user else frd.from_user for frd in friends]
    serializer = UserSerializer(friends_list, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_pending_requests(request):
    pending_requests = FriendRequest.objects.filter(to_user=request.user, status='pending')
    serializer = FriendRequestSerializer(pending_requests, many=True)
    return Response(serializer.data)