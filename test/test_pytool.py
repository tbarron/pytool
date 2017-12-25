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
    bresult = pexpect.run(mcat['pthelp'])
    sresult = bresult.decode()
    assert mcat['trace'] not in sresult
    assert mcat['cmd'] not in sresult
    assert mcat['skel'] in sresult


# -----------------------------------------------------------------------------
def test_pytool_cfgdir_neither():
    """
    pytool.cfgdir should return PYTOOL_DIR if set, else HOME/.pytool if HOME
    set, else throw tbx.Error('PYTOOL_DIR or HOME must be set')
    """
    with tbx.envset(PYTOOL_DIR=None, HOME=None):
        with pytest.raises(FileNotFoundError) as err:
            pytool.cfgdir()
    assert mcat['please'] in str(err)


# -----------------------------------------------------------------------------
def test_pytool_cfgdir_justpt_nosuch(tmpdir):
    """
    pytool.cfgdir should return PYTOOL_DIR if set, else HOME/.pytool if HOME
    set, else throw tbx.Error('PYTOOL_DIR or HOME must be set')
    """
    ptdir = tmpdir.join("envdir")
    with tbx.envset(PYTOOL_DIR=ptdir.strpath, HOME=None):
        assert pytool.cfgdir() == ptdir.strpath


# -----------------------------------------------------------------------------
def test_pytool_cfgdir_justhome_nosuch(tmpdir):
    """
    pytool.cfgdir should return PYTOOL_DIR if set, else HOME/.pytool if HOME
    set, else throw tbx.Error('PYTOOL_DIR or HOME must be set')
    """
    hdir = tmpdir.join("homedir")
    ptdir = hdir.join(".pytool")
    with tbx.envset(PYTOOL_DIR=None, HOME=hdir.strpath):
        assert pytool.cfgdir() == ptdir.strpath


# -----------------------------------------------------------------------------
def test_pytool_cfgdir_both(tmpdir):
    """
    pytool.cfgdir should return PYTOOL_DIR if set, else HOME/.pytool if HOME
    set, else throw tbx.Error('PYTOOL_DIR or HOME must be set')

    With both PYTOOL_DIR and HOME set, cfgdir should return PYTOOL_DIR
    """
    ptdir = tmpdir.join("envdir")
    hdir = tmpdir.join("homedir")
    with tbx.envset(PYTOOL_DIR=ptdir.strpath, HOME=hdir.strpath):
        assert pytool.cfgdir() == ptdir.strpath


# -----------------------------------------------------------------------------
def test_pytool_ini_unset(tmpdir):
    """
    Neither PYTOOL_DIR nor HOME is set. Should get 'Please set PYTOOL_DIR or
    HOME', thrown by cfgdir()
    """
    with tbx.envset(HOME=None, PYTOOL_DIR=None):
        with pytest.raises(FileNotFoundError) as err:
            path = py.path.local(pytool.ini_path())
            assert path.basename == mcat['ptini']
    assert mcat['please'] in str(err)


# -----------------------------------------------------------------------------
def test_pytool_ini_home_nodir(tmpdir):
    """
    pytool.ini_path() should accurately raise a FileNotFoundError when
    $PYTOOL_DIR is not set and $HOME does not contain .pytool/pytest.ini

    What about $HOME exists but .pytool does not?
    What about $HOME/.pytool exists but pytool.ini does not?
    """
    homedir = tmpdir.join("home")
    ptdir = homedir.join(".pytool")
    with tbx.envset(HOME=homedir.strpath):
        with pytest.raises(FileNotFoundError) as err:
            path = py.path.local(pytool.ini_path())
            assert path.basename == mcat['ptini']
    assert mcat['nosuch'] in str(err)
    assert ptdir.strpath in str(err)


# -----------------------------------------------------------------------------
def test_pytool_ini_home_no_pt(tmpdir):
    """
    $HOME exists but subdir .pytool does not. ini_path should raise
    FileNotFoundError
    """
    homedir = tmpdir.join("home")
    homedir.ensure(dir=True)
    ptdir = homedir.join(".pytool")
    with tbx.envset(HOME=homedir.strpath):
        with pytest.raises(FileNotFoundError) as err:
            path = py.path.local(pytool.ini_path())
            assert path.basename == mcat['ptini']
    assert mcat['nosuch'] in str(err)
    assert ptdir.strpath in str(err)


# -----------------------------------------------------------------------------
def test_pytool_ini_home_noini(tmpdir):
    """
    $HOME exists, subdir .pytool exists, pytool.ini not present
    """
    homedir = tmpdir.join("home")
    ptdir = homedir.join(".pytool")
    ptdir.ensure(dir=True)
    with tbx.envset(HOME=homedir.strpath):
        with pytest.raises(FileNotFoundError) as err:
            path = py.path.local(pytool.ini_path())
            assert path.basename == mcat['ptini']
    assert mcat['nosuch'] in str(err)
    assert ptdir.strpath in str(err)


# -----------------------------------------------------------------------------
def test_pytool_ini_home_found(tmpdir):
    """
    $HOME exists, subdir .pytool exists, pytool.ini is present, should return
    path for pytool.ini
    """
    homedir = tmpdir.join("home")
    ptdir = homedir.join(".pytool")
    ptfile = ptdir.join("pytool.ini")
    ptfile.ensure(dir=False)
    with tbx.envset(HOME=homedir.strpath):
        path = py.path.local(pytool.ini_path())
        assert path.basename == mcat['ptini']
        assert path.strpath == ptfile.strpath


# -----------------------------------------------------------------------------
def test_pytool_ini_envdir_nodir(tmpdir):
    """
    pytool.ini_path() should accurately raise a FileNotFoundError when
    $PYTOOL_DIR is set but does not contain pytest.ini
    """
    ptdir = tmpdir.join("envdir")
    with tbx.envset(PYTOOL_DIR=ptdir.strpath):
        with pytest.raises(FileNotFoundError) as err:
            path = py.path.local(pytool.ini_path())
            assert path.basename == mcat['ptini']
    assert mcat['nosuch'] in str(err)
    assert ptdir.strpath in str(err)


# -----------------------------------------------------------------------------
def test_pytool_ini_envdir_nofile(tmpdir):
    """
    pytool.ini_path() should accurately raise a FileNotFoundError when
    $PYTOOL_DIR is set but does not contain pytest.ini

    What about $PYTOOL_DIR exists but pytool.ini does not?
    """
    ptdir = tmpdir.join("envdir")
    ptdir.ensure(dir=True)
    with tbx.envset(PYTOOL_DIR=ptdir.strpath):
        with pytest.raises(FileNotFoundError) as err:
            path = py.path.local(pytool.ini_path())
            assert path.basename == mcat['ptini']
    assert mcat['nosuch'] in str(err)
    assert ptdir.strpath in str(err)


# -----------------------------------------------------------------------------
def test_pytool_ini_envdir_found(tmpdir):
    """
    pytool.ini_path() should return the path of pytool.ini in directory
    $PYTOOL_DIR if it's there.
    """
    ptdir = tmpdir.join("envdir")
    ptini = ptdir.join("pytool.ini")
    ptini.ensure(dir=False)
    with tbx.envset(PYTOOL_DIR=ptdir.strpath):
        path = py.path.local(pytool.ini_path())
        assert path.basename == mcat['ptini']
        assert path.strpath == ptini.strpath


# -----------------------------------------------------------------------------
def test_pytool_setup_config_dir(tmpdir, fx_tmpl):
    """
    pytool.setup_config_dir() should create cfgdir() if necessary then populate
    it
    """
    ptdir = tmpdir.join("envdir")
    with tbx.envset(PYTOOL_DIR=ptdir.strpath):
        pytool.setup_config_dir()
    for item in fx_tmpl:
        assert ptdir.join(item).exists()




    assert mcat['isfile'] in str(err)


    assert mcat['mbdir'] in str(err)


    assert mcat['isfile'] in str(err)


    ptdir = hdir.join(mcat['dot_pt'])
    assert mcat['isfile'] in str(err)


