from typing import List, Dict


class GprrUser(object):
    """
    User representation in GPRR
    """
    login: str = None
    name: str = None
    url: str = None

class GprrReview(object):
    """
    Review representation in GPRR
    """
    user: GprrUser = None
    state: str = None
    submitted_at: str = None
    url: str = None

class GprrPrFlag(object):
    """ Representation of GitHub flag, used in GPRR"""
    flag: str = None
    value: str = None

class GprrPrLabel(object):
    """ Representation of GitHub label, used in GPRR"""
    title: str = None
    color: str = None

class GprrPR(object):
    """ Representation of pull request, used in GPRR"""
    id: int = None
    number: int = None
    url: str = None
    repository: str = None
    title: str = None
    flags: List[GprrPrFlag] = []
    labels: List[GprrPrLabel] = []
    creator: GprrUser = None
    reviewers: List[GprrReview] = []
    assignees: List[GprrUser] = []
    created: str = None
    updated: str = None
    since_updated: int = None
    initial_branch: str = None
    initial_branch_url: str = None


class PrContainer(object):
    title: str = None
    sections: Dict[str, List[GprrPR]]

    def initSection(
            self,
            section_name: str = "",
            section_elements: List[GprrPR] = []
    ):
        self.sections[section_name] = section_elements

    def appendSection(
            self,
            section_name: str = "",
            section_elements: List[GprrPR] = []
    ):
        if section_name in self.sections.keys():
            _list = self.sections[section_name]
            _list.extend(section_elements)
            self.sections[section_name] = _list
        else:
            self.sections[section_name] = section_elements



