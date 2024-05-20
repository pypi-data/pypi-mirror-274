# {# pkglts, glabpkg_dev
import escalona2003


def test_package_exists():
    assert escalona2003.__version__

# #}
# {# pkglts, glabdata, after glabpkg_dev

def test_paths_are_valid():
    assert escalona2003.pth_clean.exists()
    try:
        assert escalona2003.pth_raw.exists()
    except AttributeError:
        pass  # package not installed in editable mode

# #}
