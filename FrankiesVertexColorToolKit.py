import bpy
import bmesh
import random
import colorsys
from mathutils import Vector, Color
#some bits taken from https://blender.stackexchange.com/questions/30841/how-to-view-vertex-colors

bl_info = {
    "name": "Frankies Vertex Colour Toolkit",
    "author": "Frankie",
    "version": (0, 47),
    "blender": (2, 90, 0),
    "location": "View3D > Tool Panel",
    "description": "Lets you set vertex colours on objects or inside mesh",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "3d View"}


def interpolate(a, b, t):
    c = [0.0, 0.0, 0.0, 0.0]
    for i in range(len(a)):
        c[i] = (1 - t) * a[i] + t * b[i]
    lerp = c
    return (lerp)


def calculateColourValue(color_original, color_new, gradient_start, gradient_position):
    # adjust
    if (bpy.context.scene.fvctk_adjustBool):
        return(color_original[0] + color_new[0],
               color_original[1] + color_new[1],
               color_original[2] + color_new[2],
               color_original[3] + color_new[3])
    # adjust hsv
    if (bpy.context.scene.fvctk_hsvBool):
        color_original_hsv = colorsys.rgb_to_hsv(color_original[0],
                                                 color_original[1],
                                                 color_original[2])
        color_new_hsv = (color_original_hsv[0] - color_new[0],
                         color_original_hsv[1] - color_new[1],
                         color_original_hsv[2] - color_new[2])
        color_new = colorsys.hsv_to_rgb(color_new_hsv[0],
                                        color_new_hsv[1],
                                        color_new_hsv[2])
        return(color_new[0],
               color_new[1],
               color_new[2],
               color_original[3])
    # adjust alpha
    if (bpy.context.scene.fvctk_alphaBool):
        return(color_original[0],
               color_original[1],
               color_original[2],
               color_original[3]-color_new[3])

    # set
    if (bpy.context.scene.fvctk_stepBool):
        return(color_new[0],
               color_new[1],
               color_new[2],
               color_new[3])
    # replace
    if (bpy.context.scene.fvctk_mode == "0"):
        return(color_new)
    # add
    if (bpy.context.scene.fvctk_mode == "1"):
        return(color_original[0] + color_new[0],
               color_original[1] + color_new[1],
               color_original[2] + color_new[2],
               color_original[3] + color_new[3])
    # subtract
    if (bpy.context.scene.fvctk_mode == "2"):
        return(color_original[0] - color_new[0],
               color_original[1] - color_new[1],
               color_original[2] - color_new[2],
               color_original[3] - color_new[3])
    # multiply
    if (bpy.context.scene.fvctk_mode == "3"):
        return(color_original[0] * color_new[0],
               color_original[1] * color_new[1],
               color_original[2] * color_new[2],
               color_original[3] * color_new[3])
    # ramdomise
    if (bpy.context.scene.fvctk_mode == "4"):
        if (bpy.context.scene.fvctk_randomiseScope == "0"):
            if (bpy.context.scene.fvctk_randomiseMode == "0"):
                return(random.random(), random.random(), random.random())
            if (bpy.context.scene.fvctk_randomiseMode == "1"):
                return(random.random() * color_new[0],
                       random.random() * color_new[1],
                       random.random() * color_new[2],
                       random.random() * color_new[3])
        if (bpy.context.scene.fvctk_randomiseScope == "1"):
            if (bpy.context.scene.fvctk_randomiseMode == "0"):
                return(bpy.context.scene.fvctk_randomColor)
            if (bpy.context.scene.fvctk_randomiseMode == "1"):
                return(bpy.context.scene.fvctk_randomColor[0] * color_new[0],
                       bpy.context.scene.fvctk_randomColor[1] * color_new[1],
                       bpy.context.scene.fvctk_randomColor[2] * color_new[2],
                       bpy.context.scene.fvctk_randomColor[3] * color_new[3])
    # gradient
    if (bpy.context.scene.fvctk_mode == "5"):
        return(interpolate(gradient_start, color_new, gradient_position))
    if (bpy.context.scene.fvctk_mode == "6"):
        color = (interpolate(gradient_start, color_new, gradient_position))        
        return(color_original[0] * color[0],
               color_original[1] * color[1],
               color_original[2] * color[2],
               color_original[3] * color[3])
    if (bpy.context.scene.fvctk_mode == "7"):
        color = (interpolate(gradient_start, color_new, gradient_position))        
        return(color_original[0] * color[0] * 2,
               color_original[1] * color[1] * 2,
               color_original[2] * color[2] * 2,
               color_original[3] * color[3] * 2)
    # copy alpha
    if (bpy.context.scene.fvctk_mode == "8"):
        return(color_original[3],
               color_original[3],
               color_original[3],
               color_original[3])
    if (bpy.context.scene.fvctk_mode == "9"):
        return(color_original[1],
               color_original[1],
               color_original[1],
               color_original[1])
    # shouldn't ever get here but return something just in case
    return(1.0, 0.0, 1.0, 0.5)


def findHighestVert():
    axis = int(bpy.context.scene.fvctk_gradient)
    # highest vert
    if (bpy.context.scene.fvctk_gradientTop == "0"):
        highestVert = -999999
        for v in bpy.context.active_object.data.vertices:
            if bpy.context.scene.fvctk_selection:
                if v.select:
                    if (v.co[axis] > highestVert):
                        highestVert = v.co[axis]
            elif (v.co[axis] > highestVert):
                highestVert = v.co[axis]
        return(highestVert)
    # 3d cursor
    if (bpy.context.scene.fvctk_gradientTop == "1"):
        return(bpy.context.scene.cursor.location[axis])
    # object named VCT
    if (bpy.context.scene.fvctk_gradientTop == "2"):
        for so in bpy.context.scene.objects:
            if ("VCT" in so.name):
                return(so.location[axis])
        for o in bpy.data.objects:
            if ("VCT" in o.name):
                return(o.location[axis])
    return(0)


def findLowestVert():
    axis = int(bpy.context.scene.fvctk_gradient)
    # lowest vert
    if (bpy.context.scene.fvctk_gradientBottom == "0"):
        lowestVert = 999999
        for v in bpy.context.active_object.data.vertices:
            if bpy.context.scene.fvctk_selection:
                if v.select:
                    if (v.co[axis] < lowestVert):
                        lowestVert = v.co[axis]
            elif (v.co[axis] < lowestVert):
                lowestVert = v.co[axis]
        return(lowestVert)
    # zero
    if (bpy.context.scene.fvctk_gradientBottom == "1"):
        return(0)
    # 3d curser
    if (bpy.context.scene.fvctk_gradientBottom == "2"):
        return(bpy.context.scene.cursor.location[axis])
    # object name VCB
    if (bpy.context.scene.fvctk_gradientBottom == "3"):
        for so in bpy.context.scene.objects:
            if ("VCB" in so.name):
                return(so.location[axis])
        for o in bpy.data.objects:
            if ("VCB" in o.name):
                return(o.location[axis])
    return(0)


def modifyVertexColor(color, current_mode):
    me = bpy.context.active_object.data
    bm = bmesh.from_edit_mesh(me)
    gradientStart = findLowestVert()
    gradientEnd = findHighestVert()
    if (bpy.context.scene.fvctk_world):
        gradientStart += gradientStart + bpy.context.active_object.location[int(bpy.context.scene.fvctk_gradient)]
        gradientEnd += gradientEnd + bpy.context.active_object.location[int(bpy.context.scene.fvctk_gradient)]
    gradient_position = 0
    if gradientStart == gradientEnd:
        gradientEnd += 0.0000001  # avoid divide by zero
    # deal with selected vs all verts
    if (bpy.context.scene.fvctk_selection):
        selected = [vert.index for vert in bm.verts if vert.select]
    else:
        selected = [vert.index for vert in bm.verts]
    bpy.ops.object.mode_set(mode='EDIT', toggle=True)
    # vert mode
    # print(current_mode)
    if bpy.context.tool_settings.mesh_select_mode[2] and current_mode == "EDIT":
        for face in me.polygons:
            if face.select:
                for vert_idx, loop_idx in zip(face.vertices, face.loop_indices):
                    # find colour of existing vert
                    vc = me.vertex_colors[me.vertex_colors.active_index].data[loop_idx].color
                    # find extra data for gradient if in gradient mode
                    if (bpy.context.scene.fvctk_mode == "5" or bpy.context.scene.fvctk_mode == "6" or bpy.context.scene.fvctk_mode == "7"):
                        vh = bpy.context.active_object.data.vertices[vert_idx].co[int(bpy.context.scene.fvctk_gradient)]
                        if (bpy.context.scene.fvctk_world):
                            vh += bpy.context.active_object.location[int(bpy.context.scene.fvctk_gradient)]
                        gradient_position = ((gradientStart * -1) + vh) / ((gradientStart * -1) + gradientEnd)
                    # work out what colour the vert will be
                    c = calculateColourValue(vc, color, bpy.context.scene.fvctk_pickerGradientStart, gradient_position)

                    # and then only apply to channels that are marked as true
                    if (bpy.context.scene.fvctk_rBool):
                        me.vertex_colors[me.vertex_colors.active_index].data[loop_idx].color[0] = c[0]
                    if (bpy.context.scene.fvctk_gBool):
                        me.vertex_colors[me.vertex_colors.active_index].data[loop_idx].color[1] = c[1]
                    if (bpy.context.scene.fvctk_bBool):
                        me.vertex_colors[me.vertex_colors.active_index].data[loop_idx].color[2] = c[2]
                    if (bpy.context.scene.fvctk_aBool):
                        me.vertex_colors[me.vertex_colors.active_index].data[loop_idx].color[3] = c[3]
    # face mode
    else:
        for face in me.polygons:
            for vert_idx, loop_idx in zip(face.vertices, face.loop_indices):
                if vert_idx in selected:
                    # find colour of existing vert
                    vc = me.vertex_colors[me.vertex_colors.active_index].data[loop_idx].color
                    # find extra data for gradient if in gradient mode
                    if (bpy.context.scene.fvctk_mode == "5" or bpy.context.scene.fvctk_mode == "6" or bpy.context.scene.fvctk_mode == "7"):
                        vh = bpy.context.active_object.data.vertices[vert_idx].co[int(bpy.context.scene.fvctk_gradient)]
                        if (bpy.context.scene.fvctk_world):
                            vh += bpy.context.active_object.location[int(bpy.context.scene.fvctk_gradient)]
                        gradient_position = ((gradientStart * -1) + vh) / ((gradientStart * -1) + gradientEnd)
                    # work out what colour the vert will be
                    c = calculateColourValue(vc, color, bpy.context.scene.fvctk_pickerGradientStart, gradient_position)
                    # and then only apply to channels that are marked as true
                    if (bpy.context.scene.fvctk_rBool):
                        me.vertex_colors[me.vertex_colors.active_index].data[loop_idx].color[0] = c[0]
                    if (bpy.context.scene.fvctk_gBool):
                        me.vertex_colors[me.vertex_colors.active_index].data[loop_idx].color[1] = c[1]
                    if (bpy.context.scene.fvctk_bBool):
                        me.vertex_colors[me.vertex_colors.active_index].data[loop_idx].color[2] = c[2]
                    if (bpy.context.scene.fvctk_aBool):
                        me.vertex_colors[me.vertex_colors.active_index].data[loop_idx].color[3] = c[3]
        bpy.ops.object.mode_set(mode='EDIT', toggle=True)
    return()


def button(mode, value):
    activeObject = bpy.context.active_object
    
    for ob in bpy.context.selected_objects:
        if (ob.type == "MESH"):
            if ob.data .vertex_colors:
                vcol_layer = ob.data .vertex_colors.active
            else:
                vcol_layer = ob.data .vertex_colors.new()

            current_mode = bpy.context.object.mode
            bpy.context.view_layer.objects.active = ob
            bpy.context.scene.fvctk_randomColor = random.random(), random.random(), random.random(), random.random()

            if (mode == 0):  # from colour picker
                #print("here")
                bpy.context.object.update_from_editmode()  # maybe dont need this
                bpy.ops.object.mode_set(mode='EDIT')
                modifyVertexColor(bpy.context.scene.fvctk_picker, current_mode)
                #print(list(bpy.context.scene.fvctk_picker))

            if (mode == 1):  # from RGB floats
                bpy.context.object.update_from_editmode()  # maybe dont need this
                current_mode = bpy.context.object.mode
                bpy.ops.object.mode_set(mode='EDIT')
                # can use values either 0-255 or normalised values from 0-1
                newR = bpy.context.scene.fvctk_r
                if (newR > 1):
                    newR /= 255
                newG = bpy.context.scene.fvctk_g
                if (newG > 1):
                    newG /= 255
                newB = bpy.context.scene.fvctk_b
                if (newB > 1):
                    newB /= 255
                newA = bpy.context.scene.fvctk_a
                if (newA > 1):
                    newA /= 255
                bpy.ops.object.mode_set(mode='EDIT')
                modifyVertexColor([newR, newG, newB, newA], current_mode)

            if (mode == 2):
                bpy.context.object.update_from_editmode()  # maybe dont need this
                current_mode = bpy.context.object.mode
                bpy.ops.object.mode_set(mode='EDIT')
                value = value / 255
                modifyVertexColor([value, value, value, value], current_mode)

            bpy.ops.object.mode_set(mode=current_mode)
    bpy.context.view_layer.objects.active = activeObject


class FVCTK(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Frankies Vertex Color Toolkit"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "F VC TK"

    @classmethod
    def poll(cls, context):
        # TODO: make this work with nonetype when a script deletes something with no active selection
        if bpy.context.active_object:
            return context.active_object.type in "MESH"
        return context.mode in {'OBJECT', 'EDIT_MESH'}

    def update_HSVOffset(self, context):
        object_mode = bpy.context.object.mode
        bpy.context.scene.fvctk_hsvBool = True
        c = bpy.context.scene.fvctk_hsvOffset_cache
        v = bpy.context.scene.fvctk_hsvOffset
        bpy.context.scene.fvctk_hsvOffset_delta = (c[0] - v[0], c[1] - v[1], c[2] - v[2])
        bpy.context.scene.fvctk_hsvOffset_cache = bpy.context.scene.fvctk_hsvOffset
        bpy.context.object.update_from_editmode()  # maybe dont need this
        bpy.ops.object.mode_set(mode='EDIT')
        d = bpy.context.scene.fvctk_hsvOffset_delta
        modifyVertexColor([d[0] / 255, d[1] / 255, d[2] / 255, 1], object_mode)
        bpy.context.scene.fvctk_hsvBool = False
        bpy.ops.object.mode_set(mode=object_mode, toggle=True)

    def update_AlphaOffset(self, context):        
        object_mode = bpy.context.object.mode
        bpy.context.scene.fvctk_alphaBool = True
        c = bpy.context.scene.fvctk_alphaOffset_cache
        v = bpy.context.scene.fvctk_alphaOffset
        bpy.context.scene.fvctk_alphaOffset_delta = c - v
        bpy.context.scene.fvctk_alphaOffset_cache = bpy.context.scene.fvctk_alphaOffset
        bpy.context.object.update_from_editmode()  # maybe dont need this
        bpy.ops.object.mode_set(mode='EDIT')
        d = bpy.context.scene.fvctk_alphaOffset_delta
        modifyVertexColor([0, 0, 0, d/255], object_mode)
        bpy.context.scene.fvctk_alphaBool = False
        bpy.ops.object.mode_set(mode=object_mode, toggle=True)

    def update_colourOffset(self, context):
        object_mode = bpy.context.object.mode
        bpy.context.scene.fvctk_adjustBool = True
        bpy.context.scene.fvctk_colourOffset_delta = bpy.context.scene.fvctk_colourOffset_cache - bpy.context.scene.fvctk_colourOffset
        bpy.context.scene.fvctk_colourOffset_cache = bpy.context.scene.fvctk_colourOffset
        bpy.context.object.update_from_editmode()  # maybe dont need this
        bpy.ops.object.mode_set(mode='EDIT')
        v = bpy.context.scene.fvctk_colourOffset_delta / -255.0
        modifyVertexColor([v, v, v, v], object_mode)
        bpy.context.scene.fvctk_adjustBool = False
        bpy.ops.object.mode_set(mode=object_mode, toggle=True)

    def update_colourOffsetStep(self, context):
        for i in range(0, len(bpy.context.scene.fvctk_offsetList)):
            if not bpy.context.scene.fvctk_offsetList[i] == bpy.context.scene.fvctk_offsetList_cache[i]:
                object_mode = bpy.context.object.mode
                bpy.context.scene.fvctk_stepBool = True
                bpy.context.object.update_from_editmode()  # maybe dont need this   
                bpy.ops.object.mode_set(mode='EDIT')
                value = (255 / bpy.context.scene.fvctk_numberOfColours) * i
                value += (0.5 * (255 / bpy.context.scene.fvctk_numberOfColours))
                offset = ((255 / bpy.context.scene.fvctk_numberOfColours) / 2) * bpy.context.scene.fvctk_offsetList[i]
                value = round(value + offset)
                value = value / 255
                modifyVertexColor([value, value, value, value], object_mode)
                bpy.context.scene.fvctk_stepBool = False
                bpy.ops.object.mode_set(mode=object_mode, toggle=True)
        bpy.context.scene.fvctk_offsetList_cache = bpy.context.scene.fvctk_offsetList

    bpy.types.Scene.fvctk_selection = bpy.props.BoolProperty(name="Selected verts only", default=True)
    bpy.types.Scene.fvctk_world = bpy.props.BoolProperty(name="World space", default=False, description="Operate on verts in world space or local space")
    bpy.types.Scene.fvctk_r = bpy.props.FloatProperty(name="R")
    bpy.types.Scene.fvctk_rBool = bpy.props.BoolProperty(name="R", default=True)
    bpy.types.Scene.fvctk_g = bpy.props.FloatProperty(name="G")
    bpy.types.Scene.fvctk_gBool = bpy.props.BoolProperty(name="G", default=True)
    bpy.types.Scene.fvctk_b = bpy.props.FloatProperty(name="B")
    bpy.types.Scene.fvctk_bBool = bpy.props.BoolProperty(name="B", default=True)
    bpy.types.Scene.fvctk_a = bpy.props.FloatProperty(name="A")
    bpy.types.Scene.fvctk_aBool = bpy.props.BoolProperty(name="A", default=True)
    bpy.types.Scene.fvctk_adjustBool = bpy.props.BoolProperty(name="Adjust", default=False)
    bpy.types.Scene.fvctk_stepBool = bpy.props.BoolProperty(name="Step", default=False)
    bpy.types.Scene.fvctk_hsvBool = bpy.props.BoolProperty(name="HSV adjust", default=False)
    bpy.types.Scene.fvctk_alphaBool = bpy.props.BoolProperty(name="Alpha adjust", default=False)
    bpy.types.Scene.fvctk_mode = bpy.props.EnumProperty(name="Mode", items=[("0", "Replace", ""), ("1", "Add", ""),("2", "Subtract", ""), ("3", "Multiply", ""), ("4", "Randomise", ""), ("5", "Gradient", ""), ("6", "Gradient_Multiply", ""), ("7", "Gradient_Overlay", ""), ("8", "Copy Alpha", ""), ("9", "Use G for RGBA", "")], default='0',)
    bpy.types.Scene.fvctk_gradient = bpy.props.EnumProperty(name="Gradient Axis", items=[("0", "X", ""), ("1", "Y", ""),("2", "Z", "")], default='2',)
    bpy.types.Scene.fvctk_gradientTop = bpy.props.EnumProperty(name="GradientTop", items=[("0", "Highest Vert", ""), ("1", "3d Cursor", ""),("2", "VCT", "Uses location of any object with the name VCT")], default='0',)
    bpy.types.Scene.fvctk_gradientBottom = bpy.props.EnumProperty(name="GradientBottom", items=[("0", "Lowest Vert", ""), ("1", "0,0,0", ""), ("2", "3d Cursor", ""), ("3", "VCB", "Uses location of any object with the name VCB")], default='1',)
    bpy.types.Scene.fvctk_randomiseScope = bpy.props.EnumProperty(name="RandomiseScope", items=[("0", "Verts", ""), ("1", "Objects", "")], default='0',)
    bpy.types.Scene.fvctk_randomiseMode = bpy.props.EnumProperty(name="RandomiseMode", items=[("0", "Replace", ""), ("1", "Multipty", "")], default='0',)
    bpy.types.Scene.fvctk_picker = bpy.props.FloatVectorProperty(subtype='COLOR_GAMMA', size=4, default=(1, 1, 1, 0), min=0.0, max=1.0, description="Color Picker")
    bpy.types.Scene.fvctk_pickerGradientStart = bpy.props.FloatVectorProperty(subtype='COLOR_GAMMA', size=4, default=(0, 0, 0, 0), min=0.0, max=1.0, description="Color Picker")
    bpy.types.Scene.fvctk_randomColor = bpy.props.FloatVectorProperty(subtype='COLOR_GAMMA', size=4, default=(1, 1, 1, 0), min=0.0, max=1.0, description="Color Picker")
    bpy.types.Scene.fvctk_numberOfColours = bpy.props.IntProperty(default=1, name="Number Of Colours", min=0, max=10)
    bpy.types.Scene.fvctk_colourOffset = bpy.props.IntProperty(default=1, name="Drag To Adjust", update=update_colourOffset)
    bpy.types.Scene.fvctk_colourOffset_cache = bpy.props.IntProperty(default=1, name="amount to offset cache")
    bpy.types.Scene.fvctk_colourOffset_delta = bpy.props.IntProperty(default=1, name="amount to offset delta")
    bpy.types.Scene.fvctk_offsetList = bpy.props.FloatVectorProperty(size=10, update=update_colourOffsetStep, min=-1.0, max=1.0)
    bpy.types.Scene.fvctk_offsetList_cache = bpy.props.FloatVectorProperty(size=10, min=-1.0, max=1.0)
    bpy.types.Scene.fvctk_hsvOffset = bpy.props.IntVectorProperty(size=3, update=update_HSVOffset, name="HSV Adjust")
    bpy.types.Scene.fvctk_hsvOffset_cache = bpy.props.IntVectorProperty(size=3)
    bpy.types.Scene.fvctk_hsvOffset_delta = bpy.props.IntVectorProperty(size=3)
    bpy.types.Scene.fvctk_alphaOffset = bpy.props.IntProperty(update=update_AlphaOffset, name="AlphaOffset")
    bpy.types.Scene.fvctk_alphaOffset_cache = bpy.props.IntProperty()
    bpy.types.Scene.fvctk_alphaOffset_delta = bpy.props.IntProperty()
    bpy.types.Scene.fvctk_hsvCache = bpy.props.IntVectorProperty(size=3) # is this used?    
    bpy.types.Scene.fvctk_savedColour = bpy.props.FloatVectorProperty(subtype='COLOR_GAMMA', min=0.0, max=1.0)
    bpy.types.Scene.fvctk_savedColour1 = bpy.props.FloatVectorProperty(subtype='COLOR_GAMMA', min=0.0, max=1.0)
    bpy.types.Scene.fvctk_savedColour2 = bpy.props.FloatVectorProperty(subtype='COLOR_GAMMA', min=0.0, max=1.0)
    bpy.types.Scene.fvctk_savedColour3 = bpy.props.FloatVectorProperty(subtype='COLOR_GAMMA', min=0.0, max=1.0)
    bpy.types.Scene.fvctk_savedColour4 = bpy.props.FloatVectorProperty(subtype='COLOR_GAMMA', min=0.0, max=1.0)
    bpy.types.Scene.fvctk_savedColour5 = bpy.props.FloatVectorProperty(subtype='COLOR_GAMMA', min=0.0, max=1.0)
    bpy.types.Scene.fvctk_savedColour6 = bpy.props.FloatVectorProperty(subtype='COLOR_GAMMA', min=0.0, max=1.0)
    bpy.types.Scene.fvctk_savedColour7 = bpy.props.FloatVectorProperty(subtype='COLOR_GAMMA', min=0.0, max=1.0)


    def draw(self, context):
        layout = self.layout

        obj = context.object
        scene = context.scene

        row = layout.row()

        layout.template_list("MESH_UL_vcols", "vcols", context.active_object.data, "vertex_colors", context.active_object.data.vertex_colors, "active_index", rows=1)

        row = layout.row()
        row.prop(context.scene, "fvctk_selection")
        row = layout.row()
        # row.prop(context.scene, "fvctk_world")
        if (bpy.context.scene.fvctk_world):
            layout.label(text="World mode dosen't work yet", icon="ERROR")
        row = layout.row()
        row.prop(context.scene, "fvctk_rBool")
        row.prop(context.scene, "fvctk_gBool")
        row.prop(context.scene, "fvctk_bBool")
        row.prop(context.scene, "fvctk_aBool")
        row = layout.row()
        layout.separator()

        box = layout.box()
        row = box.row()
        row.label(text="Assign Vertex Colour From Values:")
        row = box.row()
        row.prop(context.scene, "fvctk_r")
        row.prop(context.scene, "fvctk_g")
        row.prop(context.scene, "fvctk_b")
        row = box.row()
        row.prop(context.scene, "fvctk_a")
        row = box.row()
        row.prop(context.scene, "fvctk_mode")
        row = box.row()
        row.scale_y = 1.5
        row.operator("vertex_col.apply_rgb", text="modify vertex color", icon="VPAINT_HLT")

        layout.separator()
        box = layout.box()
        row = box.row()

        box.label(text="Assign Vertex Colour From Picker")
        row = box.row()
        row.prop(context.scene, 'fvctk_picker', text="")
        row.prop(context.scene, "fvctk_mode")
        row = box.row()
        row.scale_y = 1.5
        row.operator("vertex_col.apply_picker", text="modify vertex color", icon="VPAINT_HLT")
        if (bpy.context.scene.fvctk_mode == "5" or bpy.context.scene.fvctk_mode == "6" or bpy.context.scene.fvctk_mode == "7"):   # gradient
            row = box.row()            
            row.prop(context.scene, 'fvctk_pickerGradientStart', text="Starting Color")
            row = box.row()
            row.prop(context.scene, "fvctk_gradient", text="Axis")
            row = box.row()
            row.prop(context.scene, "fvctk_gradientTop", text="Top")
            row = box.row()
            row.prop(context.scene, "fvctk_gradientBottom", text="Bottom")
            row = box.row()            
            if (bpy.context.scene.fvctk_gradientTop == "2"):
                VCTfound = False
                for o in bpy.data.objects:
                    if ("VCT" in o.name):
                        VCTfound = True
                if not VCTfound:
                    box.label(text="Needs an object called VCT to work!", icon="ERROR")            
            if (bpy.context.scene.fvctk_gradientBottom == "3"):
                VCBfound = False
                for o in bpy.data.objects:
                    if ("VCB" in o.name):
                        VCBfound = True
                if not VCBfound:
                    box.label(text="Needs an object called VCB to work!", icon="ERROR")
        if (bpy.context.scene.fvctk_mode == "4"):  # random
            row = box.row()
            layout.label(text="Gradient Axis:")
            row = box.row()
            row.prop(context.scene, "fvctk_randomiseScope", expand=True)
            # layout.label(text="Not used:")
            # row = layout.row()
            # row.prop(context.scene, "fvctk_randomiseMode",expand=True)

        layout.separator()
        row = layout.box()
        row.label(text="Drag To Adjust Vertex Colours:")
        split = row.split(factor=0.2)
        col_1 = split.column()
        col_2 = split.column()
        col_2.use_property_split = True
        col_2.prop(context.scene, "fvctk_hsvOffset", text="")
        col_1.label(text='Hue')
        col_1.label(text='Sat')
        col_1.label(text='Val')
        col_2.prop(context.scene, "fvctk_alphaOffset", text="")
        col_1.label(text='Alpha')
        # row = box.row()
        # row.prop(context.scene, "fvctk_colourOffset")

        layout.separator()
        box = layout.box()
        row = box.row()
        row.label(text="Value bands")
        row.prop(context.scene, "fvctk_numberOfColours")
        row = box.row()
        props = row.operator("vertex_col.apply", text="Min", icon="RADIOBUT_OFF")
        props.mode = 2
        props.value = 0
        props = row.operator("vertex_col.apply", text="Max", icon="RADIOBUT_ON")
        props.mode = 2
        props.value = 255
        row = box.row()
        for i in range(bpy.context.scene.fvctk_numberOfColours):
            row = box.row()
            value = (255 / bpy.context.scene.fvctk_numberOfColours) * i
            value += (0.5 * (255 / bpy.context.scene.fvctk_numberOfColours))
            offset = ((255 / bpy.context.scene.fvctk_numberOfColours) / 2) * bpy.context.scene.fvctk_offsetList[i]
            value = round(value + offset)
            props = row.operator("vertex_col.apply", text="Set " + str(value), icon="VPAINT_HLT")
            props.mode = 2
            props.value = value
            row.prop(context.scene, "fvctk_offsetList", index=i, slider=True, text=str("adjust"))
            row = box.row()        
        row = box.row()
        row.prop(context.scene, 'fvctk_savedColour', text="")
        row.prop(context.scene, 'fvctk_savedColour1', text="")
        row.prop(context.scene, 'fvctk_savedColour2', text="")
        row.prop(context.scene, 'fvctk_savedColour3', text="")
        row = box.row()
        row.prop(context.scene, 'fvctk_savedColour4', text="")
        row.prop(context.scene, 'fvctk_savedColour5', text="")
        row.prop(context.scene, 'fvctk_savedColour6', text="")
        row.prop(context.scene, 'fvctk_savedColour7', text="")
        row = box.row()


#  todo depricate, use applyvertcol
class ApplyVertColPicker(bpy.types.Operator):
    bl_idname = "vertex_col.apply_picker"
    bl_label = "Assign"
    bl_description = "Assign color to selected vertices for selected vertex color layer"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        bpy.context.scene.fvctk_hsvBool = False
        button(mode=0, value=0)
        return{'FINISHED'}


#  todo depricate, use applyvertcol
class ApplyVertColRGB(bpy.types.Operator):
    bl_idname = "vertex_col.apply_rgb"
    bl_label = "Assign"
    bl_description = "Assign color to selected vertices for selected vertex color layer"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        bpy.context.scene.fvctk_hsvBool = False
        button(mode=1, value=0)
        return{'FINISHED'}


class ApplyVertCol(bpy.types.Operator):
    bl_idname = "vertex_col.apply"
    bl_label = "Assign"
    bl_description = "Assign color to selected vertices for selected vertex color layer"
    bl_options = {"REGISTER", "UNDO"}

    mode: bpy.props.IntProperty(
        name="mode",
        default=0
    )

    value: bpy.props.IntProperty(
        name="value",
        default=0
    )

    def execute(self, context):
        button(self.mode, self.value)
        return{'FINISHED'}


def register():
    bpy.utils.register_class(FVCTK)
    bpy.utils.register_class(ApplyVertColPicker)
    bpy.utils.register_class(ApplyVertColRGB)
    bpy.utils.register_class(ApplyVertCol)


def unregister():
    bpy.utils.unregister_class(FVCTK)
    bpy.utils.unregister_class(ApplyVertColPicker)
    bpy.utils.unregister_class(ApplyVertColRGB)
    bpy.utils.unregister_class(ApplyVertCol)

if __name__ == "__main__":
    register()