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
resolution1 = 0.01
resolution_step1 = 5

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
example2_visuals = []

center_x2 = 0
center_y2 = 0
sidelength2 = 4
resolution2 = 0.05
resolution_step2 = 15
isovalue2 = 0

square1 = functions.rectangle_function(center_x2-0.3, center_y2+0, 1, 1)
circle1 = functions.circle_SDF(center_x2+0.5, center_y2+0.5, 1)

function2union = functions.union(square1, circle1)
function2intersection = functions.intersection(square1, circle1)
function2complement = functions.complement(square1)
function2difference_square = functions.subtract(square1, circle1)
function2difference_circle = functions.subtract(circle1, square1)

# render all in same spot, choose enabled one with button

FOBfunction2union = fob.FOB(function2union, isovalue2, center_x2, center_y2, sidelength2, resolution2, resolution_step2)
name2union = "function2union"
helper.hlp.ps_register_and_list_whole_FOB(FOBfunction2union, name2union, example2_visuals)
FOBfunction2intersection = fob.FOB(function2intersection, isovalue2, center_x2, center_y2, sidelength2, resolution2, resolution_step2)
name2intersection = "function2intersection"
helper.hlp.ps_register_and_list_whole_FOB(FOBfunction2intersection, name2intersection, example2_visuals)
FOBfunction2complement = fob.FOB(function2complement, isovalue2, center_x2, center_y2, sidelength2, resolution2, resolution_step2)
name2complement = "function2complement"
helper.hlp.ps_register_and_list_whole_FOB(FOBfunction2complement, name2complement, example2_visuals)
FOBfunction2difference_square = fob.FOB(function2difference_square, isovalue2, center_x2, center_y2, sidelength2, resolution2, resolution_step2)
name2difference_square = "function2difference_square"
helper.hlp.ps_register_and_list_whole_FOB(FOBfunction2difference_square, name2difference_square, example2_visuals)
FOBfunction2difference_circle = fob.FOB(function2difference_circle, isovalue2, center_x2, center_y2, sidelength2, resolution2, resolution_step2)
name2difference_circle = "function2difference_circle"
helper.hlp.ps_register_and_list_whole_FOB(FOBfunction2difference_circle, name2difference_circle, example2_visuals)






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

for example in ui_example_options:
    for structure in example_dict[example]:
        structure.set_enabled(False)


def my_function():
    # ... do something important here ...
    print("executing function")

# Define our callback function, which Polyscope will repeatedly execute while running the UI.
# We can write any code we want here, but in particular it is an opportunity to create ImGui 
# interface elements and define a custom UI.
def callback():


    global ui_text, ui_example_options, ui_example_options_selected, active_example



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
                    for structure in example_dict[example]:
                        structure.set_enabled(True)
                    active_example = example
                ui_example_options_selected = example
        psim.EndCombo()
    psim.PopItemWidth()





 
ps.set_user_callback(callback)


ps.show()