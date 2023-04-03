import datetime
import os
import PyQt5

#from ete3 import Tree, TreeStyle, NodeStyle, TextFace
#from ete3 import Tree, PhyloTree,TreeStyle, NodeStyle, faces, AttrFace, CircleFace, TextFace

from tools.Utils import check_create_dir


def TreeViewProcess(input_file_path, parameter_dict, output_path):
    try:
        mode, if_show_branch_length, branch_vertical_margin, scale = \
            parameter_dict["tree_mode"], parameter_dict["if_show_branch"], int(
                parameter_dict["branch_vertical_margin"]), \
            int(parameter_dict["tree_scale"])
        # tree
        tree = Tree(input_file_path)

        # Basic tree style
        ts = TreeStyle()
        ts.show_scale = True
        ts.show_leaf_name = False
        if mode == "Rectangular":
            mode = "r"
        elif mode == "Circular":
            mode = "c"
        if if_show_branch_length == "yes":
            if_show_branch_length = True
        elif if_show_branch_length == "no":
            if_show_branch_length = False
        ts.mode = mode
        ts.show_branch_length = if_show_branch_length
        ts.branch_vertical_margin = branch_vertical_margin
        ts.scale = scale

        # Annotate tree
        for node in tree.traverse():
            if node.is_leaf():
                nstyle = NodeStyle()
                node.img_style["size"] = 5
                node.img_style["shape"] = "square"  
                node.img_style["fgcolor"] = "darkred"
                # Show leaf labels
                name_face = TextFace(node.name, fgcolor="gray", fsize=8)
                node.add_face(name_face, column=0, position='branch-right')

            else:
                nstyle = NodeStyle()
                node.img_style["size"] = 3
                node.img_style["shape"] = "circle" 
                node.img_style["fgcolor"] = "green"

        current_time = datetime.datetime.now().strftime('%b%d_%H-%M-%S')
        output_file_name = current_time + "_result_TreeView"
        output_file_path = os.path.join(output_path, output_file_name)
        check_create_dir(output_file_path)
        # tree.show(tree_style=ts)

        tree.render("%%inline", dpi=300, tree_style=ts, w=600)  
        show_img_save_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                                          "static",
                                          "output_TreeView", output_file_name)
        check_create_dir(show_img_save_path)
        show_img_save_path = os.path.join(show_img_save_path, "mytree.png")
        tree.render(os.path.join(output_file_path, "mytree.png"), dpi=300, tree_style=ts, w=600)  # download as png
        tree.render(show_img_save_path, dpi=300, tree_style=ts, w=600)
        tree.render(os.path.join(output_file_path, "mytree.svg"), dpi=300, tree_style=ts, w=600)  # download as svg
        tree.render(os.path.join(output_file_path, "mytree.pdf"), dpi=300, tree_style=ts, w=600)  # download as pdf

        return_data = dict()
        return_data['status'] = "success"
        return_data['result_path'] = output_file_path
        return_data['show_img_path'] = os.path.join("..", "static", "output_TreeView", output_file_name, "mytree.png")
        return return_data
    except Exception as e:
        return_data = dict()
        return_data['status'] = "failed"
        return_data['result_path'] = ""
        print(e)
        return return_data


if __name__ == '__main__':

    # outside program to create newick tree
    tree_str = './example.nwk'

    # tree
    tree = Tree(tree_str)

    # Basic tree style
    ts = TreeStyle()
    ts.show_scale = True
    ts.show_leaf_name = False

    # Show branch length?
    ts.mode = "r"  

    ts.show_branch_length = True  

    ts.branch_vertical_margin = 5  # *********************** The default is 5, Settable parameters 1-100<optional>***********************

    ts.scale = 2000  # ***********************The default value is 2000, and adjustment parameters can be set from 500 to 10000<optional>***********************

    # Annotate tree
    for node in tree.traverse():
        if node.is_leaf():
            nstyle = NodeStyle()
            node.img_style["size"] = 5
            node.img_style["shape"] = "square"  ## “circle”, “square” or “sphere”
            node.img_style["fgcolor"] = "darkred"
            # Show leaf labels
            name_face = TextFace(node.name, fgcolor="gray", fsize=8)
            node.add_face(name_face, column=0, position='branch-right')

        else:
            # Sets the style of internal nodes
            nstyle = NodeStyle()
            node.img_style["size"] = 3
            node.img_style["shape"] = "circle"  ## “circle”, “square” or “sphere”
            node.img_style["fgcolor"] = "green"

    tree.render("%%inline", dpi=300, tree_style=ts, w=600)  

