from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.fields import DateTimeField
from rest_framework.test import APITestCase
from django.db import models

from .models import Post

class PostModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_post = Post.objects.create(
            auther = test_user,
            title = 'Title of Blog',
            body = 'Words about the blog'
        )
        test_post.save()

    def test_blog_content(self):
        post = Post.objects.get(id=1)
        
        print("post")
        self.assertEqual(str(post.auther), 'tester')
        self.assertEqual(post.title, 'Title of Blog')
        self.assertEqual(post.body, 'Words about the blog')

class APITest(APITestCase):
    def test_list(self):
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        """
        Test the api can create a post.
        """
        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        url = reverse('post-list')
        data = {
            "auther":test_user.id,
            "title":"Testing is Fun!!!",
            "body":"when the right tools are available",
            # "created_at" : DateTimeField(auto_now_add=True),
            # "updated_at" : DateTimeField(auto_now=True),
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,test_user.id)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, data['title'])

    def test_update(self):
        """
        Test the api can update a post.
        """

        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_post = Post.objects.create(
            auther = test_user,
            title = 'Title of Blog',
            body = 'Words about the blog'
        )

        test_post.save()

        url = reverse('post-detail',args=[test_post.id])
        data = {
            "title":"Testing is Still Fun!!!",
            "auther":test_post.auther.id,
            "body":test_post.body,
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK, url)

        self.assertEqual(Post.objects.count(), test_post.id)
        self.assertEqual(Post.objects.get().title, data['title'])

    def test_delete(self):
        """
        Test the api can delete a post.
        """

        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_post = Post.objects.create(
            auther = test_user,
            title = 'Title of Blog',
            body = 'Words about the blog'
        )

        test_post.save()

        post = Post.objects.get()

        url = reverse('post-detail', kwargs={'pk': post.id})


        response = self.client.delete(url)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT, url)