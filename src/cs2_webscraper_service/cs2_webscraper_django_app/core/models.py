from django.db import models
from django.conf import settings

# Create your models here.
class Match(models.Model):
    '''
    match_id = uuid (primary key)
    source = ENUM(hltv, pandascore)
    source_match_id = string
    team1_id = uuid (foreign key to teams)
    team2_id uuid (foreign key to teams)
    match_date = timestamp
    tournament_id = uuid (foreign key to tournaments)
    best_of = ENUM(b01, b03, b05)
    created_at = timestamp
    updated_at = timestamp
    '''
    class Source(models.TextChoices):
        UNSPECIFIED = "unspecified", "Unspecified"
        HLTV = "hltv", "HLTV"
        PANDASCORE = "pandascore", "Pandascore"

    source = models.CharField("Source", max_length=10, choices = Source.choices, default=Source.UNSPECIFIED)
    team1_id = models.

    pass

class Result(models.Model):
    f'''
    result_id = uuid (primary key)
    match_id = foreign key to matches
    team1_score = integer (num maps won)
    team2_score = integer (num maps won)
    winner_id = uuid (foreign key to teams)
    map_results = JSON
    completed_at = timestamp
    source = ENUM (hltv, pandascore)
    created_at = timestamp
    '''
    pass

class Team(models.Model):
    '''
    team_id = uuid (primary key)
    name = string
    country = string
    pandascore_id = uuid
    hltv_id = uuid
    created_at = timestamp
    '''
    pass

class Tournament(models.Model):
    '''
    tournament_id = uuid (primary key)
    name = text
    organizer = text
    region = text
    start_date = DATE
    end_date = DATE
    prize_pool = NUMERIC
    online = BOOLEAN
    source = ENUM(hltv, pandascore)
    external_id = uuid
    scraped_at = timestamp
    '''
    pass

class TeamRanking(models.Model):
    '''
    ranking_id = uuid (primary key)
    team_id = foreign key (to tournaments table)
    ranking = INT
    points = FLOAT
    source = ENUM(HLTV_WORLD, VRS_WORLD)
    retrieved_at = TIMESTAMP
    '''
    pass