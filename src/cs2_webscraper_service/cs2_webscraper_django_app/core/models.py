import uuid
from django.db import models
from django.conf import settings


class Team(models.Model):
    '''
    CS2 Professional teams
    '''
    team_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    pandascore_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=True, unique=True)
    hltv_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Tournament(models.Model):
    '''
    CS2 tournaments/events
    '''
    class Source(models.TextChoices):
        UNSPECIFIED = "unspecified", "Unspecified"
        HLTV = "hltv", "HLTV"
        PANDASCORE = "pandascore", "Pandascore"
    
    tournament_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    organizer = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    prize_pool = models.FloatField()
    online = models.BooleanField()
    source = models.CharField("Source", max_length=20, choices = Source.choices, default=Source.UNSPECIFIED)
    external_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=True, unique=True)
    scraped_at = models.DateTimeField(auto_now=True)


# Create your models here.
class Match(models.Model):
    '''
    CS2 match between two teams
    '''
    class Source(models.TextChoices):
        UNSPECIFIED = "unspecified", "Unspecified"
        HLTV = "hltv", "HLTV"
        PANDASCORE = "pandascore", "Pandascore"

    class BestOf(models.TextChoices):
        BO1 = "bo1", "Best of 1"
        BO3 = "bo3", "Best of 3"
        BO5 = "bo5", "Best of 5"

    match_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.CharField("Source", max_length=20, choices = Source.choices, default=Source.UNSPECIFIED)
    source_match_id = models.CharField(max_length=100)  # ID from the source (HLTV/PandaScore)
    
    team1_id = models.ForeignKey(
       Team,
       on_delete=models.CASCADE,
       related_name='matches_as_team_1'
    )
    team2_id = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='matches_as_team_2'
    )

    match_date = models.DateTimeField()
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='matches'
    )
    best_of = models.CharField(max_length=5, choices=BestOf.choices, default=BestOf.BO3)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'matches'
        verbose_name_plural = "matches"
        # Prevent dpublitate from same source
        unique_together = [['source', 'source_match_id']]
    
    def __str__(self):
        return f"{self.team1} vs {self.team2} ({self.match_date.date()})"


class Result(models.Model):
    """
    Result of a completed match
    """
    class Source(models.TextChoices):
        UNSPECIFIED = "unspecified", "Unspecified"
        HLTV = "hltv", "HLTV"
        PANDASCORE = "pandascore", "PandaScore"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.OneToOneField(
        Match,
        on_delete=models.CASCADE,
        related_name='result'
    )
    
    team1_score = models.PositiveIntegerField()  # Maps won by team1
    team2_score = models.PositiveIntegerField()  # Maps won by team2
    
    winner = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='wins'
    )
    
    # Detailed map-by-map results as JSON
    # Example: [{"map": "de_dust2", "team1_score": 16, "team2_score": 12}, ...]
    map_results = models.JSONField(default=list, blank=True)
    
    completed_at = models.DateTimeField()
    source = models.CharField(max_length=20, choices=Source.choices, default=Source.UNSPECIFIED)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'results'

    def __str__(self):
        return f"{self.match}: {self.team1_score}-{self.team2_score}"


class TeamRanking(models.Model):
    """
    Historical team rankings from various sources
    """
    class Source(models.TextChoices):
        HLTV_WORLD = "hltv_world", "HLTV World Ranking"
        VRS_WORLD = "vrs_world", "VRS World Ranking"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='rankings'
    )
    
    ranking = models.PositiveIntegerField()
    points = models.FloatField(null=True, blank=True)
    source = models.CharField(max_length=20, choices=Source.choices)
    
    retrieved_at = models.DateTimeField()  # When this ranking was captured
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'team_rankings'
        # One ranking per team per source per date
        unique_together = [['team', 'source', 'retrieved_at']]
        ordering = ['-retrieved_at', 'ranking']

    def __str__(self):
        return f"{self.team} - #{self.ranking} ({self.source})"