from django.contrib import admin

# Register your models here.
from chat.models import Conversation, ConversationMessage, ConversationReadStatus

admin.site.register(Conversation)
admin.site.register(ConversationMessage)
admin.site.register(ConversationReadStatus)
