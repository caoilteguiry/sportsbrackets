#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

__author__ = "Caoilte Guiry"

from django.db import models
from django.contrib.auth.models import User

class Sport(models.Model):
    name = models.CharField(max_length=20) # XXX: arbitrary max_length

    class Meta:
        db_table = u"sports"
        verbose_name_plural = u"sports"
        
    def __unicode__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=100) # XXX: arbitrary max_length
    code = models.CharField(max_length=2)
    # TODO: continent & population & lat/lon?

    class Meta:
        db_table = u"countries"
        verbose_name_plural = u"countries"
        
    def __unicode__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100) # XXX: arbitrary max_length
    country = models.ForeignKey(Country)
    # TODO: lat & lon & population?
    
    class Meta:
        db_table = u"cities"
        verbose_name_plural = u"cities"
        
    def __unicode__(self):
        return self.name

class Venue(models.Model):
    name = models.CharField(max_length=100) # XXX: arbitrary max_length
    city = models.ForeignKey(City)
    # TODO: lat & lon?
    
    class Meta:
        db_table = u"venues"
        verbose_name_plural = u"venues"
        
    def __unicode__(self):
        return self.name 


class Team(models.Model):
    name = models.CharField(max_length=100) # XXX: arbitrary max_length
    home_city = models.ForeignKey(City, null=True, blank=True)
    is_international = models.BooleanField()
    sport = models.ForeignKey(Sport, null=True, blank=True)

    class Meta:
        db_table = u"teams"
        verbose_name_plural = u"teams"
        ordering = ['sport', 'is_international', 'name']
    
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.sport)


class FixtureType(models.Model):
    name = models.CharField(max_length=100) # XXX: arbitrary max_length
    correct_win_points  = models.PositiveSmallIntegerField()
    semicorrect_win_points = models.PositiveSmallIntegerField()
    incorrect_win_points = models.PositiveSmallIntegerField()
    correct_draw_points = models.PositiveSmallIntegerField()
    incorrect_draw_points = models.PositiveSmallIntegerField()
    is_drawable = models.PositiveSmallIntegerField()
    sport = models.ForeignKey(Sport)
    class Meta:
        db_table = u"fixture_types"
        verbose_name_plural = u"fixture_types"
    
    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.sport)
    
class Tournament(models.Model):
    name = models.CharField(max_length=100) # XXX: arbitrary max_length
    begin_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    sport = models.ForeignKey(Sport)
    # TODO: set_in (e.g. city, country, continent?) May be tricky to implement

    class Meta:
        db_table = u"tournaments"
        verbose_name_plural = u"tournaments"
    
    def __unicode__(self):
        return self.name

class ResultType(models.Model):
    name = models.CharField(max_length=15)

    class Meta:
        db_table = u"result_types"
        verbose_name_plural = u"result_types"
    
    def __unicode__(self):
        return self.name        
    

class Fixture(models.Model):
    date = models.DateTimeField(null=True, blank=True)
    venue = models.ForeignKey(Venue, null=True, blank=True)
    team1 = models.ForeignKey(Team, related_name="team1")
    team2 = models.ForeignKey(Team, related_name="team2")
    fixture_type = models.ForeignKey(FixtureType)
    tournament = models.ForeignKey(Tournament)
    result = models.ForeignKey(ResultType, null=True, blank=True)
    score = models.CharField(max_length=7, null=True, blank=True) # TODO: custom MatchScoreField? 
    
    class Meta:
        db_table = u"fixtures"
        verbose_name_plural = u"fixtures"
        
    def __unicode__(self):
        return "%s vs %s" % (self.team1, self.team2)
    
class Prediction(models.Model):
    user = models.ForeignKey(User)
    fixture = models.ForeignKey(Fixture)
    result = models.ForeignKey(ResultType)
    
    class Meta:
        db_table = u"predictions"
        verbose_name_plural = u"predictions"
    
    def __unicode__(self):
        return u"%s predicts a %s for %s " % (self.user, self.result, self.fixture)
