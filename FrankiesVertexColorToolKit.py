import bpy
import bmesh
import random
from mathutils import Vector, Color
#some bits taken from https://blender.stackexchange.com/questions/30841/how-to-view-vertex-colors

bl_info = {
    "name": "Frankies Vertex Colour Toolkit",
    "author": "Frankie",
    "version": (0,1),
    "blender": (2, 7, 9),
    "location": "View3D > Tool Panel",
    "description": "Lets you set vertex colours on objects or inside mesh",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "3d View"}

def interpolate(vector_a, vector_b, t):
    lerp = ((1 - t) * vector_a + t * vector_b)
    return (lerp)

def calculateColourValue(color_original, color_new, gradient_start, gradient_position):
    if (bpy.context.scene.fvctk_mode=="0"):
        return(color_new)

    if (bpy.context.scene.fvctk_mode=="1"):
        return((color_original[0] + color_new[0],color_original[1] + color_new[1],color_original[2] + color_new[2]))

    if (bpy.context.scene.fvctk_mode=="2"):
        return((color_original[0] - color_new[0],color_original[1] - color_new[1],color_original[2] - color_new[2]))

    if (bpy.context.scene.fvctk_mode=="3"):
        return((color_original[0] * color_new[0],color_original[1] * color_new[1],color_original[2] * color_new[2]))

    if (bpy.context.scene.fvctk_mode=="4"): #ramdomiseú
        if (bpy.context.scene.fvctk_randomiseScope=="0"):
            if (bpy.context.scene.fvctk_randomiseMode=="0"):
                return(random.random(), random.random(), random.random())
            if (bpy.context.scene.fvctk_randomiseMode=="1"):
                return(random.random()*color_new[0], random.random()*color_new[1], random.random()*color_new[2])
        if (bpy.context.scene.fvctk_randomiseScope=="1"):
            if (bpy.context.scene.fvctk_randomiseMode=="0"):
                return(bpy.context.scene.fvctk_randomColor)
            if (bpy.context.scene.fvctk_randomiseMode=="1"):
                return(bpy.context.scene.fvctk_randomColor[0]*color_new[0], bpy.context.scene.fvctk_randomColor[1]*color_new[1], bpy.context.scene.fvctk_randomColor[2]*color_new[2])

    if (bpy.context.scene.fvctk_mode=="5"): #gradient
        return(interpolate(gradient_start, color_new, gradient_position))
    return(1.0, 0.0, 1.0)

def findHighestVert():
    axis = int(bpy.context.scene.fvctk_gradient)
    if (bpy.context.scene.fvctk_gradientTop=="0"):
        highestVert = -999999
        for v in bpy.context.active_object.data.vertices:
            if (v.co[axis] > highestVert):
                highestVert = v.co[axis]
        return(highestVert)

    if (bpy.context.scene.fvctk_gradientTop=="1"):
        return(bpy.context.scene.cursor_location[axis])

    if (bpy.context.scene.fvctk_gradientTop=="2"):
        for so in bpy.context.scene.objects:
            if ("VCT" in so.name):
                return(o.location[axis])
        for o in bpy.data.objects:
            if ("VCT" in o.name):
                return(o.location[axis])
    return(0)

def findLowestVert():
    axis = int(bpy.context.scene.fvctk_gradient)
    if (bpy.context.scene.fvctk_gradientBottom=="0"):
        lowestVert = 999999
        for v in bpy.context.active_object.data.vertices:
            if (v.co[axis] < lowestVert):
                lowestVert = v.co[axis]
        return(lowestVert)

    if (bpy.context.scene.fvctk_gradientBottom=="1"):
        return(0)

    if (bpy.context.scene.fvctk_gradientBottom=="2"):
        return(bpy.context.scene.cursor_location[axis])

    if (bpy.context.scene.fvctk_gradientBottom=="3"):
        for so in bpy.context.scene.objects:
            if ("VCB" in so.name):
                return(o.location[axis])
        for o in bpy.data.objects:
            if ("VCB" in o.name):
                return(o.location[axis])
    return(0)

def modifyVertexColor(color):
    me = bpy.context.active_object.data
    bm = bmesh.from_edit_mesh(me)
    gradientStart = findLowestVert()
    gradientEnd = findHighestVert()
    if (bpy.context.scene.fvctk_world):
        gradientStart += gradientStart + bpy.context.active_object.location[int(bpy.context.scene.fvctk_gradient)]
        gradientEnd += gradientEnd + bpy.context.active_object.location[int(bpy.context.scene.fvctk_gradient)]
    gradient_position = 0

    if (bpy.context.scene.fvctk_selection):
        selected = [vert.index for vert in bm.verts if vert.select]
    else:
        selected = [vert.index for vert in bm.verts]
    bpy.ops.object.mode_set(mode='EDIT', toggle=True)
    for face in me.polygons:
        for vert_idx, loop_idx in zip(face.vertices, face.loop_indices):
            if vert_idx in selected:
                #find colour of existing vert
                vc = me.vertex_colors[me.vertex_colors.active_index].data[loop_idx].color
                #find extra data for gradient if in gradient mode
                if (bpy.context.scene.fvctk_mode=="5"):
                    vh = bpy.context.active_object.data.vertices[vert_idx].co[int(bpy.context.scene.fvctk_gradient)]
                    if (bpy.context.scene.fvctk_world):
                        vh += bpy.context.active_object.location[int(bpy.context.scene.fvctk_gradient)]
                    gradient_position = ((gradientStart * -1) + vh ) / ((gradientStart * -1) + gradientEnd)
                #work out what colour the vert will be
                c = calculateColourValue(vc, color, bpy.context.scene.fvctk_pickerGradientStart, gradient_position)
                #and then only apply to channels that are marked as true
                if (bpy.context.scene.fvctk_rBool == True):
                    me.vertex_colors[me.vertex_colors.active_index].data[loop_idx].color[0] = c[0]
                if (bpy.context.scene.fvctk_gBool == True):
                    me.vertex_colors[me.vertex_colors.active_index].data[loop_idx].color[1] = c[1]
                if (bpy.context.scene.fvctk_bBool == True):
                    me.vertex_colors[me.vertex_colors.active_index].data[loop_idx].color[2] = c[2]
    bpy.ops.object.mode_set(mode='EDIT', toggle=True)
    return()

def button(mode):
    activeObject = bpy.context.scene.objects.active
    for ob in bpy.context.selected_objects:
        if (ob.type=="MESH"):
            if ob.data .vertex_colors:
                vcol_layer = ob.data .vertex_colors.active
            else:
                vcol_layer = ob.data .vertex_colors.new()
        
            current_mode = bpy.context.object.mode
            bpy.context.scene.objects.active = ob
            bpy.context.scene.fvctk_randomColor = random.random(), random.random(), random.random()

            if (mode == 0): #from colour picker
                bpy.context.object.update_from_editmode() #maybe dont need this
                bpy.ops.object.mode_set(mode='EDIT')
                modifyVertexColor(bpy.context.scene.fvctk_picker)

            if (mode == 1): #from RGB floats
                bpy.context.object.update_from_editmode() #maybe dont need this
                current_mode = bpy.context.object.mode
                bpy.ops.object.mode_set(mode='EDIT')
                #can use values either 0-255 or normalised values from 0-1
                newR = bpy.context.scene.fvctk_r
                if (newR > 1):
                    newR /= 255
                newG = bpy.context.scene.fvctk_g
                if (newG > 1):
                    newG /= 255
                newB = bpy.context.scene.fvctk_b
                if (newB > 1):
                    newB /= 255
                bpy.ops.object.mode_set(mode='EDIT')
                modifyVertexColor((Color((newR, newG, newB))))

            bpy.ops.object.mode_set(mode=current_mode)
    bpy.context.scene.objects.active = activeObject

class FVCTK(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Frankies Vertex Color Toolkit"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "F VC TK"

    @classmethod
    def poll(cls, context):
        return context.mode in {'OBJECT', 'EDIT_MESH'}

    bpy.types.Scene.fvctk_selection = bpy.props.BoolProperty(name="Selected verts only", default=False)
    bpy.types.Scene.fvctk_world = bpy.props.BoolProperty(name="World space", default=True, description="Operate on verts in world space or local space")
    bpy.types.Scene.fvctk_r = bpy.props.FloatProperty(name="R")
    bpy.types.Scene.fvctk_rBool = bpy.props.BoolProperty(name="R", default=True)
    bpy.types.Scene.fvctk_g = bpy.props.FloatProperty(name="G")
    bpy.types.Scene.fvctk_gBool = bpy.props.BoolProperty(name="G", default=True)
    bpy.types.Scene.fvctk_b = bpy.props.FloatProperty(name="B")
    bpy.types.Scene.fvctk_bBool = bpy.props.BoolProperty(name="B", default=True)
    bpy.types.Scene.fvctk_mode = bpy.props.EnumProperty(name="Mode", items=[("0", "Replace", ""), ("1", "Add", ""),("2", "Subtract", ""), ("3", "Multiply", ""), ("4", "Randomise", ""), ("5", "Gradient", "")], default='0',)
    bpy.types.Scene.fvctk_gradient = bpy.props.EnumProperty(name="Gradient Axis", items=[("0", "X", ""), ("1", "Y", ""),("2", "Z", "")], default='2',)
    bpy.types.Scene.fvctk_gradientTop = bpy.props.EnumProperty(name="GradientTop", items=[("0", "Highest Vert", ""), ("1", "3d Cursor", ""),("2", "VCT", "Uses location of any object with the name VCT")], default='0',)
    bpy.types.Scene.fvctk_gradientBottom = bpy.props.EnumProperty(name="GradientBottom", items=[("0", "Lowest Vert", ""),("1", "0,0,0", ""), ("2", "3d Cursor", ""),("3", "VCB", "Uses location of any object with the name VCB")], default='1',)
    bpy.types.Scene.fvctk_randomiseScope = bpy.props.EnumProperty(name="RandomiseScope", items=[("0", "Verts", ""), ("1", "Objects", "")], default='0',)
    bpy.types.Scene.fvctk_randomiseMode = bpy.props.EnumProperty(name="RandomiseMode", items=[("0", "Replace", ""), ("1", "Multipty", "")], default='0',)
    bpy.types.Scene.fvctk_picker = bpy.props.FloatVectorProperty(subtype='COLOR_GAMMA', default=(1,1,1), min=0.0, max=1.0, description="Color Picker")
    bpy.types.Scene.fvctk_pickerGradientStart = bpy.props.FloatVectorProperty(subtype='COLOR_GAMMA', default=(0,0,0), min=0.0, max=1.0, description="Color Picker")
    bpy.types.Scene.fvctk_randomColor = bpy.props.FloatVectorProperty(subtype='COLOR_GAMMA', default=(1,1,1), min=0.0, max=1.0, description="Color Picker")

    def draw(self, context):
        layout = self.layout

        obj = context.object
        scene = context.scene

        row = layout.row()
        layout.template_list("MESH_UL_uvmaps_vcols", "vcols", context.active_object.data, "vertex_colors", context.active_object.data.vertex_colors, "active_index", rows=1)

        row = layout.row()
        row.prop(context.scene, "fvctk_selection")
        row = layout.row()
        row.prop(context.scene, "fvctk_world")
        if (bpy.context.scene.fvctk_world):
            layout.label(text="World mode dosen't work yet", icon="ERROR")
        row = layout.row()
        row.prop(context.scene, "fvctk_rBool")
        row.prop(context.scene, "fvctk_gBool")
        row.prop(context.scene, "fvctk_bBool")
        row = layout.row()
        layout.label(text="Assign Vertex Colour From Values:")

        row = layout.row()
        row.prop(context.scene, "fvctk_r")
        row.prop(context.scene, "fvctk_g")
        row.prop(context.scene, "fvctk_b")
        row = layout.row()
        row.prop(context.scene, "fvctk_mode")

        row = layout.row()
        row.scale_y = 1.5
        row.operator("vertex_col.apply_rgb",text="modify vertex color", icon="COLOR")
        layout.label(text="Assign Vertex Colour From Picker:")

        row = layout.row()
        row.prop(context.scene, 'fvctk_picker', text="")
        row.prop(context.scene, "fvctk_mode")

        row = layout.row()
        row.scale_y = 1.5
        row.operator("vertex_col.apply_picker", text="modify vertex color",icon="COLOR")

        layout.label(text="Misc:")
        if (bpy.context.scene.fvctk_mode=="5"): #gradient
            row = layout.row()
            row.prop(context.scene, 'fvctk_pickerGradientStart', text="Starting Color")
            row = layout.row()
            layout.label(text="Gradient Axis:")
            row = layout.row()
            row.prop(context.scene, "fvctk_gradient",expand=True)
            row = layout.row()
            layout.label(text="Highest Point For Gradient:")
            row = layout.row()
            row.prop(context.scene, "fvctk_gradientTop",expand=True)
            row = layout.row()

            if (bpy.context.scene.fvctk_gradientTop=="2"):
                VCTfound =  False
                for o in bpy.data.objects:
                    if ("VCT" in o.name):
                        VCTfound = True
                if VCTfound == False:
                    layout.label(text="Needs an object called VCT to work!", icon="ERROR")

            layout.label(text="Lowest Point For Gradient:")
            row = layout.row()
            row.prop(context.scene, "fvctk_gradientBottom",expand=True)
            
            if (bpy.context.scene.fvctk_gradientBottom=="3"):
                VCBfound =  False
                for o in bpy.data.objects:
                    if ("VCB" in o.name):
                        VCBfound = True
                if VCBfound == False:
                    layout.label(text="Needs an object called VCB to work!", icon="ERROR")

        if (bpy.context.scene.fvctk_mode=="4"): #random
            row = layout.row()
            layout.label(text="Gradient Axis:")
            row = layout.row()
            row.prop(context.scene, "fvctk_randomiseScope",expand=True)
            #layout.label(text="Not used:")
            #row = layout.row()
            #row.prop(context.scene, "fvctk_randomiseMode",expand=True)

class ApplyVertColPicker(bpy.types.Operator):
    bl_idname = "vertex_col.apply_picker"
    bl_label = "Assign"
    bl_description = "Assign color to selected vertices for selected vertex color layer"

    def execute(self, context):
        button(0)
        return{'FINISHED'}

class ApplyVertColRGB(bpy.types.Operator):
    bl_idname = "vertex_col.apply_rgb"
    bl_label = "Assign"
    bl_description = "Assign color to selected vertices for selected vertex color layer"

    def execute(self, context):
        button(1)
        return{'FINISHED'}

def register():
    bpy.utils.register_class(FVCTK)
    bpy.utils.register_class(ApplyVertColPicker)
    bpy.utils.register_class(ApplyVertColRGB)

def unregister():
    bpy.utils.unregister_class(FVCTK)
    bpy.utils.unregister_class(ApplyVertColPicker)
    bpy.utils.unregister_class(ApplyVertColRGB)

if __name__ == "__main__":
    register()