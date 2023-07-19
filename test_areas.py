from django.contrib.gis.geos import Polygon, GEOSGeometry
import requests
import pytest
import json
from django.test import TestCase

API_URL = "http://127.0.0.1:8000/api/buildings/"

class MyTestForAreas(TestCase):
    def test_get_building(self):
        # Тест существующего айди здания
        building_id = 1
        res = requests.get(API_URL + f'{building_id}/')
        assert res.status_code == 200
        data = res.json()
        assert data["id"] == building_id
        return data

    def test_get_nonexistent_building(self):
        # Несуществующий айди здания
        nonexistent_building_id = 999
        res = requests.get(API_URL + f'{nonexistent_building_id}/')
        assert res.status_code == 404

    def test_invalid_building_id(self):
        # Недействительного айди здания
        invalid_id = "INVALID_ID"
        res = requests.get(API_URL + f'{invalid_id}/')
        assert res.status_code == 404

    def get_list_buildings(self):
        res = requests.get(API_URL + '')
        assert res.status_code == 200
        data = res.json()
        return data

    def test_correct_very_big_area_filter(get_list_buildings):
        res = requests.get(API_URL + '?min=0&max=1000000000000000')
        assert res.status_code == 200
        data = res.json()
        data == get_list_buildings
        return data

    def test_correct_incorrect_args_area_filter(self):
        res = requests.get(API_URL + '?min=asd&max=asd000000')
        assert res.status_code == 400
        res = requests.get(API_URL + '?min=123&max=asd000000')
        assert res.status_code == 400
        res = requests.get(API_URL + '?min=asd&max=1000000')
        assert res.status_code == 400

    def test_empty_args_area_filter(self):
        res = requests.get(API_URL + '?min=&max=')
        assert res.status_code == 200
        res = requests.get(API_URL + '?min=&max=1000000')
        assert res.status_code == 200
        res = requests.get(API_URL + '?min=0&max=')
        assert res.status_code == 200

    def test_empty_incorrect_args_names_area_filter(self):
        res = requests.get(API_URL + '?mi&ma=')
        assert res.status_code == 200
        res = requests.get(API_URL + '?mi&max=1000000')
        assert res.status_code == 200
        res = requests.get(API_URL + '?m=0&max=')
        assert res.status_code == 200

    def test_zero_max_area_filter(self):
        res = requests.get(API_URL + '?max=0')
        assert res.status_code == 200
        data = res.json()
        assert len(data["features"]) == 0