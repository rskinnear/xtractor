from datetime import datetime

from pydantic import BaseModel


# class ScrapeSettings(BaseModel):
#     username: str
#     with_replies: bool
#     limit: PositiveInt


class Credentials(BaseModel):
    email: str
    username: str
    password: str


class Impressions(BaseModel):
    views: int
    likes: int
    reposts: int
    bookmarks: int
    replies: int


class PostData(BaseModel):
    text: str | None
    url: str | None
    date: datetime | None
    author_username: str | None
    author_name: str | None
    post_media: set[str]
    is_repost: bool
    video_in_post: bool
    post_id: str | None
    impressions: Impressions


class UserData(BaseModel):
    name: str | None
    username: str | None
    url: str | None
    followers: int | None
    following: int | None
    subscriptions: int | None
    bio: str | None
    join_date: datetime | None
    profession: str | None
    location: str | None
