# {# pkglts, glabpkg_dev
import costa2019


def test_package_exists():
    assert costa2019.__version__

# #}
# {# pkglts, glabdata, after glabpkg_dev

def test_paths_are_valid():
    assert costa2019.pth_clean.exists()
    try:
        assert costa2019.pth_raw.exists()
    except AttributeError:
        pass  # package not installed in editable mode

# #}
