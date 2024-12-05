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
from bpy.types import Operator

from ..props.ButtonProps import RenderButton_Settings


def ShowMessageBox(message="", title="Message Box", icon="INFO"):
    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


class RB_OT_Render(Operator):
    bl_idname = "renderbutton.render_scene_camera"
    bl_label = "Render Camera"
    bl_description = "Render active camera"

    _autoSaveRender = None
    _chosenCamera = None
    _currentRenderFileFormat = ""
    _rendering = None
    _stop = None
    _timer = None

    KamCurrent = None
    path = "//"
    finish = None

    renderFrom: bpy.props.StringProperty(default="")  # type: ignore

    def renderComplete(self, dummy, thrd=None):
        scene = bpy.context.scene
        RBTS = scene.RBTab_Settings
        render = scene.render
        self.finish = True

        if scene.frame_current == 0:
            marker_list = scene.timeline_markers
            for m in marker_list:
                if m.camera == scene.camera:
                    scene.timeline_markers.remove(m)

    def renderCancel(self, dummy, thrd=None):
        scene = bpy.context.scene
        render = scene.render
        self._stop = True
        if scene.frame_current == 0:
            marker_list = scene.timeline_markers
            for m in marker_list:
                if m.camera == scene.camera:
                    scene.timeline_markers.remove(m)

    def execute(self, context):
        scene = context.scene
        RBTS = scene.RBTab_Settings
        chosen_camera = context.active_object
        render = scene.render
        KamCurrent = None
        self._chosenCamera = context.active_object

        if RBTS.saveInBlendFolder:
            render.filepath = "//"

        ### Check render File Format[---
        imageFormat = [
            "TIFF",
            "BMP",
            "IRIS",
            "JPEG2000",
            "TARGA",
            "TARGA_RAW",
            "CINEON",
            "DPX",
            "OPEN_EXR",
            "OPEN_EXR_MULTILAYER",
            "HDR",
            "JPEG",
            "PNG",
        ]
        if (
            render.image_settings.file_format not in imageFormat
            and render.filepath != ""
        ):
            self.report(
                {"WARNING"},
                "Cannot write a single file with an animation format selected",
            )
            bpy.ops.render.renderformat("INVOKE_DEFAULT")
            return {"CANCELLED"}
        # ]Check render File Format

        ### Check Sound File For Alarm[---
        if RBTS.playAfterRender:
            a, soundType = os.path.splitext(RBTS.soundToPlay)
            soundExt = bpy.path.extensions_audio

            if str.lower(soundType) not in soundExt or not os.path.exists(
                bpy.path.abspath(RBTS.soundToPlay)
            ):
                RBTS.soundToPlay = ""
                ShowMessageBox(
                    "Choose a sound file for alarm before !",
                    "Wrong Sound File Type OR Not Exist",
                    "ERROR",
                )
                self.report({"WARNING"}, "Wrong Sound File Type OR Not Exist")
                return {"CANCELLED"}
        # ]Check Sound File For Alarm

        ### Autosave & Render file path[---
        if len(bpy.context.scene.render.filepath) == 0:
            if not RBTS.saveInBlendFolder:
                self._autoSaveRender = False
            else:
                self._autoSaveRender = True
                self.path = "//"
        else:
            self._autoSaveRender = True
            if not RBTS.saveInBlendFolder:
                self.path = bpy.context.scene.render.filepath
            else:
                self.path = "//"
        # ]Autosave

        bpy.app.handlers.render_complete.append(self.renderComplete)
        bpy.app.handlers.render_cancel.append(self.renderCancel)
        self._timer = context.window_manager.event_timer_add(0.5, window=context.window)
        context.window_manager.modal_handler_add(self)

        self._rendering = True

        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        scene = context.scene
        render = scene.render
        RBTS = scene.RBTab_Settings

        ### EXIT after render is done or canceled[---
        if self.finish or self._stop:
            self._rendering = False

            bpy.app.handlers.render_complete.remove(self.renderComplete)
            bpy.app.handlers.render_cancel.remove(self.renderCancel)
            context.window_manager.event_timer_remove(self._timer)

            RBTS.frameRenderType = ""

            if RBTS.onlyForThisJob:
                render.image_settings.file_format = RBTS.currentFormatRenderType
                RBTS.onlyForThisJob = False

            if self._autoSaveRender:
                scene.render.filepath = self.path
            else:
                scene.render.filepath = ""

            if self._stop:
                return {"FINISHED"}
            elif RBTS.playAfterRender or RBTS.poweroffAfterRender:
                bpy.ops.renderevents.end_events("INVOKE_DEFAULT")

            return {"FINISHED"}
        # ]EXIT

        if self._rendering:
            self._rendering = False

            render = scene.render
            KamCurrent = None

            bpy.context.view_layer.objects.active = self._chosenCamera

            marker_list = context.scene.timeline_markers
            cameras = sorted(
                [o for o in scene.objects if o.type == "CAMERA"], key=lambda o: o.name
            )

            ### Checklist for avoid some errors[---
            if context.active_object is None:
                if len(cameras) == 0:
                    ShowMessageBox(
                        "No camera found in this scene !", "Render Error", "ERROR"
                    )
                    self.report({"ERROR"}, "No camera found in this scene !")
                    return {"FINISHED"}
                elif len(cameras) > 0 and scene.camera is None:
                    bpy.ops.object.select_all(action="DESELECT")
                    self._chosenCamera = cameras[0]
                    self._chosenCamera.select_set(state=True)
                    scene.camera = self._chosenCamera
                elif len(cameras) == 1:
                    bpy.ops.object.select_all(action="DESELECT")
                    self._chosenCamera = cameras[0]
                    self._chosenCamera.select_set(state=True)
                    scene.camera = self._chosenCamera
                elif len(cameras) > 1:
                    bpy.ops.object.select_all(action="DESELECT")
                    self._chosenCamera = scene.camera
                    self._chosenCamera.select_set(state=True)
                    bpy.context.view_layer.objects.active = self._chosenCamera
            else:
                if len(cameras) == 0:
                    ShowMessageBox("No Camera in this scene !", "Render", "ERROR")
                    return {"FINISHED"}
                elif len(cameras) > 0 and scene.camera is None:
                    bpy.ops.object.select_all(action="DESELECT")
                    self._chosenCamera = cameras[0]
                    self._chosenCamera.select_set(state=True)
                    scene.camera = self._chosenCamera
                elif len(cameras) == 1:
                    if context.active_object.type != "CAMERA":
                        # print("no camera active")
                        bpy.ops.object.select_all(action="DESELECT")
                        self._chosenCamera = cameras[0]
                        self._chosenCamera.select_set(state=True)
                        scene.camera = self._chosenCamera
                elif len(cameras) > 1:
                    if context.active_object.type != "CAMERA":
                        bpy.ops.object.select_all(action="DESELECT")
                        self._chosenCamera = scene.camera
                        self._chosenCamera.select_set(state=True)
                        bpy.context.view_layer.objects.active = self._chosenCamera
            # ]Checklist

            # if bpy.context.scene.render.display_mode not in ('AREA', 'NONE', 'WINDOW'):  self.renderFrom = 'PROPERTIES'
            if context.preferences.view.render_display_type not in (
                "AREA",
                "NONE",
                "WINDOW",
            ):
                self.renderFrom = "PROPERTIES"

            if self.renderFrom == "TAB":
                scene.camera = context.space_data.camera
                self._chosenCamera = context.space_data.camera
            elif self.renderFrom in ("PROPERTIES", "CAMANAGER"):
                scene.camera = self._chosenCamera

            x = render.resolution_x
            y = render.resolution_y

            rs = scene.RBTab_Settings

            render.resolution_x = RBTS.Default_HRes_prop
            render.resolution_y = RBTS.Default_VRes_prop
            render.pixel_aspect_x = RBTS.Default_HPixRes_prop
            render.pixel_aspect_y = RBTS.Default_VPixRes_prop

            if len(marker_list) > 0:
                bpy.ops.object.select_all(action="DESELECT")
                self._chosenCamera.select_set(state=True)
                context.view_layer.objects.active = scene.camera

                if self.renderFrom == "TAB":

                    context.space_data.camera = bpy.data.objects[scene.camera.name]
                    for area in context.screen.areas:
                        if area.type == "VIEW_3D":
                            context.area.spaces[0].region_3d.view_perspective = "CAMERA"
                            break

                for marker in marker_list:
                    if self._chosenCamera == marker.camera:
                        scene.camera = marker.camera
                        scene.frame_current = marker.frame

                        scene.render.filepath = self.path + scene.camera.name
                        bpy.ops.render.render(
                            "INVOKE_DEFAULT", write_still=self._autoSaveRender
                        )

                        return {"PASS_THROUGH"}

                marker = None

                scene.frame_current = 0

                current_frame = scene.frame_current

                for m in reversed(
                    sorted(
                        filter(
                            lambda m: m.frame <= current_frame, scene.timeline_markers
                        ),
                        key=lambda m: m.frame,
                    )
                ):
                    marker = m
                    break

                marker_name = scene.camera.name

                if marker and (marker.frame == current_frame):
                    marker.name = marker_name
                else:
                    marker = scene.timeline_markers.new(marker_name)

                marker.frame = scene.frame_current
                marker.camera = scene.camera
                marker.select = True

                for other_marker in [m for m in scene.timeline_markers if m != marker]:
                    other_marker.select = False

                scene.render.filepath = self.path + scene.camera.name
                bpy.ops.render.render(
                    "INVOKE_DEFAULT", write_still=self._autoSaveRender
                )

            elif len(marker_list) == 0:
                bpy.ops.object.select_all(action="DESELECT")
                self._chosenCamera.select_set(state=True)
                context.view_layer.objects.active = scene.camera

                if self.renderFrom in ("TAB", "CAMANAGER"):
                    context.space_data.camera = bpy.data.objects[scene.camera.name]
                    for area in context.screen.areas:
                        if area.type == "VIEW_3D":
                            context.area.spaces[0].region_3d.view_perspective = "CAMERA"
                            break

                scene.render.filepath = self.path + scene.camera.name
                bpy.ops.render.render(
                    "INVOKE_DEFAULT", write_still=self._autoSaveRender
                )

        return {"PASS_THROUGH"}


class RB_OT_RenderAnimation(Operator):
    bl_idname = "renderbutton.render_scene_animation"
    bl_label = "Render Animation"
    bl_description = "Render active camera across the playback/rendering range"

    _autoSaveRender = None
    _cameras = None
    _finish = None
    _stop = None
    _timer = None

    path = "//"

    renderFrom: bpy.props.StringProperty(default="")  # type: ignore

    def renderComplete(self, dummy, thrd=None):
        self._finish = True

    def renderCancel(self, dummy, thrd=None):
        self._stop = True

    def execute(self, context):

        scene = bpy.context.scene
        RBTS = scene.RBTab_Settings

        self._cameras = sorted(
            [o for o in scene.objects if o.type == "CAMERA"], key=lambda o: o.name
        )

        ### Check Sound File For Alarm[---
        if RBTS.playAfterRender:
            a, soundType = os.path.splitext(RBTS.soundToPlay)
            soundExt = bpy.path.extensions_audio

            if (
                str.lower(soundType) not in soundExt
                or os.path.exists(bpy.path.abspath(RBTS.soundToPlay)) == False
            ):
                RBTS.soundToPlay = ""
                ShowMessageBox(
                    "Choose a sound file for alarm before !",
                    "Wrong Sound File Type OR Not Exist",
                    "ERROR",
                )
                self.report({"WARNING"}, "Wrong Sound File Type OR Not Exist")
                return {"CANCELLED"}
        ### ]Check Sound File For Alarm

        ## Autosave & Render file path[---
        if len(bpy.context.scene.render.filepath) == 0:
            if not RBTS.saveInBlendFolder:
                self._autoSaveRender = False
            else:
                self._autoSaveRender = True
                self.path = "//"
        else:
            self._autoSaveRender = True
            if RBTS.saveInBlendFolder:
                self.path = bpy.context.scene.render.filepath
            else:
                self.path = "//"
        ### ]Autosave

        ## Application handlers[---
        bpy.app.handlers.render_complete.append(self.renderComplete)
        bpy.app.handlers.render_cancel.append(self.renderCancel)
        self._timer = context.window_manager.event_timer_add(
            0.5, window=context.window
        )  # Timer event
        context.window_manager.modal_handler_add(self)
        ## ]Application handlers

        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        scene = context.scene
        RBTS = scene.RBTab_Settings

        ### EXIT after render is done or canceled[---
        if self._finish or self._stop:

            if self._autoSaveRender:
                scene.render.filepath = self.path
            else:
                scene.render.filepath = ""
            # Remove handlers
            bpy.app.handlers.render_complete.remove(self.renderComplete)
            bpy.app.handlers.render_cancel.remove(self.renderCancel)
            context.window_manager.event_timer_remove(self._timer)
            # Alarm
            if RBTS.playAfterRender or RBTS.poweroffAfterRender:
                bpy.ops.renderevents.end_events("INVOKE_DEFAULT")

            return {"FINISHED"}
        ### ]EXIT

        scene.render.filepath = self.path

        if len(self._cameras) == 0:
            ShowMessageBox("No camera found in this scene !", "Render Error", "ERROR")
            self.report({"ERROR"}, "No camera found in this scene !")
            return {"FINISHED"}
        else:
            bpy.ops.render.render("INVOKE_DEFAULT", animation=True)

        return {"PASS_THROUGH"}
