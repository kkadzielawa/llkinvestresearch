from unittest.mock import patch

from django.conf import settings
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(SECURE_SSL_REDIRECT=False)
class SEOTests(TestCase):
    def test_homepage_has_specific_title(self):
        response = self.client.get(reverse("home"))
        self.assertContains(
            response,
            "<title>LLK Investment Research | Independent Market Notes</title>",
            html=False,
        )

    def test_robots_txt_lists_sitemap(self):
        response = self.client.get(reverse("robots_txt"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "User-agent: *")
        self.assertContains(response, "Sitemap:")
        self.assertContains(response, reverse("sitemap_xml"))

    def test_sitemap_contains_public_pages(self):
        response = self.client.get(reverse("sitemap_xml"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("home"))
        self.assertContains(response, reverse("blog"))
        self.assertContains(response, reverse("contact"))


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

    @override_settings(CONTACT_FORM_RECIPIENTS=["editor@example.com"])
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
        self.assertEqual(mail.outbox[0].to, settings.CONTACT_FORM_RECIPIENTS)
        self.assertEqual(mail.outbox[0].reply_to, ["visitor@example.com"])
        self.assertIn("Visitor", mail.outbox[0].body)
        self.assertIn("555-0101", mail.outbox[0].body)
        self.assertContains(response, "Your note has been sent successfully")

    def test_honeypot_submission_does_not_send_mail(self):
        response = self.client.post(
            reverse("contact"),
            {
                "name": "Spam Sender",
                "email": "spam@example.com",
                "phone": "555-0101",
                "message": "This message is long enough to pass validation.",
                "website": "https://example.com",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)

    @patch("llkinvestresearch.views.logger.exception")
    @patch(
        "llkinvestresearch.views.EmailMessage.send",
        side_effect=OSError("SMTP timeout"),
    )
    def test_email_failure_rerenders_form_with_error(
        self,
        mock_send,
        mock_logger_exception,
    ):
        response = self.client.post(
            reverse("contact"),
            {
                "name": "Visitor",
                "email": "visitor@example.com",
                "phone": "555-0101",
                "message": "Hello from the site.",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sorry, your message could not be sent.")
        self.assertEqual(len(mail.outbox), 0)
        mock_send.assert_called_once_with(fail_silently=False)
        mock_logger_exception.assert_called_once_with(
            "Contact form email delivery failed"
        )
