from django.core.validators import RegexValidator


phone_message = 'Phone number must be entered in the format '

# your desired format
phoneNumberRegex = RegexValidator(
    regex=r"^\+?1?\d{8,15}$", message=phone_message)