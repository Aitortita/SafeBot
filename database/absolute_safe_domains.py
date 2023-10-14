from database.models import SafeDomain
import uuid

domainList = [
    "google.com",
    "youtube.com",
    "you.tube",
    "outplayed.tv",
    "streamable.com",
    "twitch.tv",
    "discordapp.net",
]

absoluteSafeDomains = [SafeDomain(id=str(uuid.uuid4()), domain_name=value) for value in domainList]
