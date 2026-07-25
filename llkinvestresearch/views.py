from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from .forms import ContactForm


class HomeView(TemplateView):
    template_name = "home.html"


class MicroViewPageView(TemplateView):
    template_name = "microview_blog.html"


class OptionsStudyPageView(TemplateView):
    template_name = "options_study.html"


class MarketAnalyzerPageView(TemplateView):
    template_name = "market_analyzer.html"


class ContactView(FormView):
    template_name = "contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contact_email"] = settings.CONTACT_EMAIL
        context["linkedin_url"] = "https://www.linkedin.com/in/konradkadzielawa/"
        return context

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        phone = cleaned_data.get("phone") or "Not provided"
        body = (
            f"Name: {cleaned_data['name']}\n"
            f"Email: {cleaned_data['email']}\n"
            f"Phone: {phone}\n\n"
            f"{cleaned_data['message']}"
        )
        send_mail(
            subject=f"Website inquiry from {cleaned_data['name']}",
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
        )
        messages.success(
            self.request,
            "Thanks for reaching out. Your note has been sent successfully.",
        )
        return super().form_valid(form)
