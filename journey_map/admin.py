from django.contrib import admin
from .models import UserJourney, JourneyStage, JourneyAction, UserFeedback

class JourneyActionInline(admin.TabularInline):
    model = JourneyAction
    extra = 1

class UserFeedbackInline(admin.TabularInline):
    model = UserFeedback
    extra = 1

class JourneyStageInline(admin.TabularInline):
    model = JourneyStage
    extra = 1
    inlines = [JourneyActionInline]

@admin.register(UserJourney)
class UserJourneyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    inlines = [JourneyStageInline]

@admin.register(JourneyStage)
class JourneyStageAdmin(admin.ModelAdmin):
    list_display = ('stage_name', 'journey', 'order')
    search_fields = ('stage_name',)
    inlines = [JourneyActionInline]

@admin.register(JourneyAction)
class JourneyActionAdmin(admin.ModelAdmin):
    list_display = ('action_description', 'stage', 'order')
    autocomplete_fields = ('stage',)
    inlines = [UserFeedbackInline]

@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = ('feedback_text', 'action', 'is_positive')