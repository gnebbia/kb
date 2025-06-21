# Changelog
:Info: This is the changelog for kb.
:Author: gnc <nebbionegiuseppe@gmail.com>
:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE or :doc:`Appendix B <LICENSE>`.)
:Date: 2025-06-22
:Version: 0.1.1

## Version History

0.1.1 

    * Initial release.

0.1.2

    * Fixed important bugs of 0.1.1
    * Refactored
    * Added cross-platform binaries
    * Included docker image
    * Ready for pypi publishing

0.1.3

    * Added support for brew (with brew tap)
    * Fixed minor bugs
    * Fixed update mode '-e' flag
    * Fixed Windows bugs
    * Fixed cross-platforms tests
    * Improved continuous integration

0.1.4

    * Added body "-b" function in add
    * Fixed bugs related to the update function
    * Added templates
    * Added schema migration logic
    * Updated docs with a TOC

0.1.5

    * Solved minor bug related to viewing certain escape sequences
    * Added strings helping users for some exceptions
    * Implemented a faster edit/view functionality by guessing input id/title
    * Updated bash shortcuts
    * Updated Documentation

0.1.6

    * Added full path list mode (kb list -f)
    * Added rofi custom mode
    * Added grep matches mode (kb grep "string" -m)
    * Fixed important bug in grep mode
    * Added sync mode

0.1.7

    * Fixed grep bug with pull request 89
    * XDG Compliance: moving files to `$XDG_DATA_HOME/kb`, if it exists, and fall back 
      to `$HOME/.local/share/kb` if that environment variable does not exist
    * Added kb to pkgsrc
    * Added stdin functionality to add artifacts. For example:
      `cat ../script.py | python -m kb add -t mycoolscript`
      `cat path/to/script.py | python -m kb add -t mycoolscript -c python_scripts`
    * Implemented the confirmation mechanism for artifact removal
