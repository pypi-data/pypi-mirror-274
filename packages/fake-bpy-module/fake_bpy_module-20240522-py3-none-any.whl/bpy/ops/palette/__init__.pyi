import typing
import collections.abc
import bpy.types

GenericType1 = typing.TypeVar("GenericType1")
GenericType2 = typing.TypeVar("GenericType2")

def color_add(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
):
    """Add new color to active palette

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    """

    ...

def color_delete(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
):
    """Remove active color from palette

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    """

    ...

def color_move(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    type: str | None = "UP",
):
    """Move the active Color up/down in the list

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param type: Type
    :type type: str | None
    """

    ...

def extract_from_image(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    threshold: typing.Any | None = 1,
):
    """Extract all colors used in Image and create a Palette

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param threshold: Threshold
    :type threshold: typing.Any | None
    """

    ...

def join(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    palette: str | typing.Any = "",
):
    """Join Palette Swatches

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param palette: Palette, Name of the Palette
    :type palette: str | typing.Any
    """

    ...

def new(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
):
    """Add new palette

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    """

    ...

def sort(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    type: str | None = "HSV",
):
    """Sort Palette Colors

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param type: Type
    :type type: str | None
    """

    ...
