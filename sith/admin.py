from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Planet, Sith, Challenge, Question


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(Planet)
class PlanetAdmin(admin.ModelAdmin):
    pass


@admin.register(Sith)
class SithAdmin(admin.ModelAdmin):
    pass


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass

