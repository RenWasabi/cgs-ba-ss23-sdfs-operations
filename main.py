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


helper.hlp.create_coordinate_axis()




# EXAMPLE LEVEL SETS START
# stores all the polyscope structures belonging to example 1
example1_visuals = []

center_x1 = 0
center_y1 = 0
sidelength1 = 5
resolution1 = 0.1
resolution_step1 = 20

unit_circle_SDF = functions.circle_SDF(center_x1+0,center_y1+0,1)
shifted_unit_circle_SDF = functions.circle_SDF(center_x1+0.8, center_y1+0.8, 0.8)
function1 = functions.union(unit_circle_SDF, shifted_unit_circle_SDF)



# isovalue 0
FOBfunction1a = fob.FOB(function1, 0, center_x1, center_y1, sidelength1, resolution1, resolution_step1)
name1a = "function1_a"
helper.hlp.ps_register_and_list_whole_FOB(FOBfunction1a, name1a, example1_visuals)
# isovalue -0.5
FOBfunction1b = fob.FOB(function1, -0.5, center_x1, center_y1, sidelength1, resolution1, resolution_step1)
name1b = "function1_b"
helper.hlp.ps_register_and_list_whole_FOB(FOBfunction1b, name1b, example1_visuals)
# isovalue 0.5
FOBfunction1c = fob.FOB(function1, 0.5, center_x1, center_y1, sidelength1, resolution1, resolution_step1)
name1c = "function1_c"
helper.hlp.ps_register_and_list_whole_FOB(FOBfunction1c, name1c, example1_visuals)

# EXAMPLE LEVEL SETS END


#  EXAMPLE BOOLEAN OPERATIONS START
example2_visuals = [] # all visuals belonging to this example
example2_primitives = [] # stores the visuals belonging to the two functions before operation
example2_union = [] # all visuals belonging to union
example2_intersection = []
example2_complement = []
example2_square_subtract_circle = []
example2_circle_subtract_square = []

center_x2 = 0
center_y2 = 0
sidelength2 = 4
resolution2 = 0.01
resolution_step2 = 10
isovalue2 = 0

square1 = functions.rectangle_function(center_x2-0.3, center_y2+0, 1, 1)
circle1 = functions.circle_SDF(center_x2+0.5, center_y2+0.5, 1)

function2union = functions.union(square1, circle1)
function2intersection = functions.intersection(square1, circle1)
function2complement = functions.complement(square1)
function2difference_square = functions.subtract(square1, circle1)
function2difference_circle = functions.subtract(circle1, square1)

# the primitives
# left primitive
prim1_x = center_x2 - sidelength2
prim1_y = center_y2 + sidelength2
square1prim = functions.rectangle_function(prim1_x-0.3, prim1_y+0, 1, 1)
circle1prim = functions.circle_SDF(prim1_x+0.5, prim1_y+0.5,1)
FOBfunction2prim1 = fob.FOB(circle1prim, isovalue2, prim1_x, prim1_y, sidelength2, resolution2, resolution_step2)
name2prim1 = "function2prim1"
helper.hlp.ps_register_and_list_whole_FOB(FOBfunction2prim1, name2prim1, example2_visuals)
example2_primitives.append(example2_visuals[len(example2_visuals)-3])
example2_primitives.append(example2_visuals[len(example2_visuals)-2])
example2_primitives.append(example2_visuals[len(example2_visuals)-1])
# right primitive
prim2_x = center_x2 + sidelength2
prim2_y = center_y2 + sidelength2
square1prim = functions.rectangle_function(prim2_x-0.3, prim2_y+0, 1, 1)
circle1prim2 = functions.circle_SDF(prim2_x+0.5, prim2_y+0.5,1)

FOBfunction2prim2 = fob.FOB(circle1prim2, isovalue2, prim2_x, prim2_y, sidelength2, resolution2, resolution_step2)
name2prim2 = "function2prim2"
helper.hlp.ps_register_and_list_whole_FOB(FOBfunction2prim2, name2prim2, example2_visuals)
example2_primitives.append(example2_visuals[len(example2_visuals)-3])
example2_primitives.append(example2_visuals[len(example2_visuals)-2])
example2_primitives.append(example2_visuals[len(example2_visuals)-1])

# union
FOBfunction2union = fob.FOB(function2union, isovalue2, center_x2, center_y2, sidelength2, resolution2, resolution_step2)
name2union = "function2union"
helper.hlp.ps_register_and_list_whole_FOB(FOBfunction2union, name2union, example2_visuals) 
# the last 3 structures belong to union
example2_union.append(example2_visuals[len(example2_visuals)-3])
example2_union.append(example2_visuals[len(example2_visuals)-2])
example2_union.append(example2_visuals[len(example2_visuals)-1])

# intersection
FOBfunction2intersection = fob.FOB(function2intersection, isovalue2, center_x2, center_y2, sidelength2, resolution2, resolution_step2)
name2intersection = "function2intersection"
helper.hlp.ps_register_and_list_whole_FOB(FOBfunction2intersection, name2intersection, example2_visuals)
example2_intersection.append(example2_visuals[len(example2_visuals)-3])
example2_intersection.append(example2_visuals[len(example2_visuals)-2])
example2_intersection.append(example2_visuals[len(example2_visuals)-1])

# complement
FOBfunction2complement = fob.FOB(function2complement, isovalue2, center_x2, center_y2, sidelength2, resolution2, resolution_step2)
name2complement = "function2complement"
helper.hlp.ps_register_and_list_whole_FOB(FOBfunction2complement, name2complement, example2_visuals)
example2_complement.append(example2_visuals[len(example2_visuals)-3])
example2_complement.append(example2_visuals[len(example2_visuals)-2])
example2_complement.append(example2_visuals[len(example2_visuals)-1])

# subtract circle from square
FOBfunction2difference_square = fob.FOB(function2difference_square, isovalue2, center_x2, center_y2, sidelength2, resolution2, resolution_step2)
name2difference_square = "function2difference_square"
helper.hlp.ps_register_and_list_whole_FOB(FOBfunction2difference_square, name2difference_square, example2_visuals)
example2_square_subtract_circle.append(example2_visuals[len(example2_visuals)-3])
example2_square_subtract_circle.append(example2_visuals[len(example2_visuals)-2])
example2_square_subtract_circle.append(example2_visuals[len(example2_visuals)-1])

# subtract square from circle
FOBfunction2difference_circle = fob.FOB(function2difference_circle, isovalue2, center_x2, center_y2, sidelength2, resolution2, resolution_step2)
name2difference_circle = "function2difference_circle"
helper.hlp.ps_register_and_list_whole_FOB(FOBfunction2difference_circle, name2difference_circle, example2_visuals)
example2_circle_subtract_square.append(example2_visuals[len(example2_visuals)-3])
example2_circle_subtract_square.append(example2_visuals[len(example2_visuals)-2])
example2_circle_subtract_square.append(example2_visuals[len(example2_visuals)-1])






# EXAMPLE BOOLEAN OPERATIONS END

"""
isocurve1 = ps.register_curve_network("isocurve1", FOBfunction1.isocurve_points, FOBfunction1.isocurve_edges)
FOBfunction1.compute_value_visuals()
value_mesh1 = ps.register_surface_mesh("value_mesh1", FOBfunction1.value_mesh_points, FOBfunction1.value_mesh_faces)
value_mesh1.add_color_quantity("value_mesh1_colors", FOBfunction1.value_mesh_colors, defined_on='faces', enabled=True)

value_plane1 = ps.register_surface_mesh("value_plane1", FOBfunction1.value_plane_points, FOBfunction1.value_mesh_faces)
value_plane1.add_color_quantity("value_plane1_colors", FOBfunction1.value_mesh_colors, defined_on='faces', enabled=True)
                                
"""
                                   








### UI

active_example = "None"


example_dict = {
    "None" : [],
    "Level Set Methods" : example1_visuals,
    "Boolean Operations" : example2_visuals
}



ui_text = "some input text"


ui_example_options = [ "None", "Level Set Methods", "Boolean Operations"]
ui_example_options_selected = ui_example_options[0]

# initially, the visibiliy of all structures is disabled
for example in ui_example_options:
    for structure in example_dict[example]:
        structure.set_enabled(False)

# options for boolean operations example
ui_boolean_operations = ["None","Union", "Intersection", "Complement", "Square\Circle", "Circle\Square" ]
ui_boolean_operation_selected = ui_boolean_operations[0]
boolean_op_dict = {
    "None" : [],
    "Union": example2_union,
    "Intersection" : example2_intersection,
    "Complement" : example2_complement,
    "Square\Circle" : example2_square_subtract_circle,
    "Circle\Square" : example2_circle_subtract_square
}





def my_function():
    # ... do something important here ...
    print("executing function")

# Define our callback function, which Polyscope will repeatedly execute while running the UI.
# We can write any code we want here, but in particular it is an opportunity to create ImGui 
# interface elements and define a custom UI.
def callback():


    global ui_text, ui_example_options, ui_example_options_selected, active_example, ui_boolean_operations, ui_boolean_operation_selected



    # == Settings

    # Use settings like this to change the UI appearance.
    # Note that it is a push/pop pair, with the matching pop() below.
    psim.PushItemWidth(150)


    # == Show text in the UI

    psim.TextUnformatted("Some sample text")
    psim.TextUnformatted("An important value: {}".format(42))
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
                    print("Changed example to " + example)
                    print("examplelist1")
                    print(len(example1_visuals))
                    # change visibility
                    for structure in example_dict[active_example]:
                        structure.set_enabled(False)
                    # for Boolean operations we still want to select the specific operation to be displayed
                    if example != "Boolean Operations":
                        for structure in example_dict[example]:
                            structure.set_enabled(True)
                    else: # but in Boolean, always show the primitive examples besides the actual operation
                        for structure in example2_primitives:
                            structure.set_enabled(True)
                    active_example = example
                ui_example_options_selected = example
        psim.EndCombo()
    psim.PopItemWidth()


    # Boolean Operations
    if (active_example == ui_example_options[2]):

        # Choose the Boolean operation
        psim.PushItemWidth(200)
        changed = psim.BeginCombo("Choose operation", ui_boolean_operation_selected)
        if changed:
            for operation in ui_boolean_operations:
                _, selected = psim.Selectable(operation, ui_boolean_operation_selected==operation)
                if selected:
                    # everything in this if block is only executed once when the example is changed
                    if ui_boolean_operation_selected != operation:
                        print("Changed boolean Operation")
                        for structure in boolean_op_dict[ui_boolean_operation_selected]:
                            structure.set_enabled(False)
                        for structure in boolean_op_dict[operation]:
                            structure.set_enabled(True)
                    ui_boolean_operation_selected = operation
            psim.EndCombo()
        psim.PopItemWidth()




 
ps.set_user_callback(callback)


ps.show()