import polyscope as ps
import numpy as np
import functions
import marching_squares as ms
import evaluation_grid as ev_grid
import function_visualization as func_visual
import sys # for printing max
import function_object as fob
import helper as helper
import polyscope.imgui as psim # for ui

# some options
ps.set_program_name("first presentation main")
ps.set_verbosity(0)
ps.set_use_prefs_file(False)
ps.set_up_dir("z_up") 

ps.init()


#helper.hlp.create_coordinate_axis()
center_point = np.asarray([[-7,-7,0]])
ps_coordinates = ps.register_point_cloud("center point", center_point, enabled=True, radius=0.0001)
axis_len = 20
x_vector = np.asarray([[axis_len,0,0]])
y_vector = np.asarray([[0,axis_len, 0]])
z_vector = np.asarray([[0,0,axis_len]])
axis_radius = 0.01
ps_coordinates.add_vector_quantity("x_vector", x_vector, axis_radius, color=(1,0,0), vectortype="ambient")
ps_coordinates.add_vector_quantity("y_vector", y_vector, axis_radius, color=(0,1,0), vectortype="ambient")
ps_coordinates.add_vector_quantity("z_vector", z_vector, axis_radius, color=(0,0,1), vectortype="ambient")


# help for creating examples more compact when there is example/subexample structure

# creates a FOB, registers it with polyscope and adds it to all relevant lists
# example visuals is e.g. all the visuals for Boolean operations
# example case groups all the structures (isocurves, meshes, planes...) belonging to
# one specific case of that example, e.g. intersection as case of Boolean
def create_subexample(FOBname, example_visuals: list, example_case: list, function, isovalue: float, center_x: float, center_y: float, sidelength:float, resolution: float, resolution_step: int):
    FOBfunction = fob.FOB(function, isovalue, center_x, center_y, sidelength, resolution, resolution_step)
    helper.hlp.ps_register_and_list_whole_FOB(FOBfunction, FOBname, example_visuals)
    example_case.append(example_visuals[-3])
    example_case.append(example_visuals[-2])
    example_case.append(example_visuals[-1])
    examples_planes.append(example_visuals[-1])
    examples_value_meshes.append(example_visuals[-2])
    examples_isocurves.append(example_visuals[-3])

# EXAMPLE CASES/SCENES
# for visibility control of elements -> for several examples:
# when using register_and_list_whole_FOB, the plane is always the last entry appended to the list
examples_planes = []
# all the (3d) value meshes, middle entry
examples_value_meshes = []
# all the isocurves, first entry
examples_isocurves = []

# EXAMPLE LEVEL SETS START
# stores all the polyscope structures belonging to example 1

example1_visuals = []
#"""
center_x1 = 0
center_y1 = 0
sidelength1 = 8
resolution1 = 0.01
resolution_step1 = 1

unit_circle_SDF = functions.circle_SDF(center_x1+0,center_y1+0,1) # good radius: 1
shifted_unit_circle_SDF = functions.circle_SDF(center_x1+0.8, center_y1+0.8, 0.8) # good radius: 0.8
function1 = functions.union(unit_circle_SDF, shifted_unit_circle_SDF)



# isovalue 0
FOBfunction1a = fob.FOB(function1, 0, center_x1, center_y1, sidelength1, resolution1, resolution_step1)
name1a = "function1_a"
helper.hlp.ps_register_and_list_whole_FOB(FOBfunction1a, name1a, example1_visuals)
examples_planes.append(example1_visuals[-1])
examples_value_meshes.append(example1_visuals[-2])
examples_isocurves.append(example1_visuals[-3])

# isovalue -0.5
FOBfunction1b = fob.FOB(function1, -0.5, center_x1, center_y1, sidelength1, resolution1, resolution_step1)
name1b = "function1_b"
helper.hlp.ps_register_and_list_whole_FOB(FOBfunction1b, name1b, example1_visuals)
examples_planes.append(example1_visuals[-1])
examples_value_meshes.append(example1_visuals[-2])
examples_isocurves.append(example1_visuals[-3])
# isovalue 0.5
FOBfunction1c = fob.FOB(function1, 0.5, center_x1, center_y1, sidelength1, resolution1, resolution_step1)
name1c = "function1_c"
helper.hlp.ps_register_and_list_whole_FOB(FOBfunction1c, name1c, example1_visuals)
examples_planes.append(example1_visuals[-1])
examples_value_meshes.append(example1_visuals[-2])
examples_isocurves.append(example1_visuals[-3])

# EXAMPLE LEVEL SETS END
#"""


#  EXAMPLE BOOLEAN OPERATIONS START
example2_visuals = [] # all visuals belonging to this example
example2_primitives = [] # stores the visuals belonging to the two functions before operation
example2_union = [] # all visuals belonging to union
example2_intersection = []
example2_complement_square = []
example2_complement_circle = []
example2_square_subtract_circle = []
example2_circle_subtract_square = []
# smooth
example2_smooth_union = []
example2_smooth_intersection = []
example2_smooth_square_subtract_circle = []
example2_smooth_circle_substract_square = []
#"""
center_x2 = 0
center_y2 = 0
sidelength2 = 4
resolution2 = 0.1
resolution_step2 = 5
isovalue2 = 0

square1 = functions.rectangle_function(center_x2-0.3, center_y2+0, 1, 1)
circle1 = functions.circle_SDF(center_x2+0.5, center_y2+0.5, 1)

function2union = functions.union(square1, circle1)
function2intersection = functions.intersection(square1, circle1)
function2complement_square = functions.complement(square1)
function2complement_circle = functions.complement(circle1)
function2difference_square = functions.subtract(square1, circle1)
function2difference_circle = functions.subtract(circle1, square1)
# smooth
function2_smooth_union = functions.smooth_union(square1, circle1, 0.3)
function2_smooth_intersection = functions.smooth_intersection(square1, circle1, 0.3)
function2_smooth_square_subtract_circle = functions.smooth_subtract(circle1, square1, 0.5)
function2_smooth_circle_substract_square = functions.smooth_subtract(square1, circle1, 0.5)


# the primitives
# left primitive
prim1_x = center_x2 - sidelength2
prim1_y = center_y2 + sidelength2
square1prim = functions.rectangle_function(prim1_x-0.3, prim1_y+0, 1, 1)
circle1prim = functions.circle_SDF(prim1_x+0.5, prim1_y+0.5,1)
name2prim1 = "function2prim1"
create_subexample(name2prim1, example2_visuals, example2_primitives, square1prim, isovalue2, prim1_x, prim1_y, sidelength2, resolution2, resolution_step2)

# right primitive
prim2_x = center_x2 + sidelength2
prim2_y = center_y2 + sidelength2
square1prim = functions.rectangle_function(prim2_x-0.3, prim2_y+0, 1, 1)
circle1prim2 = functions.circle_SDF(prim2_x+0.5, prim2_y+0.5,1)
name2prim2 = "function2prim2"
create_subexample(name2prim2, example2_visuals, example2_primitives, circle1prim2, isovalue2, prim2_x, prim2_y, sidelength2, resolution2, resolution_step2)

# REGULAR
# union
name2union = "function2union"
create_subexample(name2union, example2_visuals, example2_union, function2union, isovalue2, center_x2, center_y2, sidelength2, resolution2, resolution_step2)

# intersection
name2intersection = "function2intersection"
create_subexample(name2intersection, example2_visuals, example2_intersection,function2intersection, isovalue2, center_x2, center_y2, sidelength2, resolution2, resolution_step2)

# complement of the square
name2complement_square = "function2complement"
create_subexample(name2complement_square, example2_visuals, example2_complement_square, function2complement_square, isovalue2, center_x2, center_y2, sidelength2, resolution2, resolution_step2)

# complement of the circle
name2complement_circle = "function2complement_circle"
create_subexample(name2complement_circle, example2_visuals, example2_complement_circle, function2complement_circle, isovalue2, center_x2, center_y2, sidelength2, resolution2, resolution_step2 )

# subtract circle from square
name2difference_square = "function2difference_square"
create_subexample(name2difference_square, example2_visuals, example2_square_subtract_circle, function2difference_square, isovalue2, center_x2, center_y2, sidelength2, resolution2, resolution_step2 )

# subtract square from circle
name2difference_circle = "function2difference_circle"
create_subexample(name2difference_circle, example2_visuals, example2_circle_subtract_square, function2difference_circle, isovalue2, center_x2, center_y2, sidelength2, resolution2, resolution_step2)


# SMOOTH
# smooth union
name2smooth_union = "function2smooth_union"
create_subexample(name2smooth_union, example2_visuals, example2_smooth_union, function2_smooth_union, isovalue2, center_x2, center_y2, sidelength2, resolution2, resolution_step2)

# smooth intersection
name2smooth_intersection = "function2smooth_intersection"
create_subexample(name2smooth_intersection, example2_visuals, example2_smooth_intersection, function2_smooth_intersection, isovalue2, center_x2, center_y2, sidelength2, resolution2, resolution_step2)

# smooth square \ circle
name2smooth_square_subtract_circle = "function2smooth_square_subtract_circle"
create_subexample(name2smooth_square_subtract_circle, example2_visuals, example2_smooth_square_subtract_circle, function2_smooth_square_subtract_circle, isovalue2, center_x2, center_y2, sidelength2, resolution2, resolution_step2)

# smooth circle \ square
name2smooth_circle_substract_square = "function2smooth_circle_substract_square"
create_subexample(name2smooth_circle_substract_square, example2_visuals, example2_smooth_circle_substract_square, function2_smooth_circle_substract_square, isovalue2, center_x2, center_y2, sidelength2, resolution2, resolution_step2 )



# EXAMPLE BOOLEAN OPERATIONS END
#"""

# EXAMPLE GENERIC IMPLICIT FUNCTION VS SDF START

example3_visuals = []

center_x3 = 0
center_y3 = 0
sidelength3 = 7
resolution3 = 0.1
resolution_step3 = 1
isovalue3 = 0

implicit_circle = functions.circle_function(center_x3-sidelength3, center_y3, 1)
SDF_circle = functions.circle_SDF(center_x3+sidelength3, center_y3, 1)

# implicit circle
FOBfunction3implicit_circle = fob.FOB(implicit_circle, isovalue3, center_x3-sidelength3, center_y3, sidelength3, resolution3, resolution_step3)
name3implicit_circle = "function3implicit_circle"
helper.hlp.ps_register_and_list_whole_FOB(FOBfunction3implicit_circle, name3implicit_circle, example3_visuals)
examples_planes.append(example3_visuals[-1])
examples_value_meshes.append(example3_visuals[-2])
examples_isocurves.append(example3_visuals[-3])


# SDF circle
FOBfunction3SDF_circle = fob.FOB(SDF_circle, isovalue3, center_x3+sidelength3, center_y3, sidelength3, resolution3, resolution_step3)
name3SDF_circle = "function3SDF_circle"
helper.hlp.ps_register_and_list_whole_FOB(FOBfunction3SDF_circle, name3SDF_circle, example3_visuals)
examples_planes.append(example3_visuals[-1])
examples_value_meshes.append(example3_visuals[-2])
examples_isocurves.append(example3_visuals[-3])


# EXAMPLE GENERIC IMPLICIT FUNCTION VS SDF END


# EXAMPLE VARIOUS FUNCTIONS START
center_x4 = 0
center_y4 = 0
sidelength4 = 5
resolution4 = 0.1
resolution_step4 = 5
isovalue4 = 0


example4_visuals = []

# 3 star
example4_n5star = []
n5star = functions.nstar_SDF(0,0,1.5,9,6)
name4_n5star = "function4_n5star"
#create_subexample(name4_n5star, example4_visuals, example4_n5star, n5star, 0,0,0,4,0.005,10)
create_subexample(name4_n5star, example4_visuals, example4_n5star, n5star, isovalue4, center_x4,center_y4,sidelength4,resolution4,resolution_step4)


# diamond / cool S
example4_coolS = []
coolS = functions.cool_S_SDF(1,1)
name4_coolS = "function4_coolS"
create_subexample(name4_coolS, example4_visuals, example4_coolS, coolS, isovalue4, center_x4,center_y4,sidelength4,resolution4,resolution_step4 )


# regular Polygon
example4_batman = []
batman = functions.regular_polygon_distance(6)
name4_batman = "function4_batman"
create_subexample(name4_batman, example4_visuals, example4_batman, batman, isovalue4, center_x4,center_y4,sidelength4,resolution4,resolution_step4 )

# smile
example4_smile = []
name4_smile = "function4_smile"
mouth = functions.subtract(functions.circle_SDF(0,-0.6, 1), functions.circle_SDF(0,-0.3, 1))
left_eye = functions.subtract(functions.cool_S_SDF(-0.9,0.6), functions.rectangle_function(-0.8,0.6, 0.1, 0.3))
right_eye = functions.subtract(functions.cool_S_SDF(0.9,0.6), functions.rectangle_function(1,0.6, 0.1, 0.3))
eyes = functions.union(left_eye, right_eye)
facial_features = functions.union(eyes, mouth)
face = functions.subtract(functions.circle_SDF(0,0,2.1), facial_features)
create_subexample(name4_smile, example4_visuals, example4_smile, face, isovalue4, center_x4, center_y4, sidelength4, resolution4, resolution_step4)
#






# EXAMPLE VARIOUS FUNCTIONS END








# make all isocurves have the same color
curve_color = ([1,1,0])
initial_isocurve_radius = 0.07
for curve in examples_isocurves:
    curve.set_color(curve_color)
    curve.set_radius(0.07, relative=False)





### UI







visibility_dict = {
    "Planes" : examples_planes,
    "Value Meshes": examples_value_meshes,
    "Isocurves" : examples_isocurves
}

flag_plane = True
flag_value_mesh = True
flag_isocurve = True
visibility_flag_dict = {
        "Planes" : flag_plane,
        "Value Meshes" : flag_value_mesh,
        "Isocurves" : flag_isocurve
    }

# this will store all structures that are allowed to be shown based on the current example/operation
# selection, also the ones that are not allowed to be visible due to visibility flags
allowed_structures = []

example_dict = {
    "None" : [],
    "Level Set Methods" : example1_visuals,
    "Boolean Operations" : example2_visuals,
    "Implicit & SDF" : example3_visuals,
    "Various Functions" : example4_visuals
}



ui_text = "some input text"


ui_example_options = [ "None", "Level Set Methods", "Boolean Operations", "Implicit & SDF", "Various Functions"]
ui_example_options_selected = ui_example_options[0]

# initially, the visibiliy of all structures is disabled
for example in ui_example_options:
    for structure in example_dict[example]:
        structure.set_enabled(False)

# options for boolean operations example
ui_boolean_operations = ["None","Union", "Intersection", "Square Complement", "Circle Complement", "Square\Circle", "Circle\Square", "Smooth Union", "Smooth Intersection", "Smooth Square\Circle", "Smooth Circle\Square" ]
ui_boolean_operation_selected = ui_boolean_operations[0]
boolean_op_dict = {
    "None" : [],
    "Union": example2_union,
    "Intersection" : example2_intersection,
    "Square Complement" : example2_complement_square,
    "Circle Complement" : example2_complement_circle,
    "Square\Circle" : example2_square_subtract_circle,
    "Circle\Square" : example2_circle_subtract_square,
    "Smooth Union" : example2_smooth_union,
    "Smooth Intersection": example2_smooth_intersection,
    "Smooth Square\Circle": example2_smooth_square_subtract_circle,
    "Smooth Circle\Square" : example2_smooth_circle_substract_square
}

ui_various_shapes = ["None", "3-Star", "Diamond", "Batman", "Smile"]
ui_various_shapes_selected = ui_various_shapes[0]
various_shape_dict = {
    "None": [],
    "3-Star" : example4_n5star, 
    "Diamond" : example4_coolS,
    "Batman": example4_batman,
    "Smile" : example4_smile
}

# makes the structures belonging from list visible if their type is toggled for visibility
# differentiates between isocurves, value meshes, planes etc.
def set_example_visibility(example_list: list):
    for structure in example_list:
        for key in visibility_dict.keys():
            if structure in visibility_dict[key]:
                structure.set_enabled(visibility_flag_dict[key])


def my_function():
    # ... do something important here ...
    print("executing function")

opacity_float = 1.0
isocurve_radius = initial_isocurve_radius

# Define our callback function, which Polyscope will repeatedly execute while running the UI.
# We can write any code we want here, but in particular it is an opportunity to create ImGui 
# interface elements and define a custom UI.
def callback():


    global ui_text, ui_example_options, ui_example_options_selected,ui_boolean_operations, ui_boolean_operation_selected, flag_plane, flag_value_mesh, flag_isocurve, allowed_structures, opacity_float, isocurve_radius, ui_various_shapes, ui_various_shapes_selected



    # == Settings

    # Use settings like this to change the UI appearance.
    # Note that it is a push/pop pair, with the matching pop() below.
    psim.PushItemWidth(150)


    # == Show text in the UI

    psim.TextUnformatted("Some sample text")
    psim.TextUnformatted("An important value: {}".format(42))
    psim.Separator()

 
    changed, isocurve_radius = psim.InputFloat("Isocurve radius", isocurve_radius)
    if (changed):
        for curve in examples_isocurves:
            curve.set_radius(isocurve_radius, relative=False)

    # one opacity slider to rule them all, the new opacity only takes effect after toggling the respective
    # visibility toggle off and on again
    changed, opacity_float = psim.SliderFloat("Opacity (takes effect after visibility is toggled)", opacity_float, v_min = 0.0, v_max = 1.0)
    #psim.Separator()
    psim.TextUnformatted("Visibility")
    # Checkboxes for visibility of elements ()
    for key in visibility_dict.keys():
        changed, visibility_flag_dict[key] = psim.Checkbox(key, visibility_flag_dict[key])
        if (changed):
            for structure in allowed_structures:
                if structure in visibility_dict[key]:
                    structure.set_enabled(visibility_flag_dict[key])
                    if (visibility_flag_dict[key]):
                        structure.set_transparency(opacity_float)

    psim.Separator()




  
    # Choose the example
    psim.PushItemWidth(200)
    changed = psim.BeginCombo("Choose example", ui_example_options_selected)
    if changed:
        for example in ui_example_options:
            _, selected = psim.Selectable(example, ui_example_options_selected==example)
            if selected:
                # everything in this if block is only executed once when the example is changed
                if ui_example_options_selected != example:
                    # change visibility
                    for structure in example_dict[ui_example_options_selected]:
                        structure.set_enabled(False)
                    # for Boolean operations we still want to select the specific operation to be displayed
                    if example != "Boolean Operations":
                        set_example_visibility(example_dict[example])
                        allowed_structures = example_dict[example]
                    else: # but in Boolean, always show the primitive examples besides the actual operation
                        set_example_visibility(example2_primitives)
                        allowed_structures = example_dict[example] + example2_primitives # while doing boolean op, these are always allowed
                ui_example_options_selected = example
        psim.EndCombo()
    psim.PopItemWidth()


    # Boolean Operations
    if (ui_example_options_selected == ui_example_options[2]):

        # Choose the Boolean operation
        psim.PushItemWidth(200)
        changed = psim.BeginCombo("Choose operation", ui_boolean_operation_selected)
        if changed:
            for operation in ui_boolean_operations:
                _, selected = psim.Selectable(operation, ui_boolean_operation_selected==operation)
                if selected:
                    # everything in this if block is only executed once when the example is changed
                    if ui_boolean_operation_selected != operation:
                        for structure in boolean_op_dict[ui_boolean_operation_selected]:
                            structure.set_enabled(False)
                        set_example_visibility(boolean_op_dict[operation])
                        ui_boolean_operation_selected = operation
                        allowed_structures = boolean_op_dict[operation] + example2_primitives
            psim.EndCombo()
        psim.PopItemWidth()


    # Various Shapes
    if (ui_example_options_selected == ui_example_options[4]):
        # Choose the shape
        psim.PushItemWidth(200)
        changed = psim.BeginCombo("Choose shape", ui_various_shapes_selected)
        if changed:
            for shape in ui_various_shapes:
                _, selected = psim.Selectable(shape, ui_various_shapes_selected==shape)
                if selected:
                    # everything in this if block is only executed once when the example is changed
                    if ui_various_shapes_selected != shape:
                        for structure in various_shape_dict[ui_various_shapes_selected]:
                            structure.set_enabled(False)
                        set_example_visibility(various_shape_dict[shape])
                        ui_various_shapes_selected = shape
                        allowed_structures = various_shape_dict[shape]
            psim.EndCombo()
        psim.PopItemWidth()





                   



 
ps.set_user_callback(callback)


ps.show()