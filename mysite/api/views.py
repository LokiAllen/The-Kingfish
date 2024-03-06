# Static imports
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response

# Non-static imports
from .models import UserMessage
from .serializers import MessageSerializer

"""
 * A REST API view to handle messages between users
 * 
 * @author Jasper
"""
class MessageData(generics.GenericAPIView):
    serializer_class = MessageSerializer

    # Gets the queryset used for the view, which is the messages sent and received between the users
    def get_queryset(self):
        receiver = User.objects.get(username__iexact=self.kwargs['username'])
        user = self.request.user
        return UserMessage.objects.filter(sender=user, receiver=receiver) | UserMessage.objects.filter(sender=receiver, receiver=user)

    # GET request is to get the message data
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)

    # POST request is used to send a message
    def post(self, request, *args, **kwargs):
        request.data.update({'sender': request.user.id, 'receiver': User.objects.get(username__iexact=kwargs['username']).id})
        serializer = self.get_serializer(data=request.data)

        # Checks if the message content is valid (I.E empty message will be false)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)