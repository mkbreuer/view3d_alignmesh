# LOAD MODULE #
import bpy
from bpy import*


class VIEW3D_OT_mirror_over_edge(bpy.types.Operator):
    """mirror selected mesh over active edge / normal Y axis"""                 
    bl_idname = "tpc_ot.mirror_over_edge"          
    bl_label = "Edge Mirror"                  
    bl_options = {'REGISTER', 'UNDO'}   
        
    def execute(self, context):
        
        store_pivot = bpy.context.scene.tool_settings.transform_pivot_point

        bpy.context.scene.tool_settings.transform_pivot_point = 'ACTIVE_ELEMENT'  

        bpy.ops.transform.mirror(orient_type='NORMAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
                                 orient_matrix_type='GLOBAL', constraint_axis=(False, True, False))

        bpy.ops.mesh.normals_make_consistent(inside=False)
       
        bpy.context.scene.tool_settings.transform_pivot_point = store_pivot

        return {'FINISHED'}
