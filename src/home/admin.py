#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

__author__ = "Caoilte Guiry"

from models import *
from django.contrib import admin

class SportAdmin(admin.ModelAdmin):
    ordering = ("name",)

class CountryAdmin(admin.ModelAdmin):
    ordering = ("name",)

class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "country")
    list_filter = ("country",)
    ordering = ("name",)

class VenueAdmin(admin.ModelAdmin):
    list_display = ("name", "city")
    list_filter = ("city",)
    ordering = ("name",)

class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "home_city", "is_international", "sport")
    list_filter = ("home_city", "is_international", "sport")
    ordering = ("name",)

class FixtureTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "correct_win_points", "semicorrect_win_points", "incorrect_win_points", 
                    "correct_draw_points", "incorrect_draw_points")
    ordering = ("correct_win_points",)

class TournamentAdmin(admin.ModelAdmin):
    list_display = ("name", "begin_date", "end_date", "sport")
    ordering = ("begin_date", "end_date", "name", "sport")

class ResultTypeAdmin(admin.ModelAdmin):
    ordering = ("name",)

class FixtureAdmin(admin.ModelAdmin):
    list_display = ("date", "venue", "team1", "team2", "fixture_type", "tournament", "result", "score")
    list_filter = ("tournament",)
    ordering = ("date", "tournament",)

class PredictionAdmin(admin.ModelAdmin):
    list_display = ("user", "fixture", "result")
    list_filter = ("user", "fixture", "result")
    ordering = ("user",)

admin.site.register(Sport, SportAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(FixtureType, FixtureTypeAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(ResultType, ResultTypeAdmin)
admin.site.register(Fixture, FixtureAdmin)
admin.site.register(Prediction, PredictionAdmin)
