# pytool

This program provides an easy way to set up

 * stand-alone python programs,
 * stand-alone python programs that contain command line accessible
   sub-functions (tool structure), and
 * complete setup.py-based python projects

It used to be part of the
[backscratcher](https://github.com/tbarron/backscratcher) collection.

After the first time you run pytool, you will find a directory of templates
in $HOME/.pytool (you can put this somewhere else by setting PYTOOL_DIR
before running pytool).

Make sure to edit $HOME/.pytool/templates/prjdir/setup.py to set your
author name and e-mail address.

## Usage

### Stand-alone Program

    pytool program PATH

The following code is written into the file at PATH:

    """
    Describe your program here
    """
    import sys


    # -----------------------------------------------------------------------------
    def main():
        """
        main entrypoint
        """
        print(sys.argv)
        print("This is where your code goes")


    # -----------------------------------------------------------------------------
    if __name__ == "__main__":
        main()

### Tool-style Program (using docopt-dispatch)

    pytool tool PATH

The following code is written into the file at PATH:

    """
    Usage:
        prog cmd [-d] ARG ARG ...

    Options:
        -d      use the debugger
    """
    from docopt_dispatch import dispatch
    import sys

    # -----------------------------------------------------------------------------
    def main():
        """
        main entrypoint
        """
        dispatch(__doc__)

    # -----------------------------------------------------------------------------
    @dispatch.on('cmd')
    def function_name(**kwa):
        print("Handle 'prog cmd ARGS' here")

    # -----------------------------------------------------------------------------
    if __name__ == "__main__":
        main()


### Full Python Layout Project

    pytool progject PATH

The following files are written into the directory at PATH:

    PATH
     |
     +- setup.py
     |
     +- README.py
     |
     +- pytest.ini
     |
     +- PATH
     |   |
     |   +- __init__.py
     |
     +- test
         |
         +- test_stub.py


## Practices

### Avoiding Flaky Code

I use the following test to check my code for flakiness:

    def test_flake8():
        """
        Scan payload and test code for lint
        """
        pytest.dbgfunc()
        phandle = proc.Popen(shlex.split(mcat['flake']),
                             stdout=proc.PIPE, stderr=proc.PIPE)
        out, err = phandle.communicate()
        assert err.decode() == ""
        assert out.decode() == ""

By running this test first (i.e., it's positioned so it's the first thing
pytest discovers), I get quick feedback on my code quality. If any flakes
creep into the code, my test suite lets me know.


### Debug access during testing

Often it's helpful to be able to break into the debugger while running
tests. See conftest.py in the test directory for how this is set up.

In the main test file (test_pytool.py), I have an autouse fixture that
actually uses the hook set up in conftest.py:

    @pytest.fixture(autouse=True)
    def fx_debug(request):
        """
        Call the debug function set up in conftest.py
        """
        print("'b request.function' to stop in the target test")
        pytest.dbgfunc()

With this in place, putting '--dbg <testname>' on the py.test command line
will fire up the debugger when we hit the fixture for the specified test.
The argument to --dbg can be a partial test name and all matched tests will
get a debugger invocation. Or the argument to --dbg can be 'all' and the
debugger will be started for every test.

When the debugger starts up in the fixture, a break point can be set in the
target test by issuing the command 'b request.function'.

### Test for Deployability

There are several things that should be true if my repository is ready for
deployment:

 * There should not be any outstanding untracked files. Everything should
   either be committed or listed in .gitignore.
 * The version specified in version.py should match the most recent git
   tag.
 * The commit indicated by the most recent tag should match HEAD.

These are all things that can be checked in a test.

    def test_deployable():
        """
        Check current version against last git tag and check for outstanding
        untracked files
        """
        r = Repo('.')
        # Check for untracked files
        assert [] == r.untracked_files, "You have untracked files"

        # Check for staged but uncommitted updates
        assert [] == r.index.diff(r.head.commit), "You have staged updates"

        # Check for uncommitted updates
        assert [] == r.index.diff(None), "You have uncommited changes"

        # Check that the current version matches the latest tag
        assert version._v == str(r.tags[-1]), "Version does not match tag"

        # Check that the latest tag points at HEAD
        assert str(r.head.commit) == str(r.tags[-1].commit), "Tag != HEAD"
