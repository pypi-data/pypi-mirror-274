# Simple facilities to load GTK '.ui' files in Python


The 'gtk_simple_loader' package provides very simple facilities to load '.ui' files like the ones exported by
[Cambalache][cambalache]. This module works with GTK 4.0 and higher.


## Overview

This module simplifies the loading of simple GTK widgets from '.ui' files. It automatizes some common tasks like load the objects from the
'.ui' file and connect the 'activate' signal to the 'on_activate_handler' method.

With the default approach, when loading the GTK widgets from '.ui' files with `Gtk.Builder`, you need to manually add the files to the
`Gtk.Builder` instance and get each widget object with `Gtk.Builder.get_object()`. If the user interface file contains multiple widgets,
this can be a tedious task and result in a large code like the following:

```python
class App(Gtk.Application):
    def __init__(self, **kwargs: Unpack[AppKwargsTypes]) -> None:
        super().__init__(**kwargs)
        self.connect("activate", self.on_activate_handler)

    def on_activate_handler(self, app: Gtk.Application) -> None:  # noqa: ARG002
        # Configures the bulder to get the objects from the '.ui' file
        self._builder = Gtk.Builder(self)
        self._builder.add_from_file("examples/interface.ui")

        # Gets the objects from the '.ui' file
        self.main_window = self._builder.get_object("main_window")
        self.box_1 = self._builder.get_object("box_1")
        self.entry_1 = self._builder.get_object("entry_1")
        self.scale_1 = self._builder.get_object("scale_1")
        self.button_1 = self._builder.get_object("button_1")
        self.switch_1 = self._builder.get_object("switch_1")
        self.button_2 = self._builder.get_object("button_2")

        # Configures the main window and the shows it
        self.main_window.set_application(self)
        self.main_window.present()
```

With 'gtk_simple_loader' module, you can replace the above code by the following:

```python
@gtk_simple_loader.builder.load_from_files(["examples/interface.ui"])
class App(Gtk.Application):
    def on_activate_handler(self, app: Gtk.Application) -> None:  # noqa: ARG002
        self.main_window.present()
```

Because the first core has many lines that load objects, and this module automatizes it, the reduction was significant. With codes that
have fewer objects and more callbacks, this reduction will not be so significant.


### Static typing

You can apply static typing to the above examples. In these case, you will need to manually add the Type Hints to the objects.
So code without 'gtk_simple_loader' and with it will look similar and rave a similar number of lines.

Without 'gtk_simple_loader':

```python
class AppKwargsTypes(TypedDict):
    """Types for the Application keyword arguments."""

    application_id: str


class App(Gtk.Application):
    """Simple example that shows how to load a '.ui' file and create a window."""

    def __init__(self, **kwargs: Unpack[AppKwargsTypes]) -> None:
        """Initialize the application."""
        super().__init__(**kwargs)
        self.connect("activate", self.on_activate_handler)

    def on_activate_handler(self, app: Gtk.Application) -> None:  # noqa: ARG002
        """Show the window.

        Called when the application is launched.

        Parameters
        ----------
        app : Gtk.Application
            The application object (equal to *self* in this context).

        """
        # Configures the bulder to get the objects from the '.ui' file
        self._builder = Gtk.Builder(self)
        self._builder.add_from_file("examples/interface.ui")

        # Gets the objects from the '.ui' file
        self.main_window = cast(Gtk.Window, self._builder.get_object("main_window"))
        self.box_1 = cast(Gtk.Box, self._builder.get_object("box_1"))
        self.entry_1 = cast(Gtk.Entry, self._builder.get_object("entry_1"))
        self.scale_1 = cast(Gtk.Scale, self._builder.get_object("scale_1"))
        self.button_1 = cast(Gtk.Button, self._builder.get_object("button_1"))
        self.switch_1 = cast(Gtk.Switch, self._builder.get_object("switch_1"))
        self.button_2 = cast(Gtk.ToggleButton, self._builder.get_object("button_2"))

        # Configures the main window and the shows it
        self.main_window.set_application(self)
        self.main_window.present()
```

With 'gtk_simple_loader':

```python
@gtk_simple_loader.builder.load_from_files(["examples/interface.ui"])
class App(Gtk.Application):
    """Simple example that shows how to load a '.ui' file and create a window."""

    def on_activate_handler(self, app: Gtk.Application) -> None:  # noqa: ARG002
        """Show the window.

        Called when the application is launched.

        Parameters
        ----------
        app : Gtk.Application
            The application object (equal to *self* in this context).

        """
        self.main_window: Gtk.Window
        self.box_1: Gtk.Box
        self.entry_1: Gtk.Entry
        self.scale_1: Gtk.Scale
        self.button_1: Gtk.Button
        self.switch_1: Gtk.Switch
        self.button_2: Gtk.ToggleButton

        self.main_window.present()
```

In terms of code, there are a little less lines, but is more readable. Does not use the `cast` function or the `Unpack` type hinting.

A complete example of these codes can be found in the [examples/](examples/) folder.


### Signal handlers

This module does not affect the signal handlers of the source code. This part of the code is equal to a code with 'gtk_simple_loader' and
without it. The only facility is that the 'activate' signal will be automatically connected to the 'on_activate_handler' method.

With GTK 4.0 and higher, the `Gtk.BUilder` automatically connects the signal handlers of the interfaces files to the application instance.
You only need to provide it when creating the builder:

```python
self._builder = Gtk.Builder(self)                     # Providing the Gtk.Application instance to the builder
self._builder.add_from_file("examples/interface.ui")  # Loading the interface (signals are connected automatically)
```


## Building

The building process use some bash scripts and Makefile, these will work fine a practically every Linux distribution. If you use Windows,
maybe you will need to adjust the [scripts/](scripts/) and the [Makefile](Makefile) to your environment.

Otherwise, just run:

```shell
make build
```


## Installation

You need to install [PyGObject][pygobject] by yourself. There are not an official [PyPI][pypi]
package to it.


### Local installation

Just run:

```shell
make install
```


## Creating interfaces

This module works fine with the user interface files generated by [Cambalache][cambalache]. The object name is
retrieved from the `id` attribute of the widget in the interface using the
[`get_buildable_id()`](https://docs.gtk.org/gtk4/method.Buildable.get_buildable_id.html) method. This will get the 'id' attribute of the
`<object>` tag. In a [Cambalache][Cambalache] project, you only need to set the 'Object id' in the interface.

This example will load the window with the 'main_window' id as 'self.main_window' in the application instance:

![Cambalache-example](img/example-cambalache.png)

A [more complex example](examples/simple_window.py) is available at [examples/](examples/) folder.


## Development

This project uses [Python LSP Server](https://github.com/python-lsp/python-lsp-server) with the
[Mypy plugin for PYLSP](https://github.com/python-lsp/pylsp-mypy) and [python-lsp-ruff](https://github.com/python-lsp/python-lsp-ruff)
plugins. I could not set up [Pyright](https://github.com/microsoft/pyright) to work fine with GTK. Maybe because the
GTK module makes some manipulation to be possible to load different GTK versions.

The HTML documentation is build with [Sphinx](https://www.sphinx-doc.org/en/master/) and its configuration is available at the
[sphinx/](sphinx/) folder. In the docstrings of the source code, you can add these extra field lists:

```python
"""
:issue:`1234` -> Shows the issue 1234 in the generated documentation (creates a hyperlink).
:pull:`1234` -> Shows the pull request 1234 in the generated documentation (creates a hyperlink).
"""
```


<!-- References -->
[cambalache]: https://gitlab.gnome.org/jpu/cambalache 'Cambalache'
[pygobject]: https://pygobject.gnome.org/index.html 'PyGObject'
[pypi]: https://pypi.org/ 'PyPI'
