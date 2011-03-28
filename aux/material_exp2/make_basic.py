from subprocess import *
import os
import itertools


# define variable string elements

#colors = ["blue","red", "yellow","green"]
#color_names = ["B","R", "Y","G"]

colors = ["blue"]
color_names = ["Blau"]

#plabels = ["\\text{\\SI}","\\leftmoon","\\text{\\blitze}","\\varheartsuit","\\text{\\ding{96}}"]
#plabel_names = ["Sonne", "Mond","Blitz","Herz", "Blume"]

plabels = ["\\text{\\SI}","\\leftmoon"]
plabel_names = ["Sonne", "Mond"]

#clabels = ["\\text{\\Letter}","\\text{\\Rightscissors}","\\text{\\ding{46}}","\\star","\\text{\\bell}","\\text{\\clock}"]
#clabel_names = ["Brief","Schere", "Stifte","Sterne","Glocken","Uhren"]

clabels = ["\\text{\\Letter}"]
clabel_names = ["Brief"]

shapes = ["circle"]
shape_names = ["Kreise"]

#shapes = ["circle","semicircle,shape border rotate=180",\
#          "regular polygon, regular polygon sides=4",\
#          "regular polygon, regular polygon sides=3",\
#          "regular polygon, regular polygon sides=6",\
#          "regular polygon, regular polygon sides=8"]
#shape_names = ["Kreise", "Halbkreise", "Vierecke", "Dreiecke", "Sechsecke","Achtecke"]


# define text blocks

file_header = """
\\documentclass{article}

\\usepackage[palatino]{mypackages}\\usepackage{mycommands}

\\usepackage[]{mathdesign}
%\\usepackage{MnSymbol}
\\usepackage{ulsy}
\\usepackage{wasysym}
\\usepackage{ascii}
\\usepackage{marvosym}
\\usepackage{pifont}
\\usepackage{phaistos}
\\usepackage{epsdice}
\\usepackage{skak}

\\usepackage{verbatim}
\\usepackage[active,tightpage]{preview}
\\PreviewEnvironment{tikzpicture}
\\setlength\\PreviewBorder{20pt}

\\usetikzlibrary{shapes.geometric}
\pgfdeclarelayer{foreground}
\pgfsetlayers{background,main,foreground}

\\begin{document}
"""

def make_tikzheader():
    return """\\begin{tikzpicture}[node distance = 3cm]

    \\tikzset{ctype/.style={circle,thick,minimum
      width=18mm},
      htype/.style={},
      p6type/.style={thick,minimum width=14mm},
      p4type/.style={thick,minimum width=14mm},
      arrow/.style={-,very thick}}\n"""

def powerset(seq):
    if len(seq) > 0:
        head = powerset(seq[:-1])
        return head + [item + [seq[-1]] for item in head]
    else:
        return [[]]

def make_periphery(hidden=False, labeled = False, connections = [],labels=[],color="",shape="",p_label_pos=[0,0,0,0,0,0],p_label="",shape_pos=[]):
    """
        itype:
            hidden = integer values representing how much of the figure is hidden
                0: nothing is hidden
                1: lower half is hidden
                2: positions 4 and 5 are hidden
                3: positions 5 and 6 are hidden
                4: all is hidden
    """

    directions = ["above left of = c0", "above of = c0", "above right of = c0",\
                  "below right of = c0", "below of = c0", "below left of = c0"]

    periphery = "\\begin{pgfonlayer}{foreground}\n\n"

    if labeled:
        for i in range(6):
            if p_label_pos[i] == 1:
                periphery += "\\node [p4type,%s,draw=black!70,fill=%s!50,%s]\
                  (p%s)   {\\Huge{$%s$}};\n\n" % (shapes[shape_pos[i]],color,directions[i],i,p_label)
            else:
                periphery += "\\node [p4type,%s,draw=black!70,fill=%s!50, %s]  (p%s)   {};\n\n"\
                    % (shapes[shape_pos[i]],color,directions[i],i)
    else:
        for i in range(6):
            periphery += "\\node [p6type,%s,draw=black!70,fill=%s!50, %s]  (p%s)   {};\n\n"\
             % (shape,color,directions[i],i)

    periphery += "\\end{pgfonlayer}"

    for connection in connections:
        periphery += '\\draw [arrow] (c0) to (p%s);\n\n' % str(connection)

    if hidden == 0:
        return periphery
    elif hidden == 1:
        return periphery + """
        
                 \\begin{scope}

                      \\clip (-4.1,-4.1) rectangle (4.1,0);

                      \\node at (0,0) [circle,draw=gray!80,fill=gray!80,minimum size = 8.1cm] {};

                \\end{scope}
        
        """
    elif hidden == 2: # hide positions 4 and 5
        return periphery + """
        
                 \\begin{scope}

                      \\clip (-4.1,-4.1) rectangle (4.1,0);
                      
                      \\clip[rotate = 65] (-4.1,-4.1) rectangle (4.1,0);

                      \\node at (0,0) [circle,draw=gray!80,fill=gray!80,minimum size = 8.1cm] {};

                \\end{scope}
        
        """
    elif hidden == 3: # hide positions 5 and 6
        return periphery + """
        
                 \\begin{scope}

                      \\clip (-4.1,-4.1) rectangle (4.1,0);
                      
                      \\clip[rotate = -65] (-4.1,-4.1) rectangle (4.1,0);

                      \\node at (0,0) [circle,draw=gray!80,fill=gray!80,minimum size = 8.1cm] {};

                \\end{scope}
        
        """
    elif hidden == 4: # all is hidden
        return periphery + """
        
                 \\begin{scope}

                      \\node at (0,0) [circle,draw=gray!80,fill=gray!80,minimum size = 8.1cm] {};

                \\end{scope}
        
        """

tikzbackground = """\\begin{pgfonlayer}{background}
      \\node at (0,0) [circle,draw=black!70,fill=gray!20,minimum size = 8.5cm] {};
    \\end{pgfonlayer}"""

def make_center(clabel=''):
    return """\\begin{pgfonlayer}{foreground}
      
      \\node at (0,0)  [ctype,draw=black!70,fill=brown!20] 
      (c0)   {\\textcolor{black}{\\Huge{$%s$}}}; 

    \\end{pgfonlayer}\n""" % clabel 

tikzfooter = """\\end{tikzpicture}\n\n"""

file_footer = "\\end{document}"

###########################
### Generate Unlabelled ###
###########################

counter = 1

for s,shape in enumerate(shapes):
    for c,color in enumerate(colors):    
        for j,clabel in enumerate(clabels):
            connections = [powerset(range(6)),powerset(range(3)),powerset([0,1,2,5]),powerset([0,1,2,3]),powerset([])]
            for hide_int in range(5):
                for connect in connections[hide_int]:
                    out_string = file_header
                    out_string += make_tikzheader() + tikzbackground + make_center(clabel)
                    out_string += make_periphery(hidden=hide_int,connections=connect,shape=shape,color=color)
                    out_string += tikzbackground + tikzfooter
                    out_string += file_footer
                    file_dir = os.path.join(os.path.dirname(__file__), 'Pics','Unlabeled')
                    file_name = os.path.join(file_dir, str(counter))
                    f = open(file_name+'.tex','w')
                    f.write(out_string)
                    f.close()
                    counter += 1
#            os.chdir(file_dir)
#            call(["pdflatex", file_name+".tex"])
#            call(["open", "-a", "Skim", file_name+".pdf"])


########################
### Generate Labeled ### 
########################

def combinations_with_replacement(iterable, r):
    pool = tuple(iterable)
    n = len(pool)
    for indices in itertools.product(range(n), repeat=r):
            yield tuple(pool[i] for i in indices)

#for p_label in range(len(plabels)):
#    for p_label_pos in combinations_with_replacement(range(2),6):
#        for shape_pair in itertools.combinations(range(len(shapes)),2):
#            shape_pos_name = shape_names[shape_pair[0]] + "-" + shape_names[shape_pair[1]] 
#            for shape_pos in combinations_with_replacement(shape_pair,6):
#                shape_pos_name = shape_names[shape_pair[0]] + "-" + shape_names[shape_pair[1]] +"-" + str(shape_pos)
#                for c,color in enumerate(colors):    
#                    for j,clabel in enumerate(clabels):
#                        out_string = file_header
#                        connections = [powerset(range(6)),powerset(range(3)),powerset([0,1,2,5]),powerset([0,1,2,3]),powerset([])]
#                        for hide_int in range(5):
#                            for connect in connections[hide_int]:
#                                out_string += make_tikzheader() + tikzbackground + make_center(clabel)
#                                out_string += make_periphery(hidden=hide_int,labeled = True, connections=connect,\
#                                            color=color,p_label=plabels[p_label],p_label_pos=p_label_pos,shape_pos=shape_pos)
#                                out_string += tikzbackground + tikzfooter
#                        out_string += file_footer
#                        file_dir = os.path.join(os.path.dirname(__file__), 'Pics','Labeled')
#                        file_name = os.path.join(file_dir, clabel_names[j] + "-" + color_names[c] + "-" +plabel_names[p_label] + "-" + str(p_label_pos) + "-" + shape_pos_name)
#                        f = open(file_name+'.tex','w')
#                        f.write(out_string)
#                        f.close()
#                        os.chdir(file_dir)
#                        call(["pdflatex", file_name+".tex"])
#                        call(["open", "-a", "Skim", file_name+".pdf"])
        
    

### BROKEN or old?

#for label_permutation in itertools.permutations(range(len(plabels))):
#    p_permut_name = ""
#    for p in label_permutation:
#        p_permut_name += plabel_names[p]
#    for color_permutation in itertools.permutations(range(len(colors))):
#        c_permut_name = ""
#        for p in color_permutation:
#            c_permut_name += color_names[p]
#        for j,clabel in enumerate(clabels):
#            out_string = file_header
#            connections = [powerset(range(6)),powerset(range(3)),powerset([0,1,2,5]),powerset([0,1,2,3]),powerset([])]
#            for hide_int in range(5):
#                for connect in connections[hide_int]:
#                    out_string += make_tikzheader() + tikzbackground + make_center(clabel)
#                    out_string += make_periphery(hidden=hide_int,labeled = True, connections=connect,\
#                                color=color,p_label=plabels[p_label],p_label_pos=[0,0,0,0,0,0],shape_pos=[0,0,0,0,0,0])
#                out_string += tikzbackground + tikzfooter
#            for connections in pset3:
#                out_string += make_tikzheader() + tikzbackground + make_center(clabel)
#                out_string += make_periphery(hidden=True,labeled=True,\
#                                             connections=connections,labels=label_permutation,\
#                                             color_list=color_permutation)
#                out_string += tikzbackground + tikzfooter
#            out_string += file_footer
#            file_dir = os.path.join(os.path.dirname(__file__), 'Pics','Labeled')
#            file_name = os.path.join(file_dir,clabel_names[j] + "-" + c_permut_name + "-" + p_permut_name)
#            f = open(file_name+'.tex','w')
#            f.write(out_string)
#            f.close()
##            os.chdir(file_dir)
##            call(["pdflatex", file_name+".tex"])
####            #call(["open", "-a", "Skim", file_name+".pdf"])


