import py
import pytest
import re

import pytool
from pytool.msgcat import mcat
from pytool import version
import tbx


# -----------------------------------------------------------------------------
def test_flake8():
    """
    Scan payload and test code for lint
    """
    result = tbx.run(mcat['flake'])
    assert "" == result.decode()


# -----------------------------------------------------------------------------
def test_runnable():
    """
    Verify that pytool is runnable from the command line
    """
    bresult = tbx.run(mcat['pthelp'])
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
        cdir, src = pytool.cfgdir()
        assert cdir == ptdir.strpath
        assert src == "env"


# -----------------------------------------------------------------------------
def test_pytool_cfgdir_justhome_nosuch(tmpdir):
    """
    pytool.cfgdir should return PYTOOL_DIR if set, else HOME/.pytool if HOME
    set, else throw tbx.Error('PYTOOL_DIR or HOME must be set')
    """
    hdir = tmpdir.join("homedir")
    ptdir = hdir.join(".pytool")
    with tbx.envset(PYTOOL_DIR=None, HOME=hdir.strpath):
        cdir, src = pytool.cfgdir()
        assert cdir == ptdir.strpath
        assert src == "home"


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
        cdir, src = pytool.cfgdir()
        assert cdir == ptdir.strpath
        assert src == "env"


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
def test_pytool_load_cfg_nosuch(tmpdir):
    """
    Attempting to load config from no such file should get FileNotFoundError
    """
    wdir = tmpdir.join("pytool")
    ptini = wdir.join("pytool.ini")
    with tbx.envset(PYTOOL_DIR=wdir.strpath):
        with pytest.raises(FileNotFoundError) as err:
            cfg = pytool.load_config()
            assert cfg is not None
    assert ptini.strpath in str(err)


# -----------------------------------------------------------------------------
def test_pytool_load_cfg_exist(tmpdir):
    """
    Attempting to load config from a real file should work
    """
    wdir = tmpdir.join(mcat['pytool'])
    tdir = wdir.join(mcat['tmpl'])
    with tbx.envset(PYTOOL_DIR=wdir.strpath):
        pytool.setup_config_dir()
        cfg = pytool.load_config()
        assert mcat['pytool'] in cfg.sections()
        assert mcat['tmpldir'] in cfg.options(mcat['pytool'])
        assert cfg.get('pytool', 'templates_dir') == tdir.strpath


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


# -----------------------------------------------------------------------------
def test_pytool_initialize_envdir_scratch(tmpdir, fx_tmpl):
    """
    With PYTOOL_DIR set but the directory not existing, pytool.initialize()
    should mkdir $PYTOOL_DIR, then write $PYTOOL_DIR/pytool.ini,
    .../templates/, etc.
    """
    ptdir = tmpdir.join("envdir")
    with tbx.envset(PYTOOL_DIR=ptdir.strpath):
        pytool.initialize()
    assert ptdir.isdir()
    for item in fx_tmpl:
        assert ptdir.join(item).exists()


# -----------------------------------------------------------------------------
def test_pytool_initialize_envdir_create(tmpdir, fx_tmpl):
    """
    With PYTOOL_DIR set and created, pytool.initialize() should create
    pytool.ini, templates/, etc.
    """
    ptdir = tmpdir.join("envdir")
    ptdir.ensure(dir=True)
    with tbx.envset(PYTOOL_DIR=ptdir.strpath):
        pytool.initialize()
    for item in fx_tmpl:
        assert ptdir.join(item).exists()


# -----------------------------------------------------------------------------
def test_pytool_initialize_envdir_isfile(tmpdir):
    """
    With PYTOOL_DIR set and pointed at a file, pytool.initialize() should throw
    an exception indicating that $PYTOOL_DIR is a file, not a directory.
    """
    ptdir = tmpdir.join("envdir")
    ptdir.ensure()
    with tbx.envset(PYTOOL_DIR=ptdir.strpath):
        with pytest.raises(FileExistsError) as err:
            pytool.initialize()
    assert ptdir.strpath in str(err)
    assert mcat['isfile'] in str(err)


# -----------------------------------------------------------------------------
def test_pytool_initialize_homedir_scratch(tmpdir):
    """
    If HOME is set but the directory does not exist, this implies an
    incompletely created user. The program should throw FileNotFoundError for
    $HOME.
    """
    hdir = tmpdir.join("home")
    with tbx.envset(HOME=hdir.strpath):
        with pytest.raises(FileNotFoundError) as err:
            pytool.initialize()
    assert hdir.strpath in str(err)
    assert mcat['notdir'] in str(err)


# -----------------------------------------------------------------------------
def test_pytool_initialize_homedir_create(tmpdir, fx_tmpl):
    """
    With PYTOOL_DIR unset, HOME set and existing, but no .pytool directory in
    place, pytool.initialize() should create $HOME/.pytool, and write
    pytool.ini in it along with all the other templates.
    """
    hdir = tmpdir.join("home")
    hdir.ensure(dir=True)
    ptdir = hdir.join(mcat['dot_pt'])
    with tbx.envset(HOME=hdir.strpath):
        pytool.initialize()
    for item in fx_tmpl:
        assert ptdir.join(item).exists()


# -----------------------------------------------------------------------------
def test_pytool_initialize_homedir_isfile(tmpdir):
    """
    If HOME is a file, pytool.initialize() should throw a FileExistsError
    """
    hdir = tmpdir.join("home")
    hdir.ensure(dir=False)
    with tbx.envset(HOME=hdir.strpath):
        with pytest.raises(FileExistsError) as err:
            pytool.initialize()
    assert hdir.strpath in str(err)
    assert mcat['isfile'] in str(err)


# -----------------------------------------------------------------------------
def test_pytool_initialize_homedir_pt_isfile(tmpdir):
    """
    If HOME/.pytool is a file, pytool.initialize() should throw a
    FileExistsError
    """
    hdir = tmpdir.join("home")
    hdir.ensure(dir=True)
    ptdir = hdir.join(mcat['dot_pt'])
    ptdir.ensure(dir=False)
    with tbx.envset(HOME=hdir.strpath):
        with pytest.raises(FileExistsError) as err:
            pytool.initialize()
    assert ptdir.strpath in str(err)
    assert mcat['isfile'] in str(err)


# -----------------------------------------------------------------------------
def test_version():
    """
    Test 'pytool version'
    """
    result = tbx.run("pytool version")
    assert mcat['trace'] not in result.decode()
    assert re.findall("pytool version \d+\.\d+\.\d+", result.decode())


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("func, snips", [
    (pytool.file_pytool_ini, ['tmpl', 'udir', ]),
    (pytool.file_prog_py,  ['impsys', 'defmn', 'triquo', 'where',
                            'ifneqm', 'callmain']),
    (pytool.file_tool_py,  ['usage', 'cmdline', 'triquo', 'options', 'debug',
                            'impdd', 'impsys', 'defmn', 'where']),
    (pytool.file_init_py,  ['impsys', 'defmn', 'triquo', 'where',
                            'ifneqm', 'callmain']),
    (pytool.file_readme,   ['title',
                            'describe', ]),
    (pytool.file_setup_py, ['impstp', 'callstp', 'author', 'authmail',
                            'entpts', 'closep']),
    (pytool.file_test_stub_py, ['imppytst', 'deftest', 'triquo', 'testdoc',
                                'writst'])
    ])
def test_content(func, snips):
    """
    Check the content produced by file_readme()
    """
    content = func()
    assert type(content) == str
    for item in snips:
        assert mcat[item] in content


# -----------------------------------------------------------------------------
def test_deployable():
    """
    Check current version against last git tag and check for outstanding
    untracked files
    """
    result = tbx.run("git status --porc")
    assert "" == result.decode()

    result = tbx.run("git tag")
    tagl = result.decode().split("\n")
    assert version._v == tagl[-1]


# -----------------------------------------------------------------------------
@pytest.fixture(autouse=True)
def fx_debug(request):
    """
    """
    print("'b request.function' to stop in the target test")
    pytest.dbgfunc()


# -----------------------------------------------------------------------------
@pytest.fixture
def fx_tmpl():
    """
    Return a list of files and directories expected in the pytool config dir
    """
    rval = ["pytool.ini",
            "templates",
            "templates/prog.py",
            "templates/tool.py",
            "templates/prjdir",
            "templates/prjdir/setup.py",
            "templates/prjdir/README.md",
            "templates/prjdir/prjdir/__init__.py",
            "templates/prjdir/test/test_stub.py"
            ]
    return(rval)
