from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from nba_stats.models import *


class PlayerForm(forms.ModelForm):
	class Meta:
		model = Player
		fields = '__all__'
		# season = forms.ModelMultipleChoiceField(queryset=Player.objects.all())

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'submit'))


class TeamForm(forms.ModelForm):
	class Meta:
		model = Team
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'submit'))