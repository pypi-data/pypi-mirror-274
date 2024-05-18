from datetime import datetime, timezone, timedelta
import pydantic
from pydantic import Json, EmailStr
from pydantic.networks import HttpUrl, IPv4Address, IPv6Address
from typing import Literal

class SocialLink(pydantic.BaseModel):
    domain : str
    url : HttpUrl | EmailStr

class LinktreeLink(SocialLink):
    id : int
    title : str
    type : str

class HoobeLinkShort(SocialLink):
    id : str

class HoobeLink(SocialLink):
    id : str
    title : str
    created : datetime
    updated : datetime

class SnipfeedLinkShort(SocialLink):
    id : str
    platform : str

class SnipfeedLink(SocialLink):
    id : str
    title : str
    image : HttpUrl | None

class BeaconsLinkShort(SocialLink):
    pass

class BeaconsLink(SocialLink):
    title : str
    image : HttpUrl

class AllmylinksLink(SocialLink):
    title : str
    image : HttpUrl

class MilkshakeLink(SocialLink):
    title : str

class LinkrLink(SocialLink):
    id : str
    title : str
    image : HttpUrl | None
    created : datetime | None

class CarrdLink(SocialLink):
    title : str

class LnkbioLinkShort(SocialLink):
    pass

class LnkbioLink(SocialLink):
    id : str
    title : str

class DirectmeLinkShort(SocialLink):
    pass

class DirectmeLink(SocialLink):
    title : str

class LinkmeLinkShort(SocialLink):
    id : int
    title : str
    image : HttpUrl

class LinkmeLink(SocialLink):
    id : int
    title : str
    description : str | None
    image : HttpUrl
    thumbnail : Literal['small', 'medium', 'big']
    color : Json[dict[str, dict[str, str]]]
    type : dict[str, str]

class TaplinkLink(SocialLink):
    title : str



class SocialsTree(pydantic.BaseModel):
    username : str
    avatar : HttpUrl | Literal[''] | None
    links : list[SocialLink]
    
class LinktreeTree(SocialsTree):
    id : int
    tz : str
    links : list[LinktreeLink]

class HoobeTree(SocialsTree):
    id : str
    displayname : str
    usertype : int
    created : datetime
    updated : datetime
    links : list[HoobeLink | HoobeLinkShort]

class SnipfeedTree(SocialsTree):
    id : str
    links : list[SnipfeedLink | SnipfeedLinkShort]

class BeaconsTree(SocialsTree):
    links : list[BeaconsLink | BeaconsLinkShort]

class AllmylinksTree(SocialsTree):
    displayname : str
    links : list[AllmylinksLink]

class MilkshakeTree(SocialsTree):
    links : list[MilkshakeLink]

class LinkrTree(SocialsTree):
    description : str
    links : list[LinkrLink]

class CarrdTree(SocialsTree):
    description : str
    links : list[CarrdLink]

class LnkbioTree(SocialsTree):
    id : str
    tz : str
    links : list[LnkbioLink | LnkbioLinkShort]

class DirectmeTree(SocialsTree):
    description : str
    links : list[DirectmeLink | DirectmeLinkShort]

class LinkmeTree(SocialsTree):
    ip : IPv4Address | IPv6Address
    id : str
    first_name : str
    last_name : str
    verified : int
    bio : str
    ambassador : int
    profile_visits : str
    links : list[LinkmeLink | LinkmeLinkShort]

class TaplinkTree(SocialsTree):
    id : int
    profile_id : int
    displayname : str
    nickname : str
    links : list[TaplinkLink]
