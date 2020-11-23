## Frequently Asked Questions

## Troubleshooting

#### I get the error:
`` 
File "----------/.pyenv/versions/3.X.Y/lib/pythonX.Ysite-packages/kb_manager-0.U.V-pyX.Y.egg/kb/commands/grep.py", line 66, in grep
printer.print_grep_matches(artifact_names)
TypeError: print_grep_matches() missing 1 required positional argument: 'hits_list'
``

If you are using a version of kb 0.1.5 or lower, (you can check by using ``kb --version`` ) then this feature was not completely implemented. Check the latest version of the kb software to check if the functionality has been implemented.

#### I see the following: 
`` ModuleNotFoundError: No module named '_sqlite3'``

Some versions of Python do not have the **Python sqlite3 bindings library** compiled in. The solution here depends on the OS in use - become root and install the corrosponding Python version sqlite3 package.
For example:

for NetBSD+Python3.7 : ``doas pkgin install py37-sqlite3``
