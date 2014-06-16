#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

__author__ = "Caoilte Guiry"

import datetime
import logging

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.template import RequestContext
from django.core.cache import cache


from models import ResultType
from models import Tournament
from models import Fixture
from models import FixtureType
from models import Prediction
from models import Sport
#from custom_decorators import timer

logger = logging.getLogger("debugger")

__author__ = "Caoilte Guiry"

""" TODO:  
* Handle timezones, etc. (Store time in UTC, and adjust for client TZ?)
* Allow clicking on teams, instead of radio buttons
* Add menubar? 
* Automatically generate knockout fixtures (tricky!)
* Automatically fill in scores/results (cron scripts)
* Implement "groups" functionality.
* Sort out join stuff (very inefficient!)
* Delete unused teams (we don't nee all 300 world countires!)
* Links (login & register) should cover full button, not just the <a> part
* Color login buttons on login page like the other buttons
* Create a login_not_required decorator and make login_required the default
* Automatically log user in after registration?
* Mobile App?
* Prevent "staff members"/admin users from editing fixtures with non-null 
  results (i.e. "changing the past")
"""


def index(request):
    """
    Index view. If user is authenticated show the list of sports, 
    tournaments, etc. Otherwise show login/register buttons.
    """
    if request.user.is_authenticated():
        sports = Sport.objects.all()
        tournaments = Tournament.objects.all()
        #groups = Group.objects.all() 
        return render_to_response("home_authorised.html", locals(), context_instance=RequestContext(request))
    else:
        return render_to_response("home_unauthorised.html", locals(), context_instance=RequestContext(request))


@login_required
def sports(request, sport_id=None):
    """
    List all sports. If an id is specified, list the tournaments for that sport.
    """
    if sport_id:
        try:
            sport = Sport.objects.get(pk=sport_id)
        except ObjectDoesNotExist:
            # TODO: i18!
            return HttpResponse('Sport %s does not exist. <br><a href="/tournaments">View Tournaments</a>'
                    '<br><a href="/sports">View Sports</a>' % sport_id)
        tournaments = Tournament.objects.filter(sport=sport_id)
        return render_to_response("sport.html", locals(), context_instance=RequestContext(request))
    else:
        sports = Sport.objects.all()
        return render_to_response("sports.html", locals(), context_instance=RequestContext(request))

@login_required
def tournaments(request):
    try:
        sport_id = request.GET["sport_id"]
        sport = Sport.objects.get(pk=sport_id)
        title = "%s Tournaments" % sport.name
        tournaments = Tournament.objects.filter(sport=sport_id)
    except MultiValueDictKeyError:
        tournaments = Tournament.objects.all()
        title = "All Tournaments"
    except ObjectDoesNotExist:
        # TODO: i18!
        return HttpResponse('Sport %s does not exist. <br><a href="/tournaments">View Tournaments</a>'
                            '<br><a href="/sports">View Sports</a>' % sport_id)
        tournaments = Tournament.objects.all()
        title = "All Tournaments"
    return render_to_response("tournaments.html", locals(), context_instance=RequestContext(request))


@login_required
def view_fixtures(request, tournament_id, user_id=None):
    # XXX: All of the following is very inefficient (hurriedly implemented to get things finished in
    # time for wc2010). I've begun work on a replacement view that uses joins instead of making 
    # queries within loops; will merge in once its finished.

    if user_id:
        user = User.objects.get(id=user_id)
    else:
        user = request.user


    now = datetime.datetime.now()  # TODO: Allow pardon of 1 minute maybe?
    if request.method == "POST":
        if user_id:
            raise PermissionDenied("Not allowed POST to this URL")
        # extract the pertinent POST values (i.e. those with numeric keys)
        predictions_req = dict([(k,v) for k,v in request.POST.items() if str(k).isdigit()])
        for fixture_id, result_type_id in predictions_req.items():
            try:
                fixture = Fixture.objects.get(pk=fixture_id)
            except ObjectDoesNotExist:
                # No such fixture
                continue
            
            if now > fixture.date:
                # Not allowed to update anymore
                continue
            
            try:
                result_type = ResultType.objects.get(pk=result_type_id)
            except ObjectDoesNotExist:
                # No such result type.
                continue

            
            # TODO: add a create_or_update() method for Prediction (i.e. PUT) 
            # (this kind of idiom must exist in django already surely?)
            try:
                # update if prediction exists already. TODO: Perhaps add a unique constraint on (user, prediction)
                prediction = Prediction.objects.filter(user=user).get(fixture=fixture)
                prediction.result = result_type
                prediction.save()
            except ObjectDoesNotExist:
                # prediction doesn't exist, lets add it
                prediction = Prediction(user=user, fixture=fixture, result=result_type)
                # FIXME: This is quite inefficient. Generate a comma-separated insert query instead. 
                prediction.save() 
        return redirect(request.get_full_path())
    
    
    all_result_types = ResultType.objects.all()  # TODO: error handling if no result types found?
    knockout_result_types = ResultType.objects.filter(Q(pk=1) | Q(pk=2))   # FIXME: hack (hard-coded values)

    # TODO: move this above the POST block?
    try:
        tournament = Tournament.objects.get(pk=tournament_id)
    except ObjectDoesNotExist:
        return HttpResponse('Tournament %s does not exist. <a href="/tournaments">View Tournaments</a>' % tournament_id)

    fixtures = Fixture.objects.filter(tournament=tournament_id).order_by("-date")
    # FIXME: This is pretty poor.. should really use a single SQL query to retrieve this data
    games = []  # this array stores dicts containing a fixture, prediction, is_disabled bool val, and 
    for fixture in fixtures:
        try:
            prediction = Prediction.objects.filter(fixture=fixture.id).get(user=user)
        except ObjectDoesNotExist:
            prediction = None
        
        is_disabled = False    
        if now > fixture.date or fixture.result:
            is_disabled = True
            
        if fixture.fixture_type.is_drawable:
            result_types = all_result_types
        else:
            result_types = knockout_result_types
        games.append({"fixture":fixture,
                      "prediction":prediction,
                      "is_disabled":is_disabled,
                      "result_types":result_types  # FIXME: inefficient
                      })
    
    c = csrf(request)
    c.update(locals())
    return render_to_response("fixtures.html", c, context_instance=RequestContext(request))


@login_required
def view_table(request, tournament_id):

    try:
        tournament_id = int(tournament_id)
    except ValuError:
        return HttpResponse("Tournament '%s' is an invalid tournament." % tournament_id)
    
    # Make sure that we are dealing with a valid tournament
    try:
        tournament = Tournament.objects.get(pk=tournament_id)
    except ObjectDoesNotExist:
        return HttpResponse('Tournament "%s" does not exist. <a href="/tournaments">View Tournaments</a>' % tournament_id)

    cache_key = request.path
    logger.info('cache_key=%s' % cache_key)
    users_and_points = cache.get(cache_key)


    is_cached = True
    if not users_and_points:
        is_cached = False
        logger.info("Found no cache")
        # FIXME: This is also really slow (~3s on my home computer). Refine.
        
        # We'll store the user and points a in a list, which we'll sort by points at the end (TODO: caching)
        users_and_points = []
        users = User.objects.all()
        
        for user in users:
            # TODO: only get fixtures which are in the past (integrity measure to ensure that only actual "results" are processed)?
            fixtures_and_predictions = Fixture.objects.raw("SELECT f.id, f.fixture_type_id, p.result_id as prediction_id, f.result_id as result_id "
                                                            "FROM predictions AS p LEFT JOIN fixtures AS f ON p.fixture_id=f.id "
                                                            "WHERE f.tournament_id=%s AND user_id=%s ", (tournament_id, user.id))
            if not list(fixtures_and_predictions):
                continue 

            # Initialise the user with zero points
            uap = {
              "user":user, 
              "username":user.username,
              "played":len(list(fixtures_and_predictions)),
              "correct_wins":0,
              "semicorrect_wins":0,
              "incorrect_wins":0,
              "correct_draws":0,
              "incorrect_draws":0,
              "points":0
            }
        
            # Iterate over the fixtures_and_predictions, checking if the user guessed correctly
            for fap in fixtures_and_predictions:
                try:
                    # TODO: cache this! 
                    # TODO: get by sport id (yet to be implemented).
                    fixture_type = FixtureType.objects.get(pk=fap.fixture_type_id) 
                except ObjectDoesNotExist:
                    return HttpResponse("ERROR: failed to generate league table. No such fixture type '%s'" % fap.fixture_type_id)
                
                # Handle the "win" cases first
                if fap.prediction_id in [1, 2]:
                    if fap.prediction_id == fap.result_id:
                        uap["correct_wins"] += 1
                        uap["points"] += fixture_type.correct_win_points
                    elif fap.result_id == 3:
                        uap["semicorrect_wins"] += 1
                        uap["points"] += fixture_type.semicorrect_win_points
                    else:
                        uap["incorrect_wins"] += 1
                        uap["points"] += fixture_type.incorrect_win_points
                elif fap.prediction_id == 3:
                    if fap.prediction_id == fap.result_id:
                        uap["correct_draws"] += 1
                        uap["points"] += fixture_type.correct_draw_points
                    else:
                        uap["incorrect_draws"] += 1
                        uap["points"] += fixture_type.incorrect_draw_points
                else:
                    return HttpResponse("ERROR: Invalid prediction '%s' for user '%s'" % (fap.prediction_id, user))

            users_and_points.append(uap)
        
        # Sort the users_and_points list by points
        users_and_points.sort(key=lambda x: x['username'].lower())
        users_and_points.sort(key=lambda x: x['points'], reverse=True)
        
        cache.set(cache_key, users_and_points)
        
    

    return render_to_response("table.html", locals(), context_instance=RequestContext(request))

