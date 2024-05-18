import typing
import nodeitems_utils

GenericType = typing.TypeVar("GenericType")

class SortedNodeCategory(nodeitems_utils.NodeCategory):
    def poll(self, _context):
        """

        :param _context:
        """
        ...

class CompositorNodeCategory(SortedNodeCategory, nodeitems_utils.NodeCategory):
    def poll(self, context):
        """

        :param context:
        """
        ...

class ShaderNodeCategory(SortedNodeCategory, nodeitems_utils.NodeCategory):
    def poll(self, context):
        """

        :param context:
        """
        ...

def group_input_output_item_poll(context): ...
def group_tools_draw(_self, layout, _context): ...
def node_group_items(context): ...
def register(): ...
def unregister(): ...
