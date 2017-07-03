# Albert extensions

Extensions for use with [Albert](https://albertlauncher.github.io/)

Installation
==

```
git clone https://github.com/Tyilo/albert-extensions ~/.local/share/albert/external
```

and then enable "External extensions" in Albert's settings.


If the python icon doesn't show up install it:

```
mkdir -p ~/.local/share/icons/hicolor/scalable/apps
cp python.svg ~/.local/share/icons/hicolor/scalable/apps/albert-python-evaluate.svg
```


List of extensions
==

Python eval
--

Type `py <python expression>` and see the result of the expression when evaluated in python. Press enter to copy the result to the clipboard.


Mathematica eval
--

Type `mma <mathematica expression>` and see the result of the expression when evaluated in Mathematica using wolframscript. Press enter to copy the result to the clipboard.


Pass
--

Type `pass <name>` to list [pass](https://www.passwordstore.org/) passwords. Press enter to copy the password to the clipboard.
