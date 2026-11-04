from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class SignUpViewTests(TestCase):
    def test_signup_page_status_code(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")
        self.assertContains(response, "Create an Account")
        # Check Bootstrap 5 CDN is present
        self.assertContains(response, "bootstrap@5.3.3")

    def test_signup_successful_creation_and_success_message(self):
        signup_data = {
            "username": "newstudent",
            "email": "newstudent@example.com",
            "first_name": "New",
            "last_name": "Student",
            "course": "BSIT",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
        }
        response = self.client.post(reverse("signup"), signup_data, follow=True)
        # Should redirect to login page
        self.assertRedirects(response, reverse("login"))
        self.assertEqual(response.status_code, 200)

        # Check user was created
        self.assertTrue(User.objects.filter(username="newstudent").exists())
        user = User.objects.get(username="newstudent")
        self.assertEqual(user.first_name, "New")
        self.assertEqual(user.last_name, "Student")
        self.assertEqual(user.course, "BSIT")

        # Check that success message is displayed
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Account created successfully" in m.message for m in messages))
        self.assertContains(response, "Account created successfully")


class ProfileUpdateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="Password123!",
            first_name="InitialFirst",
            last_name="InitialLast",
            course="BSCS",
        )

    def test_profile_requires_login(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("login")))

    def test_profile_page_loads_for_authenticated_user(self):
        self.client.login(username="testuser", password="Password123!")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/profile.html")
        self.assertContains(response, "Edit Profile")
        self.assertContains(response, "InitialFirst")
        self.assertContains(response, "BSCS")

    def test_profile_update_successful(self):
        self.client.login(username="testuser", password="Password123!")
        post_data = {
            "first_name": "UpdatedFirst",
            "last_name": "UpdatedLast",
            "email": "updated@example.com",
            "course": "BSIT",
        }
        response = self.client.post(reverse("profile"), post_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Refresh from database
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "UpdatedFirst")
        self.assertEqual(self.user.last_name, "UpdatedLast")
        self.assertEqual(self.user.email, "updated@example.com")
        self.assertEqual(self.user.course, "BSIT")

        # Verify success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("profile has been updated" in m.message for m in messages))
        self.assertContains(response, "Your profile has been updated successfully!")

    def test_profile_update_cannot_escalate_role(self):
        """Security test: Users cannot change their role via ProfileUpdateView."""
        self.client.login(username="testuser", password="Password123!")
        post_data = {
            "first_name": "Hacker",
            "last_name": "User",
            "email": "hacker@example.com",
            "course": "BSIT",
            "role": "admin",
            "is_staff": True,
        }
        self.client.post(reverse("profile"), post_data)
        self.user.refresh_from_db()
        # Role must remain student and is_staff must remain False
        self.assertEqual(self.user.role, User.Role.STUDENT)
        self.assertFalse(self.user.is_staff)
