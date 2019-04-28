from .views import CreateWorkspaceView, AddVerificationCodeView, EmailView
from django.urls import path, include

webhook_patterns = [
    path('add-code/', AddVerificationCodeView.as_view()),
]

urlpatterns = [
    path('create-workspace/', CreateWorkspaceView.as_view()),
    path('webhook/', include(webhook_patterns)),
    path('emails/', EmailView.as_view())
]
