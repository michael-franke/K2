from subprocess import *
import os
import itertools


# define variable string elements

colors = ["blue","red", "yellow","green"]
color_names = ["Blau","Rot", "Gelb","Gruen"]

#colors = ["blue","red"]
#color_names = ["Blau","Rot"]

#plabels = ["\\text{\\SI}","\\leftmoon","\\text{\\blitze}","\\varheartsuit","\\text{\\ding{96}}","\\text{\epsdice{5}}"]
#plabel_names = ["Sonne", "Mond","Blitz","Herz", "Blume","Wuerfel"]

plabels = ["\\text{\\SI}","\\leftmoon","\\text{\\blitze}","\\varheartsuit"]
plabel_names = ["Sonne", "Mond","Blitz","Herz"]

#clabels = ["\\text{\\Letter}","\\text{\\Rightscissors}","\\text{\\ding{46}}","\\star","\\text{\\bell}","\\text{\\clock}"]
#clabel_names = ["Brief","Schere", "Stifte","Sterne","Glocken","Uhren"]

clabels = ["\\text{\\Letter}","\\text{\\Rightscissors}"]
clabel_names = ["Brief","Schere"]


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

def make_tikzheader(color):
    return """\\begin{tikzpicture}[rounded corners,node distance = 3cm]

    \\tikzset{ctype/.style={circle,thick,minimum
      width=18mm},
      htype/.style={},
      ptype/.style={circle,draw=black!70,fill=%s!50,thick,minimum
      width=8mm},
      p4type/.style={circle,thick,minimum width=14mm},
      arrow/.style={-,very thick}}\n""" % color

def powerset(seq):
    if len(seq) > 0:
        head = powerset(seq[:-1])
        return head + [item + [seq[-1]] for item in head]
    else:
        return [[]]

def make_periphery(hidden=False, labeled = False, connections = [],plabels=[],color_list=[]):

    if labeled:
        directions = ["above left of = c0", "above right of = c0",\
                  "below right of = c0", "below left of = c0"]
    else:
        directions = ["above left of = c0", "above of = c0", "above right of = c0",\
                  "below right of = c0", "below of = c0", "below left of = c0"]

    periphery = "\\begin{pgfonlayer}{foreground}\n\n"

    if labeled:
        print color_list
        for i in range(4):
            periphery += "\\node [p4type, ,draw=black!70,fill=%s!50,%s]\
              (p%s)   {\\Huge{$%s$}};\n\n" % (color_list[i],directions[i],i,plabels[i])
    else:
        for i in range(6):
            periphery += "\\node [ptype, %s]  (p%s)   {};\n\n" % (directions[i],i)

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


# Generate Unlabelled

#for c,color in enumerate(colors):    
#    for j,clabel in enumerate(clabels):
#        out_string = file_header
#        pset6 = powerset(range(6))
#        pset3 = powerset(range(3))
#        for connections in pset6:
#            out_string += make_tikzheader(color) + tikzbackground + make_center(clabel)
#            out_string += make_periphery(hidden=False,connections=connections)
#            out_string += tikzbackground + tikzfooter
#        for connections in pset3:
#            out_string += make_tikzheader(color) + tikzbackground + make_center(clabel)
#            out_string += make_periphery(hidden=True,connections=connections)
#            out_string += tikzbackground + tikzfooter
#        out_string += file_footer
#        file_dir = os.path.join(os.path.dirname(__file__), 'Pics')
#        file_name = os.path.join(file_dir,"Unlabeled-"+clabel_names[j] + "-" +color_names[c])
#        f = open(file_name+'.tex','w')
#        f.write(out_string)
#        f.close()
#        os.chdir(file_dir)
#        call(["pdflatex", file_name+".tex"])
#        #call(["open", "-a", "Skim", file_name+".pdf"])

# Generate Labeled 

out_string = file_header
for color_permutation in itertools.permutations(colors):
    for j,clabel in enumerate(clabels):
        pset6 = powerset(range(4))
        pset3 = powerset(range(2))
        for connections in pset6:
            out_string += make_tikzheader("green") + tikzbackground + make_center(clabel)
            out_string += make_periphery(hidden=False,labeled=True,\
                                         connections=connections,plabels=plabels,color_list=color_permutation)
            out_string += tikzbackground + tikzfooter
        for connections in pset3:
            out_string += make_tikzheader("green") + tikzbackground + make_center(clabel)
            out_string += make_periphery(hidden=True,labeled=True,\
                                         connections=connections,plabels=plabels,color_list=color_permutation)
            out_string += tikzbackground + tikzfooter
        out_string += file_footer
        file_dir = os.path.join(os.path.dirname(__file__), 'Pics')
        file_name = os.path.join(file_dir,"Labeled-"+clabel_names[j] + "-" + str(color_permutation))
        f = open(file_name+'.tex','w')
        f.write(out_string)
        f.close()
        os.chdir(file_dir)
        call(["pdflatex", file_name+".tex"])
        #call(["open", "-a", "Skim", file_name+".pdf"])


