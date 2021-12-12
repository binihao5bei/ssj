import allure
import pytest


@pytest.mark.dependency(name="notify_team", depends=["create_project"], scope="session")
def test_notify_team(rq, value):
    rq(value)


@pytest.mark.dependency(depends=["notify_team"])
def test_put_notify_team(rq, value):
    rq(value)


@pytest.mark.dependency(depends=["notify_team"])
def test_notify_project(rq, value):
    rq(value)


@pytest.mark.dependency(depends=["notify_team"])
def test_put_notify_project(rq, value):
    rq(value)
