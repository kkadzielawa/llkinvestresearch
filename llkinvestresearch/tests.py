from django.conf import settings
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    SECURE_SSL_REDIRECT=False,
)
class ContactViewTests(TestCase):
    def test_get_renders_form(self):
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Konrad Kadzielawa")
        self.assertContains(response, "Send message")

    def test_invalid_post_rerenders_errors(self):
        response = self.client.post(reverse("contact"), {"name": "", "email": "bad"})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "name",
            "This field is required.",
        )

    @override_settings(CONTACT_EMAIL="editor@example.com")
    def test_valid_post_sends_mail(self):
        response = self.client.post(
            reverse("contact"),
            {
                "name": "Visitor",
                "email": "visitor@example.com",
                "phone": "555-0101",
                "message": "Hello from the site.",
            },
            follow=True,
        )
        self.assertRedirects(response, reverse("contact"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [settings.CONTACT_EMAIL])
        self.assertContains(response, "Your note has been sent successfully")
