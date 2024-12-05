# This file is part of Render Button.
#
# Render Button is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.
#
# Render Button is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Render Button. If not, see https://www.gnu.org/licenses/.

import os

import bpy
from bpy.props import PointerProperty
from bpy.types import Scene
from bpy.utils import register_class, unregister_class

from . import modules, operators, props, ui
from .bpy_class import classes

addon_keymaps = []


def register():

    for cls in classes.values():
        register_class(cls)

    Scene.RBTab_Settings = PointerProperty(type=classes["RenderButton_Settings"])  # type: ignore
    Scene.RBpackage = __package__

    WinMan = bpy.context.window_manager
    KeyConfig = WinMan.keyconfigs.addon
    if KeyConfig is not None:
        KeyMap = KeyConfig.keymaps.new(name="Object Mode")
        # KeyMapItem = KeyMap.keymap_items.new(
        #     SCENECAMERA_OT_Add.bl_idname, "C", "PRESS", alt=True
        # )
        # addon_keymaps.append((KeyMap, KeyMapItem))


def unregister():

    for cls in classes.values():
        unregister_class(cls)

    WinMan = bpy.context.window_manager
    KeyConfig = WinMan.keyconfigs.addon
    if KeyConfig is not None:
        for KeyMap, KeyMapItem in addon_keymaps:
            KeyMap.keymap_items.remove(KeyMapItem)


if __name__ == "__main__":
    try:
        unregister()
    except:
        pass
    register()
