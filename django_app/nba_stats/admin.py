from django.contrib import admin
import nba_stats.models as models

@admin.register(models.College)
class CollegeAdmin(admin.ModelAdmin):
	fields = [
		'college_name'
	]

	list_display = [
		'college_name'
	]

	ordering = [
		'college_name'
	]


@admin.register(models.StateCountry)
class StateCountryAdmin(admin.ModelAdmin):
	fields = [
		'state_country_name'
	]

	list_display = [
		'state_country_name'
	]

	ordering = [
		'state_country_name'
	]


@admin.register(models.Season)
class SeasonAdmin(admin.ModelAdmin):
	fields = [
		'season_year',
		'season_game'
	]

	list_display = [
		'season_year',
		'season_game'
	]

	ordering = [
		'season_year'
	]


@admin.register(models.Player)
class PlayerAdmin(admin.ModelAdmin):
	fields = [
		'player_name',
		'player_height',
		'player_weight',
		'player_birth_year',
		'player_birth_state',
		'player_college'
	]

	list_display = [
		'player_name',
		'player_height',
		'player_weight',
		'player_birth_year',
		'player_birth_state',
		'player_college',
		'team_display',
		'season_display'
	]

	ordering = [
		'player_name'
	]


@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
	fields = [
		'team_name',
	]

	list_display = [
		'team_name',
		'season_display'
	]

	ordering = [
		'team_name'
	]

@admin.register(models.SeasonPlayer)
class SeasonPlayerAdmin(admin.ModelAdmin):
	fields = [
		'player',
		'season',
		'team',
		'player_age',
		'player_games',
		'player_minutes',
		'player_per',
		'player_ts',
		'player_ows',
		'player_dws',
		'player_ws',
		'player_ws_per',
		'player_fg',
		'player_fgp',
		'player_three_fg',
		'player_three_fgp',
		'player_trb',
		'player_ast',
		'player_stl',
		'player_blk',
		'player_tov',
		'player_pf',		
		'player_pts'
	]

	list_display = [
		'player',
		'season',
		'team',
		'player_age',
		'player_games',
		'player_minutes',
		'player_per',
		'player_ts',
		'player_ows',
		'player_dws',
		'player_ws',
		'player_ws_per',
		'player_fg',
		'player_fgp',
		'player_three_fg',
		'player_three_fgp',
		'player_trb',
		'player_ast',
		'player_stl',
		'player_blk',
		'player_tov',
		'player_pf',		
		'player_pts'
	]

	ordering = [
		'player',
		'season',
		'team'
	]
