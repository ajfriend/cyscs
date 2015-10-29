def test_import():
    import scs

def test_version():
    import scs
    import pkg_resources

    assert scs.version() == pkg_resources.require("scs")[0].version