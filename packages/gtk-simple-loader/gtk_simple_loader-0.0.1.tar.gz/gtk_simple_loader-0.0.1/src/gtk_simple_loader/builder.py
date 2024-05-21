"""Functions to load GTK libraries easily.

To load all objects from Gtk.Builder to a file, use the
:func:`load_objects_from_builder()` function.

To create a Gtk.Builder from '.ui' files, use the
:func:`get_builder_from_files()`

To load all objects from Gtk.Builder to a class, use the
:func:`load_from_files()` decorator in the class.
"""


from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, TypeVar, cast

if TYPE_CHECKING:
    from collections.abc import Callable

from gi.repository import GObject, Gtk


def load_objects_from_builder(
        parent: GObject.GObject, builder: Gtk.Builder) -> list[str]:
    """Load objects from a Gtk.Builder in a parent object.

    Attempt to load all objects inside the Gtk.Builder. First tries to load by the
    'buildable_id' as if the object is a widget (uses the `get_buildable_id()` method).
    If not possible, try to load by the 'name' property. Saves the widget object as
    *parent.<buildable_id>*, or *parent.<name>* if the 'buildable_id' can not be loaded.

    Before to call this function, you need to manually add the '.ui' files to the
    builder with its 'add_from_file()' method.

    When more than one object has the same name, it will throw a warning message.

    You should not use this function more than once with the same builder. Some objects
    will be overwritten, and this function will throw a warning message.

    Parameters
    ----------
    parent : GObject.GObject
        The objects loaded from the builder will be saved in this object.

    builder : Gtk.Builder
        The GTK builder object that will load the objects.

    Returns
    -------
    list[str]
        The list of names of the objects that were loaded.

    """
    objects = builder.get_objects()
    objects_names: list[str] = []

    for obj in objects:
        widget_id: str| None

        try:
            # Try to get the 'widget_id' by the 'get_buildable_id()' method. Only works
            # with widgets. Otherwise, causes a AttributeError
            widget = cast(Gtk.Widget, obj)
            widget_id = widget.get_buildable_id()

        except AttributeError:  # 'obj' is not a widget
            try:
                widget_id = obj.get_property("name")

            except TypeError:  # No 'name' property found in the object
                widget_id = None

        # If there are not a 'widget_id' property, `widget_id` is an empty string. If
        # there are a 'widget_id' property, but it is not specified, it is also an
        # empty string
        if widget_id is not None and widget_id[0:2] != "___":
            objects_names.append(widget_id)

            if hasattr(parent, widget_id):
                logging.warning(
                    "Object '%s' already exists, skipping.\n"
                    "\tThere are more that one object with the same widget_id.\n"
                    "\tTry to change the property 'widget_id' in the '.ui' file.",
                    widget_id)
            else:
                setattr(parent, widget_id, obj)

    return objects_names


def load_builder_from_files(
        parent: GObject.GObject, filenames: list[str], *, load_obj: bool = True,
    ) -> tuple[Gtk.Builder, list[str]]:
    """Get a Gtk.Buider and load all GTK libraries from a '.ui' file.

    The created Gtk.Builder will be bind to the *parent* object. But it will not be
    included in the *parent* object. If you want this, you need to manually add it:

    .. code-block:: python

        parent._builder, parent._obj_names = get_builder_from_files(parent, filenames)

    If *load* is True, the builder will load all objects inside the '.ui' files
    with the :func:`load_objects_from_builder()` function when the application is
    launched.

    If using GTK4, All the handlers in the provided '.ui' files will be
    automatically connected to the methods in *parent*. They need to have the same name.
    E.g. If there are a handler named 'on_button_clicked' in a '.ui' file, it will be
    connected to the *parent.on_button_clicked* method. This is a default GTK4 feature.

    Parameters
    ----------
    parent : GObject.GObject
        The parent object. Where the Gtk.Builder will be bind.

    filenames : list[str]
        The list of '.ui' files to load.

    load_obj : bool
        Whether to load the objects from the builder in *parent* or not.

    Returns
    -------
    Gtk.Builder
        The GTK builder object with all the '.ui' files added
        (with Gtk.Builder.add_from_file() function).

    list[str]
        The list of names of the objects that were automatically loaded. If *load_obj*
        is False, this list will be empty.

    """
    builder = Gtk.Builder(parent)
    object_names: list[str] = []

    for file in filenames:
        builder.add_from_file(file)

    if load_obj:
        object_names = load_objects_from_builder(parent, builder)

    return builder, object_names


# Type checking variables and classes
if TYPE_CHECKING:
    class Class:
        """Base class to load GTK libraries."""

        nothing = None

    UILoadedClass = TypeVar("UILoadedClass")


def set_windows_application(
        app: Gtk.Application, parent: GObject.GObject,
        window_names: list[str]) -> None:
    """Set the application associated with the windows in the parent object.

    Parameters
    ----------
    app : Gtk.Application
        The application object.

    parent : GObject
        Object with the windows.

    window_names : list[str]
        The list of names of the windows that will be set.

    """
    window_objs = [getattr(parent, name) for name in window_names]

    for window_obj in window_objs:
        window_obj.set_application(app)


def load_from_files(
        filenames: list[str], *, load_obj: bool = True,
    ) -> Callable[[Any], type[UILoadedClass]]:
    """Generate a decorator to load '.ui' files in a class and do a basic setup.

    Generates a function that can be used as a decorator to classes. The decorator will
    return a new class that loads the provided '.ui' files and does a basic setup.

    Can be used as the following code sample:

    .. code-block:: python

        @load_from_files(["example.ui"])
        class MyApp(Adw.Application):
            def __init__(self, **kwargs: object) -> None:
                print("Loaded!")

            def on_activate_handler(self, app: Gtk.Application) -> None:
                self.main_window.set_application(self)
                self.main_window.present()

    Naming conventions:

    * *parent class*: The ancestor class of the decorated class.
    * *original class*: The class that will be extended by the decorator.
    * *decorated class*: The new class that will be created by the decorator. (result
      of decorating of the original class).

    The methods that the *decorated class* overloads will always call its respective
    method in the parent. So, this class will not remove any features, only add them.
    All the methods and attributes of the *original class* will be available in the
    *decorated class*.

    It is not required to provide a '__init__()' function in the *original class*. If it
    is not found, it will not be called. It is not required to provide a
    'on_activate_handler()' function in the *original class*, but it may be an error, so
    the implementation will show a warning message.

    The *decorated class* already calls the '__init__()' function from the
    *parent class*. The user does not need to call 'super().__init__()' in the
    *original class*.

    The 'activate' signal is automatically connected to the 'on_activate_handler()'
    function. The user only needs to provide this method in the *original class*.

    The 'on_activate_handler' of the *decorated class* will attempt to load the objects
    from the provided '.ui' files as objects in the instance with the
    :func:`load_objects_from_builder()` function. The generated builder will be saved
    as *self._loader_builder* and the loaded objects names will be saved in
    *self._loaded_obj_names*. If there are a 'main_window' object in the
    *decorated class*, it will consider this object a 'Gtk.Window' object and will
    sets the *decorated class* as its application (see `Gtk.Window.set_application()`).
    After this, will call the 'on_activate_handler' of the *original class*.

    Parameters
    ----------
    filenames : list[str]
        The list of '.ui' files to load.

    load_obj : bool
        Whether to load the objects from the builder.

    Returns
    -------
    Callable[[type[Class]], type[UILoadedClass]]
        The function that can be used as class decorator to load the '.ui' files.

    """
    def wrapper(cls: type[Class]) -> type[UILoadedClass]:
        """Extend the provided class with a basic setup.

        Parameters
        ----------
        cls : type[Class]
            The class that will be extended by the decorator. This is the
            *original class*.

        Returns
        -------
        type[UILoadedClass]
            The new class that will be created by the decorator. This is the
            *decorated class*.

        """
        class UILoadedClass(cls):  # type: ignore[misc, valid-type]
            """Extended class with a basic setup.

            This is the *decorated class*.
            """

            def __init__(self, **kwargs: dict[str, object]) -> None:
                """Initialize the class.

                Parameters
                ----------
                kwargs : dict[str, object]
                    The keyword arguments to pass to the parent class.

                """
                # Basic setup: Initialize the parent of the decorated class and connect
                # the usually used signals
                super(cls, cast("Class", self)).__init__(**kwargs)
                self.connect("activate", self.on_activate_handler)

                # User '__init__()' function
                if hasattr(super(), "__init__"):
                    super().__init__(**kwargs)

            def on_activate_handler(self, app: Gtk.Application) -> None:
                """Load the objects from the '.ui' files.

                Called when the application is launched.

                Parameters
                ----------
                app : Gtk.Application
                    The application object.

                """
                self._loader_builder, self._loaded_obj_names = load_builder_from_files(
                    self, filenames, load_obj=load_obj)

                if hasattr(self, "main_window"):
                    self.main_window.set_application(self)

                # User 'on_activate_handler()' function
                if hasattr(super(), "on_activate_handler"):
                    super().on_activate_handler(app)

                else:
                    # Not provide a 'on_activate_handler()' function can be an error, so
                    # shows a warning
                    logging.warning(
                        "No 'on_activate_handler()' function found, skipping.")

        return UILoadedClass

    return wrapper
