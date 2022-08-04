from metabase_tools import __version__


def test_version():
    assert __version__ is not None and isinstance(__version__, str)
