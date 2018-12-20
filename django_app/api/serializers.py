from nba_stats.models import *
from rest_framework import response, serializers, status

class CollegeSerializer(serializers.ModelSerializer):

	class Meta:
		model = College
		fields = ('college_id', 'college_name')

class StateCountrySerializer(serializers.ModelSerializer):

	class Meta:
		model = StateCountry
		fields = ('state_country_id', 'state_country_name')

class SeasonSerializer(serializers.ModelSerializer):

	class Meta:
		model = Season
		fields = ('season_id', 'season_year', 'season_game')

class TeamSerializer(serializers.ModelSerializer):
	season = SeasonSerializer(many=True, read_only=True)

	class Meta:
		model = Team
		fields = ('team_id', 'team_name', 'season')


class PlayerSerializer(serializers.ModelSerializer):
	player_birth_state = StateCountrySerializer(many=False, read_only=True)
	player_college = CollegeSerializer(many=False, read_only=True)	
	# team = TeamSerializer( many=True, read_only=True)
	# season = SeasonSerializer(many=True, read_only=True)

	class Meta:
		model = Player
		fields = ('player_id', 'player_name', 'player_height', 'player_weight', 'player_birth_year', 
					'player_birth_state', 'player_college','team_display', 'season_display')


class SeasonPlayerSerializer(serializers.ModelSerializer):

	player = PlayerSerializer(many=False, read_only=True)
	team = TeamSerializer(many=False, read_only=True)
	season = TeamSerializer(many=False, read_only=True)
	class Meta:
		model = SeasonPlayer
		fields = ('season_player_id', 'player', 'team', 'season', 
					'player_age', 'player_games','player_minutes', 'player_per', 'player_ts', 'player_ows',
					'player_dws', 'player_ws', 'player_ws_per', 'player_fg', 'player_fgp', 'player_three_fg', 'player_three_fgp', 
					'player_trb', 'player_ast', 'player_stl', 'player_blk', 'player_tov', 'player_pf', 'player_pts')




	def create(self, validated_data):

		print(validated_data)

		player = Player.objects.create(**validated_data)

		# if countries is not None:
		# 	for country in countries:
		# 		HeritageSiteJurisdiction.objects.create(
		# 			heritage_site_id=site.heritage_site_id,
		# 			country_area_id=country.country_area_id
		# 		)
		return player


	def update(self, instance, validated_data):
		# site_id = validated_data.pop('heritage_site_id')
		team_id = instance.team_id
		# new_countries = validated_data.pop('heritage_site_jurisdiction')

		instance.player_name = validated_data.get(
			'player_name',
			instance.player_name
		)

		instance.save()

		# # If any existing country/areas are not in updated list, delete them
		# new_ids = []
		# old_ids = HeritageSiteJurisdiction.objects \
		# 	.values_list('country_area_id', flat=True) \
		# 	.filter(heritage_site_id__exact=site_id)

		# # TODO Insert may not be required (Just return instance)

		# # Insert new unmatched country entries
		# for country in new_countries:
		# 	new_id = country.country_area_id
		# 	new_ids.append(new_id)
		# 	if new_id in old_ids:
		# 		continue
		# 	else:
		# 		HeritageSiteJurisdiction.objects \
		# 			.create(heritage_site_id=site_id, country_area_id=new_id)

		# # Delete old unmatched country entries
		# for old_id in old_ids:
		# 	if old_id in new_ids:
		# 		continue
		# 	else:
		# 		HeritageSiteJurisdiction.objects \
		# 			.filter(heritage_site_id=site_id, country_area_id=old_id) \
		# 			.delete()

		return instance

