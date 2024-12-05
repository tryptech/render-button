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
from bpy import context
from bpy.types import Panel, UILayout

from ..props.ButtonProps import RenderButton_Settings


class PROPERTIESPANEL_PT_RenderButton(Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"
    bl_label = "Render"
    bl_idname = "PROPERTIESPANEL_PT_RenderButton"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return not context.scene.RBTab_Settings.alarmInProgress

    def draw(self, context):
        scene = context.scene
        render = scene.render
        RBTS = context.scene.RBTab_Settings
        prefs = context.preferences
        addon_prefs = prefs.addons[scene.RBpackage].preferences

        layout = self.layout
        split = layout.split()

        layout.use_property_split = True
        layout.use_property_decorate = False

        if addon_prefs.renderButtonEnable:
            row = layout.row(align=True)
            row.scale_y = addon_prefs.renderButtonSize

            if (context.active_object is not None) and (
                context.active_object.mode != "OBJECT"
            ):
                row.enabled = False

            if RBTS.switchStillAnim_prop:
                row.operator(
                    "renderbutton.render_scene_animation", text="RENDER ANIMATION"
                )

            else:
                row.operator(
                    "renderbutton.render_scene_camera", text="RENDER FRAME"
                ).renderFrom = "PROPERTIES"

            row.prop(RBTS, "switchStillAnim_prop", text="", icon="RENDER_ANIMATION")

            if RBTS.switchStillAnim_prop:
                row = layout.row(align=True)

                if (context.active_object is not None) and (
                    context.active_object.mode != "OBJECT"
                ):
                    row.enabled = False

                if scene.show_subframe:
                    row.prop(scene, "frame_float", text="")
                else:
                    row.prop(scene, "frame_current", text="")

                row.separator()

                row.prop(scene, "use_preview_range", text="", toggle=True)

                sub = row.row(align=True)
                sub.scale_x = 0.95

                if not scene.use_preview_range:
                    sub.prop(scene, "frame_start", text="")
                    sub.prop(scene, "frame_end", text="")
                else:
                    sub.prop(scene, "frame_preview_start", text="")
                    sub.prop(scene, "frame_preview_end", text="")

            layout.separator()
        row = layout.row()

        if (context.active_object is not None) and (
            context.active_object.mode == "EDIT"
        ):
            row.enabled = False

        row.prop(context.preferences.view, "render_display_type")

        row.prop(
            render,
            "use_lock_interface",
            text="",
            emboss=False,
            icon="DECORATE_UNLOCKED",
        )

        layout.separator()
