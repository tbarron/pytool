import pexpect

def test_runnable():
    """
    Verify that pytool is runnable from the command line
    """
    bresult = pexpect.run("pytool --help")
    sresult = bresult.decode()
    assert "Traceback" not in sresult
    assert "command not found" not in sresult
    assert "produce skeletons for python programs" in sresult
