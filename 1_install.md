# Install

## Install all the things

> It's unfortunate that installation of everything you need isn't a one-click process... although [FPGAWars' Apio](http://fpgawars.github.io/) goes a long way towards doing this. I just think that while yosys and Amaranth HDL are undergoing constant positive updates, Apio doesn't keep up with them. In the meantime, we just install all the tools separately.

## Follow the directions

The installation instructions are on the [Amaranth HDL Installation page](https://amaranth-lang.org/docs/amaranth/latest/install.html).

This involves installing Python 3.7 or above, [gtkwave](https://sourceforge.net/projects/gtkwave/), and Amaranth itself. Click on the operating system you're using, and the appropriate command line is shown. Choose either the latest release or the development snapshot. As usual, development snapshots may have fixed bugs that still exist in the latest release, but also might have introduced new bugs.

## Tip for vscode users

Open File > Preferences > Settings, look for pylint args, and add:

```txt
--contextmanager-decorators=contextlib.contextmanager,nmigen.hdl.dsl._guardedcontextmanager
```

This is because pylint doesn't recognize that `nmigen.hdl.dsl._guardedcontextmanager` is a valid context manager. Otherwise pylint will complain for every `with m.If` statement.
