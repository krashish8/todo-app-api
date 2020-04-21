from django.urls import path
from .views import TodoListView, TodoDetailView, TodoCreateView

urlpatterns = [
    path('todo/', TodoListView.as_view()),
    path('todo/<int:pk>/', TodoDetailView.as_view()),
    path('todo/create/', TodoCreateView.as_view()),
]