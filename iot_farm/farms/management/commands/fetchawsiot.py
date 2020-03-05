import boto3
import json
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from ...models import Sensor


class Command(BaseCommand):
    help = 'Fetch IoT data from AWS IoT'

    def handle(self, *args, **options):
        client = boto3.client(service_name='iot-data', region_name=settings.AWS_REGION_NAME,
                              aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        try:
            response = client.get_thing_shadow(thingName='Text_00')
        except client.exceptions.ResourceNotFoundException:
            raise CommandError('resource not found')
        payload = response['payload'].read().decode('utf-8')
        data = json.loads(payload)
        self.stdout.write(self.style.SUCCESS('Successfully fetch IoT data from AWS IoT'))