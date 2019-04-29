from rest_framework import views
from rest_framework.response import Response

from . import tasks, models
from .csv_file import CSVFile
from .queue import channel
from . import validators
from .serializers import serializers
import json

class WriteEmailsFromCSVFile(views.APIView):

    def put(self, request):
        emails_from_file = CSVFile().read_emails()
        for email in emails_from_file:
            email_in_database = models.Email.objects.filter(email=email).first()
            if not email_in_database:
                models.Email.objects.create(email=email)
        return Response({'message': 'Records were written'}, 200)


class CreateWorkspaceView(views.APIView):

    def post(self, request):
        workspace = request.data.get('workspace')
        if workspace:
            record = models.Email.objects.filter(unused=True).first()
            if not record:
                return Response({'message': 'No unused emails in database'}, 500)
            record.unused = False
            record.save()
            tasks.create_workspace.delay(record.email)
            return Response({'email': record.email}, 200)
        else:
            return Response({'message': 'Parameter workspace not found in request'}, 400)


class CreateAllWorkspacesView(views.APIView):

    def get(self, request):
        records = models.Email.objects.filter(unused=True).all()
        for record in records:
            record.unused = False
            record.save()
            tasks.create_workspace.delay(record.email)
        return Response({'message': 'All tasks were created'}, 200)



class AddVerificationCodeView(views.APIView):

    def post(self, request):
        if 'Slack confirmation code' in str(request.POST.get('subject')):
            email = request.POST.get('To')
            code = str(request.POST.get('subject')).split(':')[1].strip().replace('-', '')
            instance = models.Email.objects.get(email=email)
            instance.code = code
            instance.save()
            # TODO: rabbit queue
            # channel.basic_publish(exchange='', routing_key='email',
            #                       body=json.dumps({email: code}))
        return Response(status=200)


class EmailView(views.APIView):

    def get(self):
        emails = models.Email.objects.all()
        serializer = serializers.EmailSerializer(emails, many=True)
        return Response({'emails': serializer.data}, 200)

    def post(self, request):
        if not validators.validate_email_post(request.data):
            return Response({'message': 'Invalid required parameters'}, 400)
        errors = []
        for email in request.data.get('emails'):
            try:
                models.Email.objects.create(email=email, status='new')
            except:
                errors.append(email)
        if errors:
            return Response({'message': 'Emails have been added but these emails already exist', 'emails': errors}, 400)
        else:
            return Response(status=200)
