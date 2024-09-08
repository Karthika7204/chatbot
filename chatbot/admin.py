from django.contrib import admin
from chatbot.models import intents
  
@admin.register(intents)  
class Admin(admin.ModelAdmin):
    list_display=[
        'tag',
        'patterns',
        'responses'
    ]
