import pexpect
import py
import pytest
import shlex
import subprocess as proc

import pytool
import tbx

mcat = {'cmd': "command not found",
        'dot_pt': ".pytool",
        'flake': "flake8 pytool test",
        'isfile': "is a file, cannot mkdir",
        'mbdir': "$HOME must be a directory",
        'mbset': "PYTOOL_DIR or HOME must be set",
        'nosuch': "No such file or directory",
        'please': "Please set PYTOOL_DIR or HOME",
        'pthelp': "pytool --help",
        'ptini': "pytool.ini",
        'skel': "produce skeletons for python programs",
        'trace': "Traceback",
        }


# -----------------------------------------------------------------------------
def test_flake8():
    """
    Scan payload and test code for lint
    """
    phandle = proc.Popen(shlex.split(mcat['flake']),
                         stdout=proc.PIPE, stderr=proc.PIPE)
    out, err = phandle.communicate()
    assert err.decode() == ""
    assert out.decode() == ""


# -----------------------------------------------------------------------------
def test_runnable():
    """
    Verify that pytool is runnable from the command line
    """
    bresult = pexpect.run("pytool --help")
    sresult = bresult.decode()
    assert "Traceback" not in sresult
    assert "command not found" not in sresult
    assert "produce skeletons for python programs" in sresult


# -----------------------------------------------------------------------------
def test_flake8():
    """
    Scan payload and test code for lint
    """
    phandle = proc.Popen(shlex.split("flake8 pytool test"),
                         stdout=proc.PIPE, stderr=proc.PIPE)
    out, err = phandle.communicate()
    assert err.decode() == ""
    assert out.decode() == ""


# -----------------------------------------------------------------------------
def test_pytool_ini_home(tmpdir):
    """
    pytool.ini_path() should accurately raise a FileNotFoundError when
    $PYTOOL_DIR is not set and $HOME does not contain .pytool/pytest.ini
    """
    homedir = tmpdir.join("home")
    with tbx.envset(HOME=homedir.strpath):
        with pytest.raises(FileNotFoundError) as err:
            path = py.path.local(pytool.ini_path())
            assert path.basename == "pytool.ini"

    assert "No such file or directory" in str(err)
    assert homedir.strpath in str(err)

# -----------------------------------------------------------------------------
def test_pytool_ini_envdir(tmpdir):
    """
    pytool.ini_path() should accurate raise a FileNotFoundError when
    $PYTOOL_DIR is set but does not contain .pytool/pytest.ini
    """
    ptdir = tmpdir.join("envdir")
    with tbx.envset(PYTOOL_DIR=tmpdir.strpath):
        with pytest.raises(FileNotFoundError) as err:
            path = py.path.local(pytool.ini_path())
            assert path.basename == "pytool.ini"

    assert "No such file or directory" in str(err)
    assert ptdir.strpath in str(err)
