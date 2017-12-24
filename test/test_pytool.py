import pexpect
import pytest
import shlex
import subprocess as proc


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
    """
    phandle = proc.Popen(shlex.split("flake8 pytool test"),
                         stdout=proc.PIPE, stderr=proc.PIPE)
    out, err = phandle.communicate()
    assert err.decode() == ""
    assert out.decode() == ""


# -----------------------------------------------------------------------------
def test_pytool_init(tmpdir):
    """

    """
    pytest.fail('construction')
