from datetime import datetime
from typing import List, Dict, Set, Generic, TypeVar


class GprrUser(object):
    """
        User representation in GPRR
    """

    def __init__(self, login: str, name: str, url: str, id: int):
        assert login is not None
        assert url is not None
        assert id is not None

        self.login = login
        if name is None:  # in case if user not fill in Name field in profile
            self.name = login
        else:
            self.name = name
        self.id = id
        self.url = url


class GprrReview(object):
    """
    Review representation in GPRR
    """

    def __init__(self, user: GprrUser, state: str, submitted_at: datetime = None, url: str = None,):
        assert user is not None
        assert state is not None

        self.user = user
        self.state = state
        self.submitted_at = submitted_at
        self.url = url


class GprrPrFlag(object):
    """
        Representation of GitHub flag, used in GPRR
    """

    def __init__(self, flag: str, value: str):
        assert flag is not None
        assert value is not None
        self.flag_name = flag
        self.value = value


class GprrPrLabel(object):
    """
        Representation of GitHub label, used in GPRR
    """

    def __init__(self, title: str, color: str, description: str):
        assert title is not None
        assert color is not None
        assert description is not None
        self.title = title
        self.color = color
        self.description = description


class GprrPR(object):
    """
        Representation of pull request, used in GPRR
    """

    def __init__(self):
        self.id: int = None
        self.number: int = None
        self.url: str = None
        self.repository: GprrRepository = None
        self.title: str = None
        self.flags: List[GprrPrFlag] = []
        self.labels: List[GprrPrLabel] = []
        self.creator: GprrUser = None
        self.reviews: List[GprrReview] = []
        self.reviews_pending: List[GprrReview] = []
        self.reviews_pending_teams: List[GprrReview] = []
        self.assignees: List[GprrUser] = []
        self.created: datetime = None
        self.updated: datetime = None
        self.since_updated: int = None
        self.initial_branch: str = None
        self.initial_branch_url: str = None


class GprrRepository(object):
    """
        Representation of Github repository information, used in GPRR
    """

    def __init__(self, id: int, url: str, name: str, title: str = ""):
        assert id is not None
        assert url is not None
        assert name is not None
        self.id = id
        if title is None:  # in case if creator not fill in Title field for repository
            self.title = ""
        else:
            self.title = title
        self.url = url
        self.name = name



class PrContainer(object):
    """
        Container for pull requests. Contains some logic, but basically just a wrapper on Dict type
    """

    def __init__(self, title: str = ""):
        self.title = title
        self.container: Dict[str, List[GprrPR]] = dict()

    def append_item(self, item: GprrPR, item_group: str = "", uniq: bool = False):
        """
            Append item to container.
            if uniq param is false, always add item,
            if uniq param is true - first check if item present in dict, and if not than add

            :param item: item to add
            :param item_group: grouping key for items
            :param uniq: check uniqness of item in provided group
            :return:
        """
        assert item is not None

        if item_group in self.container.keys():
            if uniq:
                uniq_item = True
                for i in self.container[item_group]:
                    if i.id == item.id:
                        uniq_item = False
                if uniq_item:
                    self.container[item_group].append(item)
            else:
                self.container[item_group].append(item)
        else:
            self.container[item_group] = [item]


T = TypeVar('T')
class Filter(Generic[T]):
    """
        Container for configuration items. Actually, another wrapper on list() with custom logic
    """

    def __init__(self, title: str):
        assert title is not None
        self.title = title
        self.items: List[T] = []

    def contains(self, item: T) -> bool:
        return self.contains_item_id(item.id)

    def add(self, item: T):
        assert item is not None
        if not self.contains_item_id(item.id):
            self.items.append(item)

    def contains_item_id(self, item_id: int) -> bool:
        assert item_id is not None
        for usr in self.items:
            if usr.id == item_id:
                return True
        return False
