from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class DashboardAndAdminPanelTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(
            username="student1",
            password="Password123!",
            role=User.Role.STUDENT,
        )
        self.admin = User.objects.create_user(
            username="admin1",
            password="Password123!",
            role=User.Role.ADMIN,
            is_staff=True,
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_accessible_to_student(self):
        self.client.login(username="student1", password="Password123!")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/home.html")
        self.assertContains(response, "Edit Profile")
        # Student should NOT see the Open admin panel button
        self.assertNotContains(response, "Open Admin Panel")

    def test_dashboard_accessible_to_admin(self):
        self.client.login(username="admin1", password="Password123!")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        # Admin SHOULD see the Open admin panel button
        self.assertContains(response, "Open Admin Panel")

    def test_admin_panel_forbidden_for_student(self):
        self.client.login(username="student1", password="Password123!")
        response = self.client.get(reverse("admin_panel"))
        self.assertEqual(response.status_code, 403)

    def test_admin_panel_accessible_for_admin(self):
        self.client.login(username="admin1", password="Password123!")
        response = self.client.get(reverse("admin_panel"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/admin_panel.html")
        self.assertContains(response, "Registered Member")
        self.assertContains(response, "student1")
        self.assertContains(response, "admin1")
