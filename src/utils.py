#!/usr/bin/env python

"""Miscellaneous utils for sportsbrackets.

Created by Caoilte Guiry.

"""

import os
import sys
import random
import string
import datetime
import math

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from home.models import Tournament, Sport, ResultType, FixtureType, Fixture, \
Venue, Sport, Team, Prediction

__author__ = "Caoilte Guiry"
__version__ = "0.0.1"


class Error(Exception):
    """
    Custom Error type for utils.
    """
    pass


def get_random_words(dict_file="/usr/share/dict/words", num_words=1):
    """
    Get some random words.

    First we try a dictionary file, failing that we generate some made up
    words.

    @param string dict_file     path to FS dictionary file
    @param int    num_words     number of words which will be returned
    """
    words = []
    # Try to get some real words first, just for fun
    try:
        # Too many levels of indentation, consider refactoring
        filesize = os.stat(dict_file).st_size
        # seek() to random parts of the file, and pull down a line.
        with open(dict_file, "r") as fh:
            found_count = 0
            while found_count < num_words:
                fh.seek(random.randint(0, filesize - 1))
                # Clear the first line, since it may not be guaranteed to be
                # a full line. Arguably wasteful, but better than reading the
                # whole dictionary into memory.
                fh.readline()
                word = fh.readline().strip()
                # Just incase, we seek()'d to the end verify we got a word
                if word and word.isalpha():
                    words.append(word)
                    found_count += 1
    except (OSError, IOError):
        # Problem stat'ing or open'ing the file. Lets make up some fake words
        words = [''.join(random.choice(string.ascii_lowercase)
                         for x in range(random.randint(3, 10)))
                         for i in range(num_words)]
    return words


def date_range(begin_date, end_date):
    """
    Generator for date ranges.

    @param date begin_date start of date range
    @param date end_date   end of date range
    """
    for n in xrange((end_date - begin_date).days):
        yield begin_date + datetime.timedelta(n)


def create_test_tournament(duration=14):
    """
    Create a test tournament.

    @param int duration tournament duration in days.
    """
    # Get between 1-5 random words using the get_random_words function. Map
    # this to str.title and join() with spaces.
    tournament_name = "%s Tournament" % " ".join(map(str.title,
                      get_random_words(num_words=random.randint(1, 5))))

    random_sport = get_random_sport()

    # basic enough approach here... tourney is either about to start or end
    days_passed = random.randint(0, duration)
    days_left = duration - days_passed
    today = datetime.datetime.now()
    begin_date = today - datetime.timedelta(days=days_passed)
    end_date = today + datetime.timedelta(days=days_left)

    t = Tournament(name=tournament_name, begin_date=begin_date,
                   end_date=end_date, sport=random_sport)
    t.save()
    return t


def get_random_sport():
    """
    Get a random sport. Create one if it doesn't exist.
    """
    sport_count = Sport.objects.count()
    try:
        random_sport = Sport.objects.all()[random.randint(0, sport_count - 1)]
    except IndexError:
        # No sports in the database. Add one.
        random_sport = Sport(name=get_random_words(num_words=1)[0].title)
        random_sport.save()
    return random_sport


def get_random_venue():
    """
    Get a random venue. Raise an Error if one can't be found.
    """
    venue_count = Venue.objects.count()
    try:
        return Venue.objects.all()[random.randint(0, venue_count - 1)]
    except IndexError:
        # cba creating all the dependencies automatically (TODO)
        raise Error("Create at least one venue before proceeding")


def get_random_team():
    """
    Get a random team. Raise an Error if one can't be found.
    """
    team_count = Team.objects.count()
    try:
        return Team.objects.all()[random.randint(0, team_count - 1)]
    except IndexError:
        # cba creating all the dependencies automatically (TODO)
        # TODO: should probably in fact be a few teams :-)
        raise Error("Create at least one team before proceeding")


def generate_test_data(num_users=15, num_tournaments=1,
                       fixtures_lower_limit=40, fixtures_upper_limit=60):
    """
    Populate the database with test data.

    @peram int num_users            number of users to create
    @param int num_tournaments      number of tournaments to create
    @param int fixtures_lower_limit least number of fixtures that will be
                                    created per tournmanet
    @param int fixtures_upper_limit most number of fixtures that will be
                                    created per tournmanet
    """
    # Verify the user wants to proceed, so nobody pollutes a valuable database
    # with junk data
    ans = raw_input("Are you sure you want to proceed? Do not run on a "
                    " production database or a database with valuable data! "
                    "[yes/no]")
    if ans.lower() != "yes":
        return

    # Lets get some prerequisites out of the way.
    # For the sake of simplicity, all generates fixtures will be group games.
    # We also need the three result types...
    # Lets ensure these exist. No exception handling here, let them fail
    # if necessary
    group_match = FixtureType.objects.get(name="Group")
    t1_win = ResultType.objects.get(name='Team 1 Win')
    t2_win = ResultType.objects.get(name='Team 2 Win')
    draw = ResultType.objects.get(name='Draw')

    # Quick check to see if we have venues and teams
    get_random_team()
    get_random_venue()

    # Okay, all set. Lets create some users...
    users = []
    for i in xrange(num_users):
        username = "test_user_%s" % i
        email = "%s@sbrackets.com" % username
        # Check if the user already exists (from previous
        # generate_test_data() calls)
        try:
            user = User.objects.filter(username=username).get(email=email)
        except ObjectDoesNotExist:
            # user doesn't exist yet, lets create one.
            sys.stdout.write("Creating test user %s\n" % username)
            # password 'a' will not be actually used, will call
            # set_unusuable_password() below
            user = User.objects.create_user(username, email, 'a')
            user.set_unusable_password()
        users.append(user)

    # Create some test tournaments
    for i in xrange(num_tournaments):
        t = create_test_tournament(14)
        sys.stdout.write("Created tournament %s\n" % t)
        fixtures_count = random.randint(fixtures_lower_limit,
                                        fixtures_upper_limit)
        # Pretty lazy approach here... oh well. Get the ceil of float division
        # of the fixtures_count by the tourney duration to get the number of
        # fixtures_per_day. Flaws:
        # * not guaranteed to run till the end
        # * won't work if there are more days than fixtures.
        fixtures_per_day = math.ceil(fixtures_count /
                                     float((t.end_date - t.begin_date).days))

        for fdate in date_range(t.begin_date, t.end_date):
            if fdate < datetime.datetime.now():
                actual_result = random.choice((t1_win, t2_win, draw))
            else:
                actual_result = None

            fixture = Fixture(date=fdate, venue=get_random_venue(),
                              team1=get_random_team(), team2=get_random_team(),
                              fixture_type=group_match,
                              tournament=t, result=actual_result
            )
            fixture.save()
            sys.stdout.write("Created fixture %s\n" % fixture)

            for user in users:
                pred_result = random.choice((t1_win, t2_win, draw))
                prediction = Prediction(user=user, fixture=fixture,
                                        result=pred_result)
                prediction.save()
                sys.stdout.write("Created prediction for user %s "
                                 "and fixture %s\n" % (user, fixture))
