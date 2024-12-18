from django.contrib import admin
from .models import Mood, Affirmation, JournalingPrompt, Recommendation, User

admin.site.register(Mood)
admin.site.register(Affirmation)
admin.site.register(JournalingPrompt)
admin.site.register(Recommendation)
from django.contrib import admin
from .models import JournalEntry

@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'prompt', 'text', 'created_at')
    search_fields = ('user__username', 'prompt__text', 'text')
    list_filter = ('created_at', 'user')
