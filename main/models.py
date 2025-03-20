import secrets
from django.db import models

def make_token():
    return secrets.token_urlsafe(64)

class Signature(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    affiliation = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    situation = models.CharField(max_length=64, null=False, blank=False, choices=(
        ("unable", "I am unable to travel to the US, or it is not safe for me to travel."),
        ("unwilling", "I am refusing to travel in solidarity."),
        ("support", "I am not a member of the IETF community, but I rely on their work and support this open letter")
    ))
    public = models.BooleanField(null=False, blank=True)
    validated = models.BooleanField(null=False, blank=True, default=False)
    token = models.CharField(max_length=255, null=False, blank=False, unique=True, default=make_token, db_index=True)

    def __str__(self):
        return f"{self.name} - {self.email}"