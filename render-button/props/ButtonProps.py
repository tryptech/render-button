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
from bpy.props import BoolProperty
from bpy.types import PropertyGroup


class RenderButton_Settings(PropertyGroup):

    ### Render Button[ ---
    switchStillAnim_prop: BoolProperty(
        name="Animation", description="Activate Animation Rendering", default=False
    )  # type: ignore
    ### ]Render Button

    ### Panel Quick Settings[ ---
    mbbOptions: bpy.props.BoolProperty(
        name="Render Quick Settings",
        # description="Toggle Quick Settings",
        default=False,
    )  # type: ignore

    ## Sound alarm[ ---
    playAfterRender: bpy.props.BoolProperty(
        name="Play sound", description="Play Sound when render is done", default=False
    )  # type: ignore

    soundToPlay: bpy.props.StringProperty(
        name="Choose Audio File",
        description="Specify location of audio file to play after render",
        default="",
        subtype="FILE_PATH",
    )  # type: ignore

    loopSoundToPlay: bpy.props.BoolProperty(
        name="loop sound", description="Play loop Sound", default=False
    )  # type: ignore

    repeatSoundToPlay: bpy.props.IntProperty(
        name="Repeat Sound",
        description="Repeat sound after render",
        min=0,
        max=100,
        step=1,
        default=0,
    )  # type: ignore

    alarmInProgress: bpy.props.BoolProperty(
        name="Alarm In Progress", description="Alarm In Progress", default=False
    )  # type: ignore

    abortAlarm: bpy.props.BoolProperty(
        name="Abort Alarm", description="Abort Alarm", default=False
    )  # type: ignore
    ## ]Sound alarm

    ## Power off[---
    poweroffAfterRender: bpy.props.BoolProperty(
        name="Power Off", description="Power Off after render", default=False
    )  # type: ignore

    timeoutPowerOff: bpy.props.IntProperty(
        name="Timeout Delay",
        description="Delay in secondes before Power Off",
        min=15,
        max=1200,
        step=1,
        default=60,
    )  # type: ignore

    countDownAfterRender: bpy.props.IntProperty(
        name="Countdown after render", description="Countdown after render", default=0
    )  # type: ignore

    saveAtPowerOff: bpy.props.BoolProperty(
        name="Save Blender File",
        description="Save Blender file before Power Off",
        default=False,
    )  # type: ignore
    ## ]Power off

    ## Auto save render[---
    saveInBlendFolder: bpy.props.BoolProperty(
        name="Save in blend folder",
        description="Save Camera Output in blend folder",
        default=False,
    )  # type: ignore

    storeRenderInSlots: bpy.props.BoolProperty(
        name="Store in Slots",
        description="Store Cameras Output in Render Slots",
        default=False,
    )  # type: ignore
    ## ]Auto save render
    ### ]Panel Quick Settings

    ### Dimensions settings[ ---
    switchRenderRotation_prop: bpy.props.BoolProperty(
        name="Rotation", description="Toggle Landscape / Portrait", default=False
    )  # type: ignore

    Default_HRes_prop: bpy.props.IntProperty(
        name="DHres",
        description="Horizontal Default Dimension",
        default=1920,
        max=65536,
        min=4,
        step=1,
    )  # type: ignore

    Default_VRes_prop: bpy.props.IntProperty(
        name="DVres",
        description="Vertical Default Dimension",
        default=1080,
        max=65536,
        min=4,
        step=1,
    )  # type: ignore

    Default_HPixRes_prop: bpy.props.FloatProperty(
        name="DHPix", description="Horizontal Default Pixel Aspect", default=1
    )  # type: ignore

    Default_VPixRes_prop: bpy.props.FloatProperty(
        name="DVPix", description="Vertical Default Pixel Aspect", default=1
    )  # type: ignore
    ### ]Dimensions settings

    ### Only For This Job[ -----------------------------------------
    onlyForThisJob: bpy.props.BoolProperty(
        name="Set Render Format For This Job",
        description="Revert To Current Format After This Job",
        default=False,
    )  # type: ignore
    ### ]Only For This Job
