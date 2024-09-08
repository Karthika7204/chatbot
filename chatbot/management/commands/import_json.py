import json
from django.core.management.base import BaseCommand
from chatbot.models import intents  # Make sure the class name matches your model

class Command(BaseCommand):
    help = 'Import external JSON file data into Django database'

    def handle(self, *args, **kwargs):
        with open(r'D:\nlp project\chatbot\data\intents.json', 'r', encoding='utf8') as file:
            data = json.load(file)
            # Iterate over the 'intents' key in the JSON data
            for item in data['intents']:
                intents.objects.create(  # Ensure you're using the correct model class
                    tag=item['tag'],
                    patterns=', '.join(item['patterns']),  # Convert list to comma-separated string
                    responses=', '.join(item['responses'])  # Convert list to comma-separated string
                )
        self.stdout.write(self.style.SUCCESS('Done'))