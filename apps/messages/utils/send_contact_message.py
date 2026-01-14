from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags


def send_contact_email(instance):
    """Contact Message uchun admin bildirishnomasi"""
    subject = f"📩 New Contact Message: {instance.full_name}"
    html_message = f"""
    <div style="font-family: sans-serif; border: 1px solid #eee; padding: 20px;">
        <h2 style="color: #004a99;">BMTransco - New Contact</h2>
        <p><strong>Name:</strong> {instance.full_name}</p>
        <p><strong>Email:</strong> {instance.email}</p>
        <p><strong>Phone:</strong> {instance.phone or "N/A"}</p>
        <p><strong>Company:</strong> {instance.company or "N/A"}</p>
        <div style="background: #f4f4f4; padding: 15px; border-radius: 5px;">
            <strong>Message:</strong><br>{instance.message}
        </div>
    </div>
    """
    send_mail(
        subject,
        strip_tags(html_message),
        settings.DEFAULT_FROM_EMAIL,
        [settings.ADMIN_EMAIL],
        html_message=html_message,
    )
