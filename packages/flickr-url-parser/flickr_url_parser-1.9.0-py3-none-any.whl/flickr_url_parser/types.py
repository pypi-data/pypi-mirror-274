import typing


class Homepage(typing.TypedDict):
    type: typing.Literal["homepage"]


class SinglePhoto(typing.TypedDict):
    type: typing.Literal["single_photo"]
    photo_id: str
    user_url: str | None
    user_id: str | None


def anonymous_single_photo(photo_id: str) -> SinglePhoto:
    return {
        "type": "single_photo",
        "photo_id": photo_id,
        "user_url": None,
        "user_id": None,
    }


class Album(typing.TypedDict):
    type: typing.Literal["album"]
    user_url: str
    album_id: str
    page: int


class User(typing.TypedDict):
    type: typing.Literal["user"]
    page: int
    user_url: str
    user_id: str | None


class Group(typing.TypedDict):
    type: typing.Literal["group"]
    group_url: str
    page: int


class Gallery(typing.TypedDict):
    type: typing.Literal["gallery"]
    gallery_id: str
    page: int


class Tag(typing.TypedDict):
    type: typing.Literal["tag"]
    tag: str
    page: int


ParseResult = Homepage | SinglePhoto | Album | User | Group | Gallery | Tag
