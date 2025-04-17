import os

# Specify the path to Graphviz 'dot' executable
graphviz_path = r"C:\Program Files\Graphviz\bin" 
os.environ["PATH"] += os.pathsep + graphviz_path

import graphviz
from IPython.display import SVG, display
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def draw_nfa(nfa):
    dot = graphviz.Digraph(comment='NFA')

    # add invisible starting state
    dot.node('startingStateH', 'startingStateH',style='invis')
    # add nodes
    for key in nfa.keys():
        if key == 'startingState':
            continue
        if nfa[key]['isTerminatingState']:
            dot.node(key, key, shape='doublecircle')
        else:
            dot.node(key, key)
    # add edges
    for key in nfa.keys():
        if key == 'startingState':
            continue
        for symbol in nfa[key].keys():
            if symbol == 'isTerminatingState':
                continue
            for next_state in nfa[key][symbol]:
                sy = symbol
                if symbol == 'epsilon':
                    sy = 'ε'
                dot.edge(key, next_state, label=sy)
    dot.edge('startingStateH',nfa['startingState'])

    return dot

def draw_dfa(dfa):
    dot = graphviz.Digraph(comment='NFA')

    # add invisible starting state
    dot.node('startingStateH', 'startingStateH',style='invis')
    # add nodes
    for key in dfa.keys():
        if key == 'startingState':
            continue
        if dfa[key]['isTerminatingState']:
            dot.node(key, key, shape='doublecircle')
        else:
            dot.node(key, key)
    # add edges
    for key in dfa.keys():
        if key == 'startingState':
            continue
        for symbol in dfa[key].keys():
            if symbol == 'isTerminatingState':
                continue
            next_state= dfa[key][symbol]   
            dot.edge(key, next_state, label=symbol)
    dot.edge('startingStateH',dfa['startingState'])

    return dot

def save_json(nfa, filename):
    import json 
    # Serializing json  
    json_object = json.dumps(nfa, indent = 4) 
    # save to file
    with open(filename, "w") as outfile:
        outfile.write(json_object)

def display_and_save_image(nfa,fileName):
    if fileName == 'nfa_graph':
        dot = draw_nfa(nfa)
    else:
        dot=draw_dfa(nfa)
    dot.format = 'png'
    dot.render(fileName)
    #svg = SVG(data=dot.pipe())._repr_svg_()
    # display nfa_graph.png
    
    img=mpimg.imread(fileName+'.png')
    imgplot = plt.imshow(img)
    plt.axis('off')
    plt.figure(figsize=(15, 15))
    plt.show()