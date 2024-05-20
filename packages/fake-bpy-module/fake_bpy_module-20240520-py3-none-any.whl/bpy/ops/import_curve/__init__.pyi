import typing
import collections.abc
import bpy.types

GenericType1 = typing.TypeVar("GenericType1")
GenericType2 = typing.TypeVar("GenericType2")

def svg(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    filepath: str | typing.Any = "",
    filter_glob: str | typing.Any = "*.svg",
):
    """Load a SVG file

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param filepath: File Path, Filepath used for importing the file
    :type filepath: str | typing.Any
    :param filter_glob: filter_glob
    :type filter_glob: str | typing.Any
    """

    ...
