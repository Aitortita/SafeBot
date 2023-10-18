from database.models import WhitelistedDomain
import uuid

domainList = [
    "google.com",
    "youtube.com",
    "you.tube",
    "youtu.be",
    "outplayed.tv",
    "streamable.com",
    "twitch.tv",
    "discordapp.net",
    "twitter.com",
    "x.com",
]

baseWhitelistedDomains = [WhitelistedDomain(id=str(uuid.uuid4()), domain_name=value) for value in domainList]