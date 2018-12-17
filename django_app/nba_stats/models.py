# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class College(models.Model):
    college_id = models.AutoField(primary_key=True)
    college_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'college'
        ordering = ['college_name']
        verbose_name = 'College Name'
        verbose_name_plural = 'College Name'
    def __str__(self):
        return self.college_name

class StateCountry(models.Model):
    state_country_id = models.AutoField(primary_key=True)
    state_country_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'state_country'
        ordering = ['state_country_name']
        verbose_name = 'State or Country'
        verbose_name_plural = 'State or Country'
    def __str__(self):
        return self.state_country_name



class Season(models.Model):
    season_id = models.AutoField(primary_key=True)
    season_year = models.IntegerField(unique=True)
    season_game = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'season'
        ordering = ['season_year']
        verbose_name = 'Season Year and Season Games'
        verbose_name_plural = 'Season Year and Season Games'
    def __str__(self):
        return str(self.season_year)


class Player(models.Model):
    player_id = models.AutoField(primary_key=True)
    player_name = models.CharField(max_length=255)
    player_height = models.FloatField(blank=True, null=True)
    player_weight = models.FloatField(blank=True, null=True)
    player_birth_year = models.FloatField(blank=True, null=True)
    player_birth_state = models.ForeignKey('StateCountry', models.DO_NOTHING, blank=True, null=True)
    player_college = models.ForeignKey(College, models.DO_NOTHING, blank=True, null=True)
    team = models.ManyToManyField('Team', through='SeasonPlayer', related_name='team_players')
    season = models.ManyToManyField(Season, through='SeasonPlayer', related_name='season_players')


    class Meta:
        managed = False
        db_table = 'player'
        ordering = ['player_name']
        verbose_name = 'Player'
        verbose_name_plural = 'Player'
    def __str__(self):
        return self.player_name
    def team_display(self):
        """Create a string for team. This is required to display in the Admin view."""
        return ', '.join(
            team.team_name for team in self.team.all()[:25])
    def season_display(self):
        """Create a string for season. This is required to display in the Admin view."""
        return ', '.join(
            str(season.season_year) for season in self.season.all()[:25])

    team_display.short_description = 'Team Palyer for'   
    season_display.short_description = 'Season Palyer for'    



class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=255, blank=True, null=True)
    season = models.ManyToManyField(Season, through='SeasonPlayer', related_name='season_teams')

    class Meta:
        managed = False
        db_table = 'team'
        ordering = ['team_name']
        verbose_name = 'Team'
        verbose_name_plural = 'Team'
    def __str__(self):
        return self.team_name
    def season_display(self):
        """Create a string for season. This is required to display in the Admin view."""
        re = ""
        year_list = []
        for season in self.season.all():
            if season.season_year not in year_list:
                year_list.append(season.season_year)
        re = ", ".join(str(i) for i in year_list)
        # return ', '.join(
        #     str(season.season_year) for season in self.season.all())   
        return re

    season_display.short_description = 'Season Team for'  



class SeasonPlayer(models.Model):
    season_player_id = models.AutoField(primary_key=True)
    player = models.ForeignKey(Player, models.DO_NOTHING)
    team = models.ForeignKey(Team, models.DO_NOTHING)
    season = models.ForeignKey(Season, models.DO_NOTHING)
    player_age = models.IntegerField(blank=True, null=True)
    player_games = models.IntegerField(blank=True, null=True)
    player_minutes = models.IntegerField(blank=True, null=True)
    player_per = models.DecimalField(db_column='player_PER', max_digits=10, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    player_ts = models.DecimalField(db_column='player_TS', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    player_ows = models.DecimalField(db_column='player_OWS', max_digits=10, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    player_dws = models.DecimalField(db_column='player_DWS', max_digits=10, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    player_ws = models.DecimalField(db_column='player_WS', max_digits=10, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    player_ws_per = models.DecimalField(db_column='player_WS_per', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    player_fg = models.IntegerField(db_column='player_FG', blank=True, null=True)  # Field name made lowercase.
    player_fgp = models.DecimalField(db_column='player_FGP', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    player_three_fg = models.DecimalField(db_column='player_three_FG', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    player_three_fgp = models.DecimalField(db_column='player_three_FGP', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    player_trb = models.IntegerField(db_column='player_TRB', blank=True, null=True)  # Field name made lowercase.
    player_ast = models.IntegerField(db_column='player_AST', blank=True, null=True)  # Field name made lowercase.
    player_stl = models.IntegerField(db_column='player_STL', blank=True, null=True)  # Field name made lowercase.
    player_blk = models.IntegerField(db_column='player_BLK', blank=True, null=True)  # Field name made lowercase.
    player_tov = models.IntegerField(db_column='player_TOV', blank=True, null=True)  # Field name made lowercase.
    player_pf = models.IntegerField(db_column='player_PF', blank=True, null=True)  # Field name made lowercase.
    player_pts = models.IntegerField(db_column='player_PTS', blank=True, null=True)  # Field name made lowercase.


    class Meta:
        managed = False
        db_table = 'season_player'
        ordering = ['player','team','season']
        verbose_name = 'Performance on Season Player'
        verbose_name_plural = 'Performance on Season Player'
    # do I need 



