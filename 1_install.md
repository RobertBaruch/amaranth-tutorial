# Install

## Install all the things

> TODO: Take a look at [YosysHQ/oss-cad-suite-build](https://github.com/YosysHQ/oss-cad-suite-build) which seems to contain All The Things and then some, and also seems to be updated very often.

## Follow the directions

The installation instructions are on the [Amaranth HDL Installation page](https://amaranth-lang.org/docs/amaranth/latest/install.html).

This involves installing Python 3.7 or above, [gtkwave](https://sourceforge.net/projects/gtkwave/), and Amaranth itself. Click on the operating system you're using, and the appropriate command line is shown. Choose either the latest release or the development snapshot. As usual, development snapshots may have fixed bugs that still exist in the latest release, but also might have introduced new bugs.

## Tip for vscode users

Open File > Preferences > Settings, look for pylint args, and add:

```txt
--contextmanager-decorators=contextlib.contextmanager,nmigen.hdl.dsl._guardedcontextmanager
```

This is because pylint doesn't recognize that `nmigen.hdl.dsl._guardedcontextmanager` is a valid context manager. Otherwise pylint will complain for every `with m.If` statement.
