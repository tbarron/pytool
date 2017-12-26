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

## Practices

### Non-flakey Code

I use the following test to check my code for flakiness:

        # -----------------------------------------------------------------------------
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


