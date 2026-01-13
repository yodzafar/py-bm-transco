from django.urls import path

from apps.messages.views import CreateContactMessageView, FreightQuoteCreateView

urlpatterns = [
    path(
        "contact-form",
        CreateContactMessageView.as_view(),
        name="contact-message-create",
    ),
    path(
        "freight-quote",
        FreightQuoteCreateView.as_view(),
        name="freight-quote-create",
    ),
]
