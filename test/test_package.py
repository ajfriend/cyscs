def test_import():
    import scs

def test_version():
    import scs
    import pkg_resources

    print(scs.version())
    print(pkg_resources.require("scs")[0].version)
    assert scs.version() == pkg_resources.require("scs")[0].version