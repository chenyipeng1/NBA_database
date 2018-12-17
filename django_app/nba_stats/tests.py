from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from .models import *


class IndexViewTest(TestCase):

	def test_view_route_redirection(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 302)


class HomeViewTest(TestCase):

	def test_view_route(self):
		response = self.client.get('/nba_stats/')
		self.assertEqual(response.status_code, 200)

	def test_view_route_name(self):
		response = self.client.get(reverse('home'))
		self.assertEqual(response.status_code, 200)

	def test_view_template(self):
		response = self.client.get(reverse('home'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'nba_stats/home.html')


class AboutViewTest(TestCase):

	def test_view_route(self):
		response = self.client.get('/nba_stats/about/')
		self.assertEqual(response.status_code, 200)

	def test_view_route_fail(self):
		response = self.client.get('/about/')
		self.assertEqual(response.status_code, 404)

	def test_view_route_name(self):
		response = self.client.get(reverse('about'))
		self.assertEqual(response.status_code, 200)

	def test_view_template(self):
		response = self.client.get(reverse('about'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'nba_stats/about.html')


class SiteModelTest(TestCase):

	def setUp(self):
		College.objects.create(college_name='Cultural')
		category = College.objects.get(pk=1)
	# 	College.objects.create(
	# 		# TODO restore missing properties and values
	# 		college_name='Cultural Landscape and Archaeological Remains of the Bamiyan Valley')

	# def test_site_name(self):
	# 	t = Player.objects.get(pk=1)
		# expected_object_name = f'{player.player_name}'
		# # aa = f'{site.heritage_site_category_id}'
		# self.assertEqual(expected_object_name, 'aaa')


class SiteListViewTest(TestCase):

	def test_view_route(self):
		response = self.client.get('/nba_stats/players/')
		self.assertEqual(response.status_code, 200)

	def test_view_route_fail(self):
		response = self.client.get('/players/')
		self.assertEqual(response.status_code, 404)

	def test_view_route_name(self):
		response = self.client.get(reverse('players'))
		self.assertEqual(response.status_code, 200)

	def test_view_template(self):
		response = self.client.get(reverse('players'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'nba_stats/player.html')