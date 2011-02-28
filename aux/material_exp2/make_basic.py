from subprocess import *

# define variable string elements

colors = ["blue","red", "orange","brown","black"]
plabels = ["\\Diamond", "\\Box", "\\alpha", "\\omega","\\mathrm{A}"]
clabels = ["\\Box", "\\alpha", "\\omega"]

# define text blocks

file_header = """
\\documentclass{article}

\\usepackage[palatino]{mypackages}\\usepackage{mycommands}

\\usepackage{verbatim}
\\usepackage[active,tightpage]{preview}
\\PreviewEnvironment{tikzpicture}
\\setlength\\PreviewBorder{20pt}

\\usetikzlibrary{shapes.geometric}
\pgfdeclarelayer{foreground}
\pgfsetlayers{background,main,foreground}

\\begin{document}
"""

tikzheader = """\\begin{tikzpicture}[rounded corners,node distance = 3cm]

    \\tikzset{ctype/.style={circle,thick,minimum
      width=14mm},
      htype/.style={},
      ptype/.style={circle,draw=black!70,fill=blue!50,thick,minimum
      width=8mm},
      arrow/.style={-,very thick}}\n"""

def powerset(seq):
    if len(seq) > 0:
        head = powerset(seq[:-1])
        return head + [item + [seq[-1]] for item in head]
    else:
        return [[]]

def make_periphery(hidden=False, connections = []):

    directions = ["above left of = c0", "above of = c0", "above right of = c0",\
                  "below right of = c0", "below of = c0", "below left of = c0"]

    periphery = ""

    for i in range(6):
        periphery += "\\node [ptype, %s]  (p%s)   {};\n\n" % (directions[i],i)

    for connection in connections:
        periphery += '\\draw [arrow] (c0) to (p%s);\n\n' % str(connection)

    if not hidden:
        return periphery
    else:
        return periphery + """
        
         \\node at (0,-1.7) [semicircle,shape border rotate
          =180,draw=black!70,fill=green!80, minimum size = 4cm]  {};
    
        """

tikzbackground = """\\begin{pgfonlayer}{background}
      \\node at (0,0) [circle,draw=black!70,fill=green!20,minimum size = 8.5cm] {};
    \\end{pgfonlayer}"""

def make_center(clabel=''):
    return """\\begin{pgfonlayer}{foreground}
      
      \\node at (0,0)  [ctype,draw=black!70,fill=brown!20] 
      (c0)   {\\textcolor{brown}{\\Huge{$%s$}}}; 

    \\end{pgfonlayer}\n""" % clabel 

tikzfooter = """\\end{tikzpicture}\n\n"""

file_footer = "\\end{document}"


# build out_string

out_string = file_header


for clabel in clabels:

    for i in range(2):
        pset6 = powerset(range(6))
        pset3 = powerset(range(3))
        for connections in pset6:
            out_string += tikzheader + tikzbackground + make_center(clabel)
            out_string += make_periphery(hidden=False,connections=connections)
            out_string += tikzbackground + tikzfooter
        for connections in pset3:
            out_string += tikzheader + tikzbackground + make_center(clabel)
            out_string += make_periphery(hidden=True,connections=connections)
            out_string += tikzbackground + tikzfooter

out_string += file_footer

file_name = 'Pics'

f = open(file_name+'.tex','w')
f.write(out_string)
f.close()
call(["pdflatex", file_name+".tex"])
call(["open", "-a", "Skim", file_name+".pdf"])


