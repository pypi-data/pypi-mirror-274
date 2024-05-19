from pytest import fixture

from datapools.common.session_manager import Session, SessionManager, SessionStatus
from datapools.common.types import WorkerSettings, CrawlerHintURLStatus


@fixture()
def worker_settings():
    return WorkerSettings()


@fixture()
def session_manager(worker_settings) -> SessionManager:
    return SessionManager(worker_settings.REDIS_HOST)


@fixture()
def session(session_manager):
    res = session_manager.create(1)
    yield res
    session_manager.remove(res.id)


def test_session_status(session):
    assert session.get_last_reported_status() is None

    session.set_last_reported_status(CrawlerHintURLStatus.Success)
    assert session.get_last_reported_status() == CrawlerHintURLStatus.Success
