def test_import():
    import cyscs

def test_version():
    import cyscs
    import pkg_resources

    assert cyscs.version() == pkg_resources.require("cyscs")[0].version