from subprocess import *
import os
import itertools


# define variable string elements

colors = ["blue","red", "yellow","green"]
color_names = ["B","R", "Y","G"]

#colors = ["blue","red"]
#color_names = ["Blau","Rot"]

plabels = ["\\text{\\SI}","\\leftmoon","\\text{\\blitze}","\\varheartsuit","\\text{\\ding{96}}","\\text{\epsdice{5}}"]
plabel_names = ["Sonne", "Mond","Blitz","Herz", "Blume","Wuerfel"]

#plabels = ["\\text{\\SI}","\\leftmoon","\\text{\\blitze}","\\varheartsuit"]
#plabel_names = ["Sonne", "Mond","Blitz","Herz"]

clabels = ["\\text{\\Letter}","\\text{\\Rightscissors}","\\text{\\ding{46}}","\\star","\\text{\\bell}","\\text{\\clock}"]
clabel_names = ["Brief","Schere", "Stifte","Sterne","Glocken","Uhren"]

#clabels = ["\\text{\\Letter}","\\text{\\Rightscissors}"]
#clabel_names = ["Brief","Schere"]

shapes = ["circle","regular polygon, regular polygon sides=4",\
          "regular polygon, regular polygon sides=3",\
          "regular polygon, regular polygon sides=5"]
shape_names = ["Kreise", "Vierecke", "Dreiecke", "Fuenfecke"]


# define text blocks

file_header = """
\\documentclass{article}

\\usepackage[palatino]{mypackages}\\usepackage{mycommands}

\\usepackage[]{mathdesign}
\\usepackage{MnSymbol}
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
    return """\\begin{tikzpicture}[rounded corners,node distance = 3cm]

    \\tikzset{ctype/.style={circle,thick,minimum
      width=18mm},
      htype/.style={},
      p6type/.style={thick,minimum width=8mm},
      p4type/.style={circle,thick,minimum width=14mm},
      arrow/.style={-,very thick}}\n"""

def powerset(seq):
    if len(seq) > 0:
        head = powerset(seq[:-1])
        return head + [item + [seq[-1]] for item in head]
    else:
        return [[]]

def make_periphery(hidden=False, labeled = False, connections = [],labels=[],color_list=[],color="",shape=""):

    if labeled:
        directions = ["above left of = c0", "above right of = c0",\
                  "below right of = c0", "below left of = c0"]
    else:
        directions = ["above left of = c0", "above of = c0", "above right of = c0",\
                  "below right of = c0", "below of = c0", "below left of = c0"]

    periphery = "\\begin{pgfonlayer}{foreground}\n\n"

    if labeled:
        for i in range(4):
            periphery += "\\node [p4type, ,draw=black!70,fill=%s!50,%s]\
              (p%s)   {\\Huge{$%s$}};\n\n" % (colors[color_list[i]],directions[i],i,plabels[labels[i]])
    else:
        for i in range(6):
            periphery += "\\node [p6type,%s,draw=black!70,fill=%s!50, %s]  (p%s)   {};\n\n"\
             % (shape,color,directions[i],i)

    periphery += "\\end{pgfonlayer}"

    for connection in connections:
        periphery += '\\draw [arrow] (c0) to (p%s);\n\n' % str(connection)

    if not hidden:
        return periphery
    else:
        return periphery + """
        
         \\node at (0,-1.7) [semicircle,shape border rotate
          =180,draw=black!70,fill=gray!80, minimum size = 4cm]  {};
        
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

for s,shape in enumerate(shapes):
    for c,color in enumerate(colors):    
        for j,clabel in enumerate(clabels):
            out_string = file_header
            pset6 = powerset(range(6))
            pset3 = powerset(range(3))
            for connections in pset6:
                out_string += make_tikzheader() + tikzbackground + make_center(clabel)
                out_string += make_periphery(hidden=False,connections=connections,shape=shape)
                out_string += tikzbackground + tikzfooter
            for connections in pset3:
                out_string += make_tikzheader() + tikzbackground + make_center(clabel)
                out_string += make_periphery(hidden=True,connections=connections,shape=shape)
                out_string += tikzbackground + tikzfooter
            out_string += file_footer
            file_dir = os.path.join(os.path.dirname(__file__), 'Pics','Unlabeled')
            file_name = os.path.join(file_dir, clabel_names[j] + "-" + shape_names[s] + "-" +color_names[c])
            f = open(file_name+'.tex','w')
            f.write(out_string)
            f.close()
            os.chdir(file_dir)
#            call(["pdflatex", file_name+".tex"])
            #call(["open", "-a", "Skim", file_name+".pdf"])


########################
### Generate Labeled ### 
########################


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
#            pset6 = powerset(range(4))
#            pset3 = powerset(range(2))
#            for connections in pset6:
#                out_string += make_tikzheader() + tikzbackground + make_center(clabel)
#                out_string += make_periphery(hidden=False,labeled=True,\
#                                             connections=connections,labels=label_permutation,\
#                                             color_list=color_permutation)
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
#            os.chdir(file_dir)
#            call(["pdflatex", file_name+".tex"])
##            #call(["open", "-a", "Skim", file_name+".pdf"])


