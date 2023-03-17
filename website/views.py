from django.shortcuts import render, redirect
from django.contrib import messages
from decouple import config
import boto3
from django.http import HttpResponse
from django.core.validators import validate_email


def index(request):
    return render(request, 'website/index.html')


def send_email(request):

    ses_access_key_id = config('SES_AWS_ACCESS_KEY_ID')
    ses_secret_access_key = config('SES_AWS_SECRET_ACCESS_KEY')

    if request.method == 'POST':
        # Get the form data
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')



        # Create the email client
        client = boto3.client(
            'ses',
            region_name='us-east-1',
            aws_access_key_id=ses_access_key_id,
            aws_secret_access_key=ses_secret_access_key
        )

        # Send the email
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    'millionairematt@gmail.com',
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': 'Email address: {}\n\nMessage:\n{}'.format(email, message),

                    },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': 'Message from ' + name,
                },
            },
            Source='millionairematt@gmail.com',
        )

        # Check the response
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            messages.success(request, 'Your message has been sent!')
            return redirect('/#contact')
        else:
            messages.error(request, 'There was an error sending the message.')
            return redirect('/#contact')
    else:
        return render(request, '/#contact')

