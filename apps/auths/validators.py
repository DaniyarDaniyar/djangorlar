#Python modules

#Django modules
from django.core.exceptions import ValidationError

#Project modules

__RESTRICTED_DOMAINS = (
    "kbtu.kz",
    )

def validate_not_restricted_email_domain(email: str) -> None:   
    """
    Validator to ensure email does not belong to restricted domains.
    """
    domain = email.split('@')[-1]
    if domain in __RESTRICTED_DOMAINS:
        raise ValidationError(
            message=f"Registration using the domain \"{domain}\" is not allowed.",
            code="invalid_domain",
        )