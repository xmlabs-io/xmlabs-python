from dynaconf import Dynaconf


def test_dynaconf_settingsenv():
    settingsenv = Dynaconf(environments=True)
    assert settingsenv

def test_dynaconf_settings():
    settings = Dynaconf()
    assert settings
