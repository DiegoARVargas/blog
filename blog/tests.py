from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Post
from django.urls import reverse

class BlogTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username = "testuser",
            email = "test@gmail.com",
            password = "123",
        )

        cls.post = Post.objects.create(
            title = "Titulo de prueba",
            body = "cuerpo de prueba",
            author = cls.user,
        )

    def test_post_model(self):
        self.assertEqual(self.post.title, "Titulo de prueba")
        self.assertEqual(self.post.body, "cuerpo de prueba")
        self.assertEqual(self.post.author.username, "testuser")
        self.assertEqual(str(self.post), "Titulo de prueba")
        self.assertEqual(self.post.get_absolute_url(), "/post/1/")

    def test_url_exists_at_correct_location_listview(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_detailview(self):
        response = self.client.get("/post/1/")
        self.assertEqual(response.status_code, 200)

    def test_post_listview(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "cuerpo de prueba")
        self.assertTemplateUsed(response, "home.html")

    def test_post_detailview(self):
        response = self.client.get(reverse("post_detail", kwargs={"pk": self.post.pk}))
        no_response = self.client.get("/post/1000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Titulo de prueba")
        self.assertTemplateUsed(response, "post_detail.html")
        