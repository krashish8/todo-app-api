from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from .serializers import TodoSerializer, TodoCreateSerializer
from .models import Todo


class TodoListView(generics.ListAPIView):
    """
    Get all the Todos of the logged in user.
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoSerializer

    def get_queryset(self):
        """
        Returns todo that belong to the logged in user.
        """
        return Todo.objects.filter(creator=self.request.user)


class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Get the Todo of the logged in user with given id.

    put:
    Change the title of the Todo with given id.

    patch:
    Change the title of the Todo with given id.

    delete:
    Delete the Todo with given id.
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoSerializer

    def get_object(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        return super().get_object()

    def get_queryset(self):
        """
        Returns todo that belong to the logged in user.
        """
        if self.request.user.is_anonymous:
            return None
        return Todo.objects.filter(creator=self.request.user)
    

class TodoCreateView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCreateSerializer

    def post(self, request):
        """
        Creates a Todo entry for the logged in user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)