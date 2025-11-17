# Django modules
from django.core.exceptions import ValidationError


def validate_email_payload_not_in_full_name(
        email: str,
        first_name: str,
        last_name: str) -> None:
    """
    Validate that email address does not contain the full name.
    """
    email_payload = email.split("@")[0]
    if email_payload.lower() in first_name.lower() + last_name.lower():
        raise ValidationError(
            {
                "email": "Email should not be a part of a full name.",
                "first_name": "First name shouldn't contain an email address.",
                "last_name": "Last name shouldn't  contain an email address.",
            },
            code="invalid_email_name_relation"
        )
