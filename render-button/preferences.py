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

import bpy
from bpy.props import BoolProperty, FloatProperty
from bpy.types import AddonPreferences


class RenderButton_Preferences(AddonPreferences):
    bl_idname = __package__

    renderButtonEnable: BoolProperty(
        name="Enable render button",
        default=True,
    )  # type: ignore

    renderButtonSize: FloatProperty(
        name="Render size",
        default=2.5,
        step=0.5,
    )  # type: ignore

    def draw(self, context):
        layout = self.layout
        layout.label(text="test")
        main_col = layout.column(align=True)
        box = main_col.box()
        col = box.column(align=True)
        row = col.row(align=True)
        row.prop(self, "renderButtonEnable")
        if self.renderButtonEnable:
            row = col.row(align=True)
            row.prop(self, "renderButtonSize")
