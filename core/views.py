from rest_framework import views
from rest_framework.response import Response
from . import tasks, models
from .queue import channel
from core.serializers import serializers
import json


class CreateWorkspaceView(views.APIView):

    def post(self, request):
        workspace = request.data.get('workspace')
        if workspace:
            email = models.Email.objects.filter(unused=True).first()
            if not email:
                return Response({'message': 'No unused emails in database'}, 500)
            email.unused = False
            email.save()
            tasks.create_workspace.delay(email, workspace)
            return Response(status=200)
        else:
            return Response({'message': 'Parameter workspace not found in request'}, 400)


class AddVerificationCodeView(views.APIView):

    def post(self, request):
        if 'Slack confirmation code' in str(request.POST.get('subject')):
            email = request.POST.get('To')
            code = str(request.POST.get('subject')).split(':')[1].strip().replace('-', '')
            instance = models.Email.objects.get(email=email)
            instance.code = code
            instance.save()
            channel.basic_publish(exchange='', routing_key='slack',
                                  body=json.dumps({email: code}))
        return Response(status=200)


class EmailView(views.APIView):

    def get(self):
        emails = models.Email.objects.all()
        serializer = serializers.EmailSerializer(emails, many=True)
        return Response({'emails': serializer.data})

    def post(self, request):
        errors =[]
        for email in request.data.get('emails'):
            try:
                models.Email.objects.create(email=email, status='new')
            except:
                errors.append(email)
        if errors:
            return Response({'message': 'Emails have been added but these emails already exist', 'emails': errors}, 400)
        else:
            return Response(status=200)

