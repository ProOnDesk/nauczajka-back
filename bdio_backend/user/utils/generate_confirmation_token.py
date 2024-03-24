import hashlib
import secrets
from user.models import TokenEmailConfirmation
from django.conf import settings

def generate_confirmation_token(user):
    # Generate a random string
    random_string = secrets.token_hex(16)

    # Create a confirmation token including user's email, random string, and current timestamp
    token = hashlib.sha256(f"{user.email}{random_string}".encode()).hexdigest()

    # Save the token to the database
    token_email_confirmation = TokenEmailConfirmation(user=user, token=token)
    token_email_confirmation.save()
    return token_email_confirmation


# def is_token_expired(token):
#     # Get the current timestamp
#     current_time = int(time.time())
    
#     if current_time - token.created_at_int > settings.CUSTOM_CONFIRM_EMAIL_TOKEN_EXPIRY_TIME:
#         return True
#     return False