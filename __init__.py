# ##### BEGIN GPL LICENSE BLOCK #####
#
# (C) 2021 MKB
#
#  This program is free software; you can redistribute it and / or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110 - 1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
#

bl_info = {
"name": "Align Mesh", 
"author": "marvin.k.breuer (MKB)",
"version": (0, 0, 3),
"blender": (2, 82, 0),
"location": "View3D > Editmode > Default Tab: Align > Panel: Align Mesh",
"description": "align functions for geometries in editmode",
"warning": "",
"wiki_url": "",
"tracker_url": "",
"category": "Mesh"}


# LOAD MODULES #
import bpy
import bpy.utils.previews
from bpy.props import *

# updater ops import, all setup in this file
from . import addon_updater_ops

# LOAD CUSTOM ICONS #
from . icons.icons  import load_icons
from . icons.icons  import clear_icons

# LOAD OPERATORS #                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
from .operators.ot_axis       import *                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
from .operators.ot_distribute import *                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
from .operators.ot_edit       import *                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
from .operators.ot_flatten    import *                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
from .operators.ot_help       import *                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
from .operators.ot_mirror     import *                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
from .operators.ot_smooth     import *                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               

# LOAD UI # 
from .ui_layout   import * 


# PANEL TO CONTAINING THE TOOLS #
class VIEW3D_PT_align_mesh_panel_ui(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Align'
    bl_label = "Align Mesh"
    bl_context = "mesh_edit"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout.column(align=True)

        draw_ui_panel_align_mesh(context, layout)


# UPDATE TAB CATEGORY FOR PANEL IN THE TOOLSHELF #
panels = (
        VIEW3D_PT_align_mesh_panel_ui,
        )

def update_panel(self, context):
    message = "Updating Panel locations has failed"
    try:
        for panel in panels:
            if "bl_rna" in panel.__dict__:
                bpy.utils.unregister_class(panel)

        for panel in panels:
            panel.bl_category = context.preferences.addons[__name__].preferences.toggle_category
            bpy.utils.register_class(panel)

    except Exception as e:
        print("\n[{}]\n{}\n\nError:\n{}".format(__name__, message, e))
        pass



# ADDON PREFERENCES #
@addon_updater_ops.make_annotations
class Addon_Preferences_align_mesh(bpy.types.AddonPreferences):
    bl_idname = __name__
       
    toggle_category : StringProperty(name="", description="panel location in the toolshelf", default="Align", update=update_panel)

    threshold : bpy.props.FloatProperty(name="Threshold",  description="angle value to select linked face", default=0.0174533, min=0.0174533, max=3.14159, subtype='ANGLE')

    mesh_select_mode : bpy.props.EnumProperty(
      items = [("vertices", "Vertex", "enable vertex selection", 1),
               ("edges",    "Edge",   "enable edge selection"  , 2), 
               ("faces",    "Face",   "enable face selection"  , 3)], 
               name = "Mesh Select Mode",
               default = "vertices",
               description="type of mesh select mode when finish")

    show_history_tools : bpy.props.BoolProperty(name = "Show History Tools", description = "toggle tools visibilty in the panel", default = True)

    orient : bpy.props.EnumProperty(
        items=[("GLOBAL"    ,"Global"   ,"Global"),
               ("LOCAL"     ,"Local"    ,"Local"),
               ("NORMAL"    ,"Normal"   ,"Normal"),
               ("GIMBAL"    ,"Gimbal"   ,"Gimbal"),
               ("VIEW"      ,"View"     ,"View"),
               ("CURSOR"    ,"Cursor"   ,"Cursor")],
               name = "Orientation XYZ",
               default = "GLOBAL",    
               description = "change orientation for xyz axis")

    #----------------------------

    # ADDON UPDATER #

    auto_check_update : BoolProperty(name = "Auto-check for Update", description = "If enabled, auto-check for updates using an interval", default = False)
    updater_intrval_months : IntProperty(name='Months', description = "Number of months between checking for updates", default=0, min=0)
    updater_intrval_days : IntProperty(name='Days', description = "Number of days between checking for updates", default=7, min=0)
    updater_intrval_hours : IntProperty(name='Hours', description = "Number of hours between checking for updates", default=0, min=0, max=23)
    updater_intrval_minutes : IntProperty(name='Minutes', description = "Number of minutes between checking for updates", default=0, min=0, max=59)

    #----------------------------

    def draw(self, context):
        addon_updater_ops.update_settings_ui(self, context)

        layout = self.layout.column(align=True)

        box = layout.box().column(align=True)
        box.separator()   

        row = box.row(align=True)  
        row.label(text="Tab Category:")                                           
        row.prop(self, "toggle_category", text="")

        box.separator() 

        row = box.row(align=True)
        row.label(text='Mirror Orientation:')
        row.prop(self, "orient", text ='')   

        box.separator() 

        row = box.row(align=True)
        row.label(text='When finished Modal select:')
        row.prop(self, "mesh_select_mode", text ='')           
        
        box.separator()     
 
        row = box.row(align=True)
        row.label(text="Threshold:") 
        row.prop(self, "threshold", text="Select linked face")           

        box.separator() 

        row = box.row(align=True)
        row.label(text='Undo-History-Redo (panel bottom):')       
        row.prop(self, "show_history_tools", text ='')           
     
        box.separator() 


def func_menu_vertices(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.separator()
        layout.operator('tpc_ot.shrinkwrap_smooth', text="Relax Quads")
        layout.separator()
        layout.operator('tpc_ot.vertex_align', text="Straight")
        layout.operator('tpc_ot.vertex_distribute', text="Evenly")
        layout.operator('tpc_ot.vertex_inline', text="Evenly Straight")



# PROPERTY GROUP #  
class Global_Property_Group(bpy.types.PropertyGroup):
    # use an annotation

    type_align = [("align"    ,"Align"    ,"select bounds by letter sequence" ,1),      
                  ("flatten"  ,"Flatten"  ,"select bounds by geometry"        ,2)]  

    align_typ : bpy.props.EnumProperty(name = "Align Type", default = "align", description = "switch align type", items = type_align)

    use_axis_align : BoolProperty(name="Align to Axis", description="align selected mesh to x,y,z world axis", default = False)


# REGISTERY #
classes = (
    VIEW3D_PT_align_mesh_panel_ui,
    VIEW3D_OT_align_mesh,
    VIEW3D_OT_align_mesh_to_axis,
    VIEW3D_OT_modal_snapflat,
    VIEW3D_OT_mesh_align_help,
    VIEW3D_OT_distribute_vertices,
    VIEW3D_OT_align_vertices,
    VIEW3D_OT_inline_vertices,
    VIEW3D_OT_shrinkwrap_smooth,
    VIEW3D_OT_mirror_over_edge,
    Addon_Preferences_align_mesh,
    Global_Property_Group,
)

def register():
    # addon updater code and configurations
    addon_updater_ops.register(bl_info)

    for cls in classes:
        addon_updater_ops.make_annotations(cls)
        bpy.utils.register_class(cls)
   
    bpy.types.WindowManager.alignmesh_global_props = bpy.props.PointerProperty(type=Global_Property_Group)   

    bpy.types.VIEW3D_MT_edit_mesh_vertices.append(func_menu_vertices)
  
    update_panel(None, bpy.context)


def unregister():
    # addon updater code and configurations
    addon_updater_ops.unregister()

    try:
        del bpy.types.WindowManager.alignmesh_global_props
    except Exception as e:
        print('unregister fail:\n', e)
        pass

    bpy.types.VIEW3D_MT_edit_mesh_vertices.remove(func_menu_vertices)

    try:
        for cls in reversed(classes):
            bpy.utils.unregister_class(cls)
    except RuntimeError:
        pass


if __name__ == "__main__":
    register()
