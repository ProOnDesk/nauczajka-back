"""
Tests for user models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class UserModelTests(TestCase):
    """
    Test user model
    """
    def test_create_user(self):
        """
        Test creating a new user
        """
        email = 'test@example.com'
        password = 'testpassword123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
    
    def test_create_new_superuser(self):
        """
        Test creating a new superuser
        """
        email = 'admin@example.com'
        password = 'adminpassword123'
        superuser = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertEqual(superuser.email, email)
        self.assertTrue(superuser.check_password(password))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        
    def test_new_user_email_normalized(self):
        """
        Test the email for a new user is normalized
        """
        example_emails = [
            ('test@EXAMPLE.com', 'test@example.com'),
            ('Test2@Example.com', 'Test2@example.com'),
            ('FIRST.LAST@example.com', 'FIRST.LAST@example.com'),
            ('john.doe@sub.example.co.uk', 'john.doe@sub.example.co.uk'),
        ]
        
        for original_email, expected_email in example_emails:
            user = get_user_model().objects.create_user(
                email=original_email,
                password='test123'
            )
            self.assertEqual(user.email, expected_email)
            
    def test_user_without_email(self):
        """
        Test no input in email
        """
        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(
                password='testpassword123',
                email=''
            )
    
    def test_user_with_invalid_email(self):
        """
        Test invalid email
        """
        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(
                password='testpassword123',
                email='adsa'
            )
