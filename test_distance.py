from django.contrib.gis.geos import Point, Polygon, GEOSGeometry
import requests
import pytest
import json
from django.test import TestCase

API_URL = "http://127.0.0.1:8000/api/buildings/"

class MyTestForDistance(TestCase):
    def setUp(self):
        self.test_list_buildings=self.get_list_buildings()

    def get_list_buildings(self):
        res = requests.get(API_URL + '')
        assert res.status_code == 200
        return res.json()

    def test_distance_filter_with_valid_arguments(self):
        # Тестирование фильтра расстояния с корректными аргументами
        res = requests.get(API_URL + '?dist={0}&&point={1},{2}'.format(5, 5, 5))

        assert res.status_code == 200
        data = res.json()
        assert data == self.test_list_buildings

    def test_distance_filter_with_invalid_arguments(self):
        # Тестирование фильтра расстояния с некорректными аргументами
        res = requests.get(API_URL + '??dist=&point={0},{1}'.format(5, 5))
        assert res.status_code == 200
        data = res.json()
        assert data == self.test_list_buildings

    def test_distance_filter_without_arguments(self):
        # Тестирование фильтра расстояния без аргументов
        res = requests.get(API_URL + '')
        assert res.status_code == 200
        data = res.json()
        assert data == self.test_list_buildings

    def test_invalid_api_url(self):
        # Тестирование некорректного API URL
        invalid_url = "http://127.0.0.1:8000/api/invalid_url/"
        res = requests.get(invalid_url)
        assert res.status_code == 404

    def test_default_point_argument(self):
        # Тестирование использования дефолтной точки при отсутствии аргумента "point"
        res = requests.get(API_URL + '?dist={}'.format(5))
        assert res.status_code == 200

    def test_missing_dist_argument(self):
        # Тестирование отсутствия аргумента "dist"
        res = requests.get(API_URL + '?point={0},{1}'.format(5, 5))
        assert res.status_code == 200