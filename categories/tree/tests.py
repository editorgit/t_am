import json

from django.test import TestCase

from .models import Category


class TreeTestCase(TestCase):
    maxDiff = None

    def setUp(self):
        initial_data = {
            "name": "Category 1",
            "children": [
                {
                    "name": "Category 1.1",
                    "children": [
                        {
                            "name": "Category 1.1.1",
                            "children": [
                                {
                                    "name": "Category 1.1.1.1"
                                },
                                {
                                    "name": "Category 1.1.1.2"
                                },
                                {
                                    "name": "Category 1.1.1.3"
                                }
                            ]
                        },
                        {
                            "name": "Category 1.1.2",
                            "children": [
                                {
                                    "name": "Category 1.1.2.1"
                                },
                                {
                                    "name": "Category 1.1.2.2"
                                },
                                {
                                    "name": "Category 1.1.2.3"
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": "Category 1.2",
                    "children": [
                        {
                            "name": "Category 1.2.1"
                        },
                        {
                            "name": "Category 1.2.2",
                            "children": [
                                {
                                    "name": "Category 1.2.2.1"
                                },
                                {
                                    "name": "Category 1.2.2.2"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        response = self.client.post('/categories/',
                                    json.dumps(initial_data),
                                    content_type="application/json")

    def test_cat_2(self):
        expected = {
            "id": 2,
            "name": "Category 1.1",
            "parents": [
                {
                    "id": 1,
                    "name": "Category 1"
                }
            ],
            "children": [
                {
                    "id": 3,
                    "name": "Category 1.1.1"
                },
                {
                    "id": 7,
                    "name": "Category 1.1.2"
                }
            ],
            "siblings": [
                {
                    "id": 11,
                    "name": "Category 1.2"
                }
            ]
        }

        actual = self.client.get('/categories/2').content
        self.assertDictEqual(expected, json.loads(actual))

    def test_cat_8(self):
        expected = {
            "id": 8,
            "name": "Category 1.1.2.1",
            "parents": [
                {
                    "id": 7,
                    "name": "Category 1.1.2"
                }, {
                    "id": 2,
                    "name": "Category 1.1"
                },
                {
                    "id": 1,
                    "name": "Category 1"
                },
            ],
            "children": [],
            "siblings": [
                {
                    "id": 9,
                    "name": "Category 1.1.2.2"
                },
                {
                    "id": 10,
                    "name": "Category 1.1.2.3"
                }
            ]
        }

        actual = self.client.get('/categories/8').content
        self.assertDictEqual(expected, json.loads(actual))
