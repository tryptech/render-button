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

from . import modules, operators, preferences, props, ui

classes = {
    "RenderButton_Preferences": preferences.RenderButton_Preferences,
    "RenderButton_Settings": props.ButtonProps.RenderButton_Settings,
    "RB_OT_Render": operators.RenderOps.RB_OT_Render,
    "RB_OT_RenderAnimation": operators.RenderOps.RB_OT_RenderAnimation,
    "PROPERTIESPANEL_PT_RenderButton": ui.PropertiesPanel.PROPERTIESPANEL_PT_RenderButton,
    "VIEW3DTAB_PT_RenderButton": ui.View3DTab.VIEW3DTAB_PT_RenderButton,
}
