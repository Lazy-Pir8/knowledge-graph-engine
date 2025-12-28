from django.contrib import admin
from .models import Topic
# Register your models here
@admin.register(Topic)

class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_description',)
    search_fields = ('name',)

    exclude = ('slug',)
    def short_description(self, obj):
        words = obj.description.split()
        return ' '.join(words[:50]) + ('...' if len(words) > 50 else '')

    short_description.short_description = 'Description'