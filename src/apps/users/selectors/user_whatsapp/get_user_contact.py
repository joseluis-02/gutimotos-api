from ...models.user_whatsapp import UserWhatsApp


def get_user_contact(user, phone_number):
    try:
        return UserWhatsApp.objects.get(user=user, phone_number=phone_number)
    except UserWhatsApp.DoesNotExist:
        return None
