mcat = {'author':   "author=\"Your Name\",",
        'authmail': "author_email=\"your_address@domain.com\",",
        'callmain': "main()",
        'callstp':  "setup(name=\"PROJECT\"",
        'closep':   ")",
        'cmd':      "command not found",
        'cmdline':  "prog [-d] ARG ARG ...",
        'debug':    "-d      use the debugger",
        'defmn':    "def main():",
        'deffunc':  "def function_name(**kwa):",
        'deftest':  "def test_function():",
        'descp':    "Describe your program here",
        'describe': "Describe your project here",
        'dispatch': "dispatch(__doc__)",
        'dispon':   "@dispatch.on('cmd')",
        'divider':  ("# ---------------------------------------------"
                     "--------------------------------"),
        'dot_pt':   ".pytool",
        'empty':    "",
        'entpts':   "entry_points={'console_scripts': [proj = proj:main]}",
        'env':      "env",
        'flake':    "flake8 pytool test",
        'handle':   "print(\"Handle 'prog cmd ARGS' here\")",
        'hlpprogtxt': """
        'pytool program PATH' will create a python program at PATH. If PATH
        ends with '.py', your code will be importable. You can run your program
        with a command line like

           $ python PATH options arguments

        or by setting an alias:

           $ alias cmd='python PATH'

        which will allow you to do

           $ cmd options arguments
        """,
        'hlpprojtxt': """
        'pytool project PATH' will create a directory at PATH and drop in the
        skeleton of a python project. After creating your project, to add
        version control, you might do:

           $ cd PATH
           $ git init
           $ git add .
        """,
        'hlptooltxt': """
        'pytool tool PATH' will create a python program at PATH that has
        command line dispatchable entry points (i.e., sub-commands). pytool is
        itself such a program, using docopt-dispatch to dispatch its
        sub-commands. You can run your program with a command line like

           $ python PATH subcmd options arguments

        or by setting an alias:

           $ alias cmd='python PATH'

        which will allow you to do

           $ cmd subcmd options arguments
        """,
        'ifneqm':   "if __name__ == \"__main__\":",
        'indent':   "    ",
        'impdd':    "from docopt_dispatch import dispatch",
        'imppytst': "import pytest",
        'impstp':   "from setuptools import setup",
        'impsys':   "import sys",
        'isfile':   "is a file, cannot mkdir",
        'lchome':   "home",
        'mbdir':    "$HOME must be a directory",
        'mbset':    "PYTOOL_DIR or HOME must be set",
        'mcom':     "main entrypoint",
        'newline':  "\n",
        'nonesuch': "nonesuch",
        'nosuch':   "No such file or directory",
        'notdir':   "is not a directory",
        'options':  "Options:",
        'please':   "Please set PYTOOL_DIR or HOME",
        'prargs':   "print(sys.argv)",
        'prog_py':  "prog.py",
        'program':  "program",
        'project':  "project",
        'ptdir':    "PYTOOL_DIR",
        'pthelp':   "pytool --help",
        'pthlpcmd': "pytool help",
        'ptini':    "pytool.ini",
        'pyhelp':   "pytool help",
        'pytool':   "pytool",
        'skel':     "produce skeletons for python programs",
        'sqpt':     "[pytool]",
        'stupdir':  "Setting up config dir",
        'stupflz':  "Writing config files",
        'stupmv':   "You can move the config dir by setting $PYTOOL_DIR",
        'testdoc':  "Test function description",
        'title':    "# Project Title",
        'tmpl':     "templates",
        'tmpldir':  "templates_dir",
        'tool':     "tool",
        'tool_py':  "tool.py",
        'trace':    "Traceback",
        'triquo':   "\"\"\"",
        'uchome':   "HOME",
        'udir':     "_dir",
        'unknown':  "Unknown pytool command",
        'usage':    "Usage:",
        'where':    "print(\"This is where your code goes\")",
        'writst':   "print(\"Put your test code here\")",
        }

mcat['hlpnone'] = "{} {}".format(mcat['pyhelp'], mcat['nonesuch'])
mcat['hlpprog'] = "{} {}".format(mcat['pyhelp'], mcat['program'])
mcat['hlpproj'] = "{} {}".format(mcat['pyhelp'], mcat['project'])
mcat['hlptool'] = "{} {}".format(mcat['pyhelp'], mcat['tool'])
