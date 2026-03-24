# Django
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core import signing
# Phone number field
from phonenumbers import parse, format_number, PhoneNumberFormat, NumberParseException

class UserWhatsApp(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="whatsapp_contacts",
        on_delete=models.CASCADE
    )
    country_code = models.PositiveIntegerField()
    number = models.CharField(max_length=20)
    full_number = models.CharField(max_length=20)

    verified = models.BooleanField(default=False)
    otp_signed = models.TextField(null=True, blank=True)
    otp_expires_at = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "full_number"],
                name="unique_user_full_number"
            )
        ]

    def __str__(self):
        return self.full_number

    # -----------------------
    # OTP Utilities
    # -----------------------
    def otp_is_valid(self, otp: str) -> bool:
        if not self.otp_signed or not self.otp_expires_at:
            return False
        if timezone.now() > self.otp_expires_at:
            return False
        try:
            signed_otp = signing.loads(self.otp_signed)
            return signed_otp == otp
        except signing.BadSignature:
            return False

    def verify(self):
        self.verified = True
        self.otp_signed = None
        self.otp_expires_at = None
        self.save(update_fields=["verified", "otp_signed", "otp_expires_at"])

    # -----------------------
    # Normalización de número
    # -----------------------
    @classmethod
    def normalize_number(cls, raw_number: str):
        try:
            pn = parse(raw_number, None)
            country_code = pn.country_code
            number = str(pn.national_number)
            full_number = format_number(pn, PhoneNumberFormat.E164)
            return country_code, number, full_number
        except NumberParseException:
            raise ValueError("Número inválido")
