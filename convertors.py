from datetime import datetime
from typing import List

from github.Label import Label
from github.NamedUser import NamedUser
from github.PullRequest import PullRequest
from github.Repository import Repository

from GprrModels import GprrUser, GprrRepository, GprrPrLabel, GprrReview, GprrPR, GprrPrFlag


def convert_pr(pr: PullRequest) -> GprrPR:
    """
        Converts PyGithub pull request representation to GPRR pull request representation

        :param pr: PyGithub pull request
        :return: GPRR pull request
    """
    gprr_pr = GprrPR()
    gprr_pr.id = pr.id
    gprr_pr.number = pr.number
    gprr_pr.url = pr.html_url
    gprr_pr.repository = convert_repo(pr.head.repo)
    gprr_pr.title = pr.title
    gprr_pr.creator = convert_user(pr.user)
    gprr_pr.created = pr.created_at
    gprr_pr.updated = pr.updated_at
    gprr_pr.since_updated = (datetime.today() - gprr_pr.updated).days
    gprr_pr.flags.append(GprrPrFlag("Draft", str(pr.draft)))
    gprr_pr.flags.append(GprrPrFlag("Mergeable", str(pr.mergeable)))
    gprr_pr.flags.append(GprrPrFlag("Mergeable State", str(pr.mergeable_state)))
    gprr_pr.initial_branch = pr.head.ref

    for assignee in pr.assignees:
        gprr_pr.assignees.append(convert_user(assignee))

    for label in pr.get_labels():  # this makes additional call to Github REST API
        gprr_pr.labels.append(convert_label(label))

    active_reviewers = []
    for review in pr.get_reviews():  # this makes additional call to Github REST API
        reviewer = convert_user(review.user)
        if not known_review(active_reviewers, reviewer):
            active_reviewers.append(reviewer)
            gprr_review = GprrReview(
                user=reviewer,
                state=review.state,
                submitted_at=review.submitted_at,
                url=review.html_url,
            )
            gprr_pr.reviews.append(gprr_review)

    for revusr in pr.get_review_requests()[0]:  # this makes additional call to Github REST API
        usr = convert_user(revusr)
        review = GprrReview(user=usr, state="PENDING")
        gprr_pr.reviews_pending.append(review)

    return gprr_pr


def convert_label(label: Label) -> GprrPrLabel:
    """
        Converts GitHub label object to GPRR label object

        :param label: GitHub label object
        :return: GPRR label object
    """
    return GprrPrLabel(title=label.name, color=label.color, description=label.description)


def convert_user(user: NamedUser) -> GprrUser:
    """
        Converts Github user object (NamedUser) to GPRR user object (GprrUser)

        :param user: Github user object
        :return: GPRR user object
    """
    return GprrUser(login=user.login, name=user.name, id=user.id, url=user.html_url)


def convert_repo(repo: Repository) -> GprrRepository:
    if repo is not None:
        return GprrRepository(id=repo.id, title=repo.description, url=repo.html_url, name=repo.name)
    else:
        return GprrRepository(id=-1, title="", url="#", name="unknown repository (might be private fork")


def known_review(active_reviewers: List[GprrUser], user: GprrUser) -> bool:
    """
        Check if provided user is already in reviewers list. Github returns all reviews sorted by date,
        and we are interested only in latest user review.

        :param active_reviewers: list of reviewers
        :param user: reviewer to check
        :return: true if reviewer is already in the list. Checked by user id
    """
    for rvw in active_reviewers:
        if rvw.id == user.id:
            return True
    return False
