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


class TeamTmpSerializer(serializers.ModelSerializer):

	class Meta:
		model = Team
		fields = ('team_id', 'team_name')

class SeasonTmpSerializer(serializers.ModelSerializer):

	class Meta:
		model = Season
		fields = ('season_id', 'season_year')


class PlayerTmpSerializer(serializers.ModelSerializer):

	class Meta:
		model = Player
		fields = ('player_id', 'player_name')

class SeasonPlayerSerializer(serializers.ModelSerializer):
	# player = PlayerTmpSerializer(many=False, read_only=True)
	# team = TeamSerializer(many=False, read_only=True)
	# season = SeasonSerializer(many=False, read_only=True)
	player_id = serializers.ReadOnlyField(source='player.player_id')
	team_id = serializers.ReadOnlyField(source='team.team_id')
	season_id = serializers.ReadOnlyField(source='season.season_id')

	# print(player_id, team_id, season_id)
	class Meta:
		model = SeasonPlayer
		fields = ('season_player_id', 'player', 'team', 'season', 
					'player_age', 'player_games','player_minutes', 'player_per', 'player_ts', 'player_ows',
					'player_dws', 'player_ws', 'player_ws_per', 'player_fg', 'player_fgp', 'player_three_fg', 'player_three_fgp', 
					'player_trb', 'player_ast', 'player_stl', 'player_blk', 'player_tov', 'player_pf', 'player_pts')



class PlayerSerializer(serializers.ModelSerializer):
	player_birth_state = StateCountrySerializer(many=False, read_only=True)
	player_birth_state_id = serializers.PrimaryKeyRelatedField(
		allow_null=False,
		many=False,
		write_only=True,
		queryset=StateCountry.objects.all(),
		source='player_birth_state'
	)
	player_college = CollegeSerializer(many=False, read_only=True)	
	player_college_id = serializers.PrimaryKeyRelatedField(
		allow_null=False,
		many=False,
		write_only=True,
		queryset=College.objects.all(),
		source='player_college'
	)
	team = TeamTmpSerializer(many=True, read_only=True)	
	team_id = serializers.PrimaryKeyRelatedField(
		allow_null=False,
		many=True,
		write_only=True,
		queryset=Team.objects.all(),
		source='team'
	)
	season = SeasonTmpSerializer(many=True, read_only=True)	
	season_id = serializers.PrimaryKeyRelatedField(
		allow_null=False,
		many=True,
		write_only=True,
		queryset=Season.objects.all(),
		source='season'	
	)
	# season_player = SeasonPlayerSerializer(
	# 	source='season_player_set', # Note use of _set
	# 	many=True,
	# 	read_only=True
	# )
	# season_player_ids = serializers.PrimaryKeyRelatedField(
	# 	many=True,
	# 	write_only=True,
	# 	queryset=SeasonPlayer.objects.all(),
	# 	source='season_player'
	# )

	class Meta:
		model = Player
		fields = ('player_id', 'player_name', 'player_height', 'player_weight', 'player_birth_year', 
					'player_birth_state','player_birth_state_id','player_college', 'player_college_id',  'team','team_id', 'season','season_id')
	# class Meta:
	# 	model = Player
	# 	fields = ('player_id', 'player_name', 'player_height', 'player_weight', 'player_birth_year', 
	# 				'player_birth_state','player_birth_state_id','player_college', 'player_college_id', 'team_display', 'season_display', 'season_player','season_player_ids')



	def create(self, validated_data):

		print(validated_data)

		team = list(validated_data.pop('team'))
		season = list(validated_data.pop('season'))
		print("*" * 50)
		print(team[0])
		print("*" * 50)
		print(season[0])

		player = Player.objects.create(
			player_name = validated_data.pop('player_name'),
			player_height = validated_data.pop('player_height'),
			player_weight = validated_data.pop('player_weight'),
			player_birth_year = validated_data.pop('player_birth_year'),
			player_birth_state = validated_data.pop('player_birth_state'),
			player_college =validated_data.pop('player_college'),
			)

		#  to add Season_Player table, here we need to ensure that length of the team and season should be equal
		if len(team) == len(season):
			for i in range(len(team)):
				SeasonPlayer.objects.create(
					player_id = player.player_id,
					season_id=season[i].season_id, 
					team_id=team[i].team_id
				)

		# m = Player.objects.values_list('team', flat=True).filter(player_id = 4140)
		# print("#" *50)
		# print(m)
		return player


	def update(self, instance, validated_data):
		# site_id = validated_data.pop('heritage_site_id')
		print(validated_data)
		print(instance)
		# new_countries = validated_data.pop('heritage_site_jurisdiction')

		instance.player_name = validated_data.get(
			'player_name',
			instance.player_name
		)
		instance.player_height = validated_data.get(
			'player_height',
			instance.player_height
		)
		instance.player_weight = validated_data.get(
			'player_weight',
			instance.player_weight
		)
		instance.player_birth_year = validated_data.get(
			'player_birth_year',
			instance.player_birth_year
		)
		instance.player_birth_state = validated_data.get(
			'player_birth_state',
			instance.player_birth_state
		)		
		instance.player_college = validated_data.get(
			'player_college',
			instance.player_college
		)
		instance.save()

		# handle the SeasonPlayer table.
		# notice the order input. Although for display, it may just display in ascending order (which is find). 
		# But need to correct insert into Season Player by input order


		# First get the value list. it's a list of list.
		old_ids = list(SeasonPlayer.objects\
							.values_list('team_id', 'season_id')\
							.filter(player_id = instance.player_id)\
							.order_by('season_player_id'))
		new_ids = []
		team = list(validated_data.pop('team'))
		season = list(validated_data.pop('season'))
		print(team, len(team))
		if len(team) == len(season):
			for i in range(len(team)):
				tmp = (team[i].team_id, season[i].season_id)
				new_ids.append(tmp)
		else:
			return instance

		print(new_ids)
		print(old_ids)
		# compare new_ids and old_ids
		# to insert
		print("#" * 50)
		for i in new_ids:
			if i not in old_ids:
				# i[0] for team, i[1] for season
				print("case1: ", i[0], i[1])
				SeasonPlayer.objects.create(
					player_id = instance.player_id,
					season_id=i[1], 
					team_id=i[0]
				)


		# to delete
		for i in old_ids:
			if i not in new_ids:
				SeasonPlayer.objects\
				.filter(player_id = instance.player_id,
					season_id=i[1], 
					team_id=i[0])\
				.delete()


		return instance
