def test_import():
    import cyscs

def test_version():
    import cyscs
    import pkg_resources

    # checks the *wrapper* version, but not the underlying C SCS version.
    assert cyscs.version() == pkg_resources.require("cyscs")[0].version