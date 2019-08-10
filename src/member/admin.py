from django.contrib import admin

from .models import TeamGroup, Team, PlayerProfile, Member

from common.admin import BaseAdmin, BaseTabularInline


class TeamInline(BaseTabularInline):
    model = Team
    fields = []


class TeamGroupAdmin(BaseAdmin):
    list_display = ('name',)
    fields = []
    inlines = [TeamInline]


admin.site.register(TeamGroup, TeamGroupAdmin)


class PlayerProfileInline(BaseTabularInline):
    model = PlayerProfile
    fields = []


class MemberAdmin(BaseAdmin):
    list_display = ('family_name', 'first_name', 'team_group')
    fields = []
    inlines = [PlayerProfileInline]


admin.site.register(Member, MemberAdmin)
