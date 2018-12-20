import django_filters
from nba_stats.models import *


class PlayerFilter(django_filters.FilterSet):
	player_name = django_filters.CharFilter(
		field_name='player_name',
		label='Player Name',
		lookup_expr='icontains'
	)

	player_height = django_filters.NumberFilter(
		field_name='player_height',
		label='Player Height',
		lookup_expr='icontains'
	)

	player_weight = django_filters.NumberFilter(
		field_name='player_weight',
		label='Player Weight',
		lookup_expr='icontains'
	)	
	
	player_birth_year = django_filters.NumberFilter(
		field_name='player_birth_year',
		label='Player Birth Year',
		lookup_expr='icontains'
	)

	player_birth_state = django_filters.ModelChoiceFilter(
		field_name='player_birth_state',
		label='Player Birth State/Country',
		queryset = StateCountry.objects.all(),
		lookup_expr='exact'
	)

	player_college = django_filters.ModelChoiceFilter(
		field_name='player_college',
		label='Player College',
		queryset = College.objects.all(),
		lookup_expr='exact'
	)


	team = django_filters.ModelChoiceFilter(
		field_name='team',
		label='Team',
		queryset=Team.objects.all(),
		lookup_expr='exact'
	)

	season = django_filters.ModelChoiceFilter(
		field_name='season',
		label='Season',
		queryset=Season.objects.all().order_by('season_year'),
		lookup_expr='exact'
	)

	class Meta:
		model = Player
		# form = SearchForm
		# fields [] is required, even if empty.
		fields = []