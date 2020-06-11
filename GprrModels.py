from datetime import datetime
from typing import List, Dict, Set, Generic, TypeVar


class GprrUser(object):
    """
    User representation in GPRR
    """

    def __init__(
            self,
            login: str = None,
            name: str = None,
            url: str = None,
            id: int = None,
    ):
        assert login is not None
        assert name is not None
        assert url is not None
        assert login is not None

        self.login = login
        self.name = name
        self.id = id
        self.url = url


class GprrReview(object):
    """
    Review representation in GPRR
    """

    def __init(
            self,
            user: GprrUser,
            state: str,
            submitted_at: datetime = None,
            url: str = None,
    ):
        assert user is not None
        assert state is not None

        self.user = user
        self.state = state
        self.submitted_at = submitted_at
        self.url = url


class GprrPrFlag(object):
    """ Representation of GitHub flag, used in GPRR"""

    def __init__(
            self,
            flag: str = None,
            value: str = None
    ):
        assert flag is not None
        assert value is not None
        self.flag = flag
        self.value = value


class GprrPrLabel(object):
    """ Representation of GitHub label, used in GPRR"""

    def __init__(
            self,
            title: str = None,
            color: str = None,
            description: str = None
    ):
        assert title is not None
        assert color is not None
        assert description is not None
        self.title = title
        self.color = color
        self.description = description


class GprrPR(object):
    """ Representation of pull request, used in GPRR"""

    def __init__(self):
        self.id: int = None
        self.number: int = None
        self.url: str = None
        self.repository: str = None
        self.title: str = None
        self.flags: List[GprrPrFlag] = []
        self.labels: List[GprrPrLabel] = []
        self.creator: GprrUser = None
        self.reviews: List[GprrReview] = []
        self.assignees: List[GprrUser] = []
        self.created: datetime = None
        self.updated: datetime = None
        self.since_updated: int = None
        self.initial_branch: str = None
        self.initial_branch_url: str = None


class GprrRepository(object):

    def __init__(
            self,
            id: int,
            title: str,
            url: str,
            name: str,
    ):
        assert id is not None
        assert title is not None
        assert url is not None
        assert name is not None
        self.id = id
        self.title = title
        self.url = url
        self.name = name



class PrContainer(object):

    def __init__(
            self,
            title: str = ""
    ):
        self.title = title
        self.container: Dict[str, List[GprrPR]] = {}

    def append_item(
            self,
            item: GprrPR,
            item_group: str = ""
    ):
        assert item is not None

        if item_group in self.container.keys():
            self.container[item_group].add(item)
        else:
            self.container[item_group] = [item]


T = TypeVar('T')


class Filter(Generic[T]):

    def __init__(
            self,
            title: str
    ):
        assert title is not None
        self.title = title
        self.items: [T] = []

    def contains(self, item: T) -> bool:
        return self.contains_item_id(item.id)

    def add(self, item: T):
        assert item is not None
        if not self.contains_item_id(item.id):
            self.items.add(item)

    def contains_item_id(self, item_id: int) -> bool:
        assert item_id is not None
        for usr in self.items:
            if usr.id == item_id:
                return True
        return False
