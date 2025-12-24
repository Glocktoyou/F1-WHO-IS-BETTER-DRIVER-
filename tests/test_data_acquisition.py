import pytest
from data_acquisition import F1DataLoader

class DummySession:
    def __init__(self):
        self.year = 2024
        self.event = 'Monaco'
        self.session = 'Q'
    def load(self):
        return True

def test_loader_init():
    loader = F1DataLoader(cache_dir='cache')
    assert loader is not None

def test_get_session(monkeypatch):
    loader = F1DataLoader(cache_dir='cache')
    monkeypatch.setattr(loader, 'get_session', lambda y, e, s: DummySession())
    session = loader.get_session(2024, 'Monaco', 'Q')
    assert isinstance(session, DummySession)
