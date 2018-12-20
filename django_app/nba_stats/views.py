from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.http import HttpResponseRedirect

from .models import *
from .forms import *
from .filters import *

from django.urls import reverse_lazy
from django.shortcuts import redirect

from django_filters.views import FilterView


def index(request):
   return HttpResponse("You are going to look through NBA history stats database")


class AboutPageView(generic.TemplateView):
	template_name = 'nba_stats/about.html'


class HomePageView(generic.TemplateView):
	template_name = 'nba_stats/home.html'

class PlayerListView(generic.ListView):
	model = Player
	context_object_name = 'players'
	template_name = 'nba_stats/player.html'
	paginate_by = 100

	def get_queryset(self):
		return Player.objects.all().order_by('player_name')

class PlayerDetailView(generic.DetailView):
	model = Player
	context_object_name = 'player'
	template_name = 'nba_stats/player_detail.html'



class TeamListView(generic.ListView):
	model = Team
	context_object_name = 'teams'
	template_name = 'nba_stats/team.html'
	paginate_by = 20

	def get_queryset(self):
		return Team.objects.all().order_by('team_name')

class TeamDetailView(generic.DetailView):
	model = Team
	context_object_name = 'team'
	template_name = 'nba_stats/team_detail.html'


@method_decorator(login_required, name='dispatch')
class PlayerCreateView(generic.View):
	model = Player
	form_class = PlayerForm
	success_message = "Player created successfully"
	template_name = 'nba_stats/player_new.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def post(self, request):
		form = PlayerForm(request.POST)
		# ensure that team and season must have same length
		if form.is_valid():
			player = form.save(commit=False)
			player.save()
			if len(form.cleaned_data['team']) == len(form.cleaned_data['season']):
				for i in range(len(form.cleaned_data['team'])):
					SeasonPlayer.objects.create(player_id=player.player_id, team_id=form.cleaned_data['team'][i].team_id, season_id=form.cleaned_data['season'][i].season_id)
				return redirect(player) # shortcut to object's get_absolute_url()
			# return HttpResponseRedirect(player.get_absolute_url())
		return render(request, 'nba_stats/player_new.html', {'form': form})

	def get(self, request):
		form = PlayerForm()
		return render(request, 'nba_stats/player_new.html', {'form': form})





@method_decorator(login_required, name='dispatch')
class PlayerUpdateView(generic.UpdateView):
	model = Player
	form_class = PlayerForm
	# fields = '__all__' <-- superseded by form_class
	context_object_name = 'player'
	# pk_url_kwarg = 'site_pk'
	success_message = "Player updated successfully"
	template_name = 'nba_stats/player_update.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def form_valid(self, form):
		player = form.save(commit=False)
		player.save()
		if form.is_valid():

			# Current team_id values linked to player
			old_team_ids = list(SeasonPlayer.objects\
							.values_list('team_id', flat=True)\
							.filter(player_id = player.player_id))


			# Current season_id values linked to player
			old_season_ids = list(SeasonPlayer.objects\
							.values_list('season_id', flat=True)\
							.filter(player_id = player.player_id))


			# New team list
			new_teams = form.cleaned_data['team']
			# New season list
			new_seasons = form.cleaned_data['season']

			# New ids
			new_team_ids = []
			new_season_ids = []


			if len(new_teams) == len(new_seasons):
				# Insert new unmatched entries
				for i in range(len(new_teams)):
					new_team_id = new_teams[i].team_id
					new_season_id = new_seasons[i].season_id
					new_team_ids.append(new_team_id)
					new_season_ids.append(new_season_id)


					try:
						if old_team_ids.index(new_team_id) == old_season_ids.index(new_season_id):
							print("num 1", old_team_ids.index(new_team_id),old_season_ids.index(new_season_id))
							# matched
							continue
						else:
							print("num 2", old_team_ids.index(new_team_id),old_season_ids.index(new_season_id))
							SeasonPlayer.objects\
								.create(player_id=player.player_id, season_id=new_season_id, team_id=new_team_id)
					except:
						print("num 3", player.player_id, new_season_id, new_team_id)
						SeasonPlayer.objects\
							.create(player_id=player.player_id, season_id=new_season_id, team_id=new_team_id)					
				# Delete new unmatched entries
				for i in range(len(old_team_ids)):
					try:
						if new_season_ids.index(old_season_ids[i]) == new_team_ids.index(old_team_ids[i]):
							print("num 4", new_season_ids.index(old_season_ids[i]), new_team_ids.index(old_team_ids[i]))
							continue
						else:
							print("num 5", new_season_ids.index(old_season_ids[i]), new_team_ids.index(old_team_ids[i]))
							# SeasonPlayer.objects\
							# 	.filter(player_id=player.player_id, season_id=new_season_id, team_id=new_team_id) \
							# 	.delete()
					except:
						print("num 6", player.player_id, new_season_id, new_team_id)
						SeasonPlayer.objects\
							.filter(player_id=player.player_id, season_id=old_season_ids[i], team_id=old_team_ids[i]) \
							.delete()

				# One problem, team and season can only be one to one here. Sucks.

		return HttpResponseRedirect(player.get_absolute_url())




@method_decorator(login_required, name='dispatch')
class PlayerDeleteView(generic.DeleteView):
	model = Player
	success_message = "Player deleted successfully"
	success_url = reverse_lazy('players')
	context_object_name = 'player'
	template_name = 'nba_stats/player_delete.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()

		# Delete SeasonPlayer entries
		SeasonPlayer.objects \
			.filter(player_id=self.object.player_id)\
			.delete()

		self.object.delete()

		return HttpResponseRedirect(self.get_success_url())
		# return HttpResponseRedirect(self.object.get_absolute_url())


class PlayerFilterView(FilterView):
	filterset_class = PlayerFilter
	template_name = 'nba_stats/players_filter.html'
