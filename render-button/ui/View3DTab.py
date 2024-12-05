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
from bpy.types import Panel

from ..props.ButtonProps import RenderButton_Settings


class VIEW3DTAB_PT_RenderButton(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"
    bl_label = "Render"
    bl_idname = "VIEW3DTAB_PT_RenderButton"

    @classmethod
    def poll(cls, context):
        return not context.scene.RBTab_Settings.alarmInProgress

    def draw_header_preset(self, context):
        scene = context.scene
        RBTS = context.scene.RBTab_Settings

        layout = self.layout
        layout.emboss = "NONE"
        row = layout.row(align=True)

        if not RBTS.mbbOptions:

            row.operator("render.opengl", text="", icon="RENDER_STILL")
            row.operator(
                "render.opengl", text="", icon="RENDER_ANIMATION"
            ).animation = True
            row.operator(
                "screen.screen_full_area", text="", icon="FULLSCREEN_ENTER"
            ).use_hide_panels = False
            row.separator()
            row.separator()
            row.separator()
            row.separator()

    def draw_header(self, context):
        scene = context.scene
        RBTS = scene.RBTab_Settings

        layout = self.layout
        layout.emboss = "NONE"
        row = layout.row(align=True)

        if RBTS.mbbOptions:
            _emboss = True
            row.alert = True
        else:
            _emboss = False
            row.alert = False

        row.prop(RBTS, "mbbOptions", icon="SETTINGS", icon_only=True)  #

    def draw(self, context):
        scene = context.scene
        render = scene.render
        RBTS = scene.RBTab_Settings
        image_settings = render.image_settings
        prefs = context.preferences
        addon_prefs = prefs.addons[scene.RBpackage].preferences

        layout = self.layout

        if not RBTS.mbbOptions:
            if addon_prefs.renderButtonEnable:
                row = layout.row(align=True)
                row.scale_y = addon_prefs.renderButtonSize
                # row.alert = True

                if RBTS.switchStillAnim_prop:
                    row.operator(
                        "renderbutton.render_scene_animation", text="RENDER ANIMATION"
                    )
                else:
                    row.operator(
                        "renderbutton.render_scene_camera", text="RENDER FRAME"
                    ).renderFrom = "TAB"

                row.prop(
                    scene.RBTab_Settings,
                    "switchStillAnim_prop",
                    text="",
                    icon="RENDER_ANIMATION",
                )

                # Frame Range
                if RBTS.switchStillAnim_prop:
                    row = layout.row(align=True)

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

            if render.has_multiple_engines:
                row.prop(render, "engine", text="")

            prefs = context.preferences
            view = prefs.view
            row.prop(view, "render_display_type", text="")

            row.prop(
                render,
                "use_lock_interface",
                text="",
                emboss=False,
                icon="DECORATE_UNLOCKED",
            )

        ###RENDER SETTINGS[_____________________________________________________________________________
        else:
            ## if file not saved[---
            if not bpy.data.is_saved:
                layout.use_property_split = False
                row = layout.row(align=True)
                row.alignment = "CENTER"
                row.alert = True
                row.label(text=" Save Blend File First  --->", icon="INFO")
                row.operator("wm.save_mainfile", text="", icon="FILE_TICK")
                row.alert = False
            ## ]if file not saved

            else:
                row = layout.row(align=True)
                box = layout.box()
                row = box.row(align=True)
                row.alert = True
                row.alignment = "CENTER"

                row.label(text="Output")

                row = box.row(align=True)

                row.prop(image_settings, "file_format", icon="IMAGE", text="")
                row = box.row(align=True)
                if not RBTS.saveInBlendFolder:
                    row.prop(render, "filepath", text="")

                row = box.row(align=True)
                row.prop(
                    RBTS, "saveInBlendFolder", text="In blend folder", icon="BLENDER"
                )
                row.prop(
                    RBTS,
                    "storeRenderInSlots",
                    text="In render slots",
                    icon="RENDER_RESULT",
                )
                ## ]Output settings

                ## Alarm settings[---
                row = layout.row(align=True)
                box = layout.box()
                row = box.row(align=True)
                row.alert = True
                row.alignment = "CENTER"

                row.label(text="Alarm & Power Off")

                row = box.row(align=True)

                row.prop(RBTS, "playAfterRender", text="Play Sound", icon="FILE_SOUND")

                if RBTS.playAfterRender:
                    if (
                        not RBTS.loopSoundToPlay or RBTS.poweroffAfterRender
                    ) and RBTS.soundToPlay != "":
                        row.prop(RBTS, "repeatSoundToPlay", text="Repeat")

                    if not RBTS.poweroffAfterRender and RBTS.soundToPlay != "":
                        row.prop(RBTS, "loopSoundToPlay", text="", icon="RECOVER_LAST")

                    row = box.row(align=True)
                    if RBTS.soundToPlay == "":
                        row.alert = True
                        row.prop(RBTS, "soundToPlay", text="")
                        row.alert = False
                    else:
                        row.prop(RBTS, "soundToPlay", text="")

                    if RBTS.soundToPlay != "":
                        row.operator(
                            "renderevents.end_events", text="", icon="PLAY_SOUND"
                        ).testSoundToPlay = True

                row = box.row(align=True)
                row.prop(RBTS, "poweroffAfterRender", icon="QUIT")

                if RBTS.poweroffAfterRender:
                    row.prop(RBTS, "timeoutPowerOff", text="Timeout")
            ## ]Alarm settings

    ### ]RENDER SETTINGS
