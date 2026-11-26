from django.test import TestCase

from .models import Book, Character, Review


class SchoolTests(TestCase):
    def test_pages_and_missing_parameters(self):
        for route in ("/", "/quote/", "/weekday/", "/portfolio/", "/projects/2", "/contacts/",
                      "/schedule/", "/schedule/week/", "/schedule/monday/", "/schedule/teachers/"):
            self.assertEqual(self.client.get(route).status_code, 200, route)
        self.assertEqual(self.client.get("/projects/999").status_code, 404)
        self.assertEqual(self.client.get("/schedule/not-a-day/").status_code, 404)

    def test_battle(self):
        first = Character.objects.create(name="Knight", hp=20, attack=8, defense=5)
        second = Character.objects.create(name="Orc", hp=9, attack=3, defense=3)
        response = self.client.post("/api/battle/", {"character_1": first.pk, "character_2": second.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["winner"], "Knight")
        self.assertEqual(response.json()["rounds"], 2)
        self.assertEqual(self.client.get("/api/history/").json()[0]["winner"], "Knight")

    def test_library(self):
        self.assertEqual(self.client.post("/library/add/", {"title": "Місто", "author": "Автор",
                         "genre": "Роман", "summary": ""}).status_code, 302)
        book = Book.objects.get()
        self.assertContains(self.client.get("/library/?q=Міст&genre=Роман"), "Місто")
        self.client.post("/library/reviews/add/", {"book": book.pk, "reader": "Читач", "score": 5, "text": "Добре"})
        review = Review.objects.get()
        self.assertContains(self.client.get(f"/library/reviews/{review.pk}/"), "Добре")
        self.assertEqual(self.client.post(f"/library/{book.pk}/delete/").status_code, 302)
        self.assertFalse(Review.objects.exists())
