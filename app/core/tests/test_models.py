from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@example.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email=email, password=password)


class ModelTest(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@mmm.com'
        password = 'Testcase1235'
        # create vs create_user
        user = get_user_model().objects.create(
            email=email
        )
        user.set_password(password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email normalization"""
        email = 'test@LONDON.com'
        user = get_user_model().objects.create_user(
            email, 'Testcase1235'
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_email_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(AssertionError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test create a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@superuser.com', 'test1234'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='vegan'
        )
        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )
        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and sauce',
            time_minutes=5,
            price=5.00
        )
        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
