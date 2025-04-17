import graphviz
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import json

def draw_nfa(nfa):
    dot = graphviz.Digraph(comment='NFA')

    # Add invisible starting state
    dot.node('startingStateH', 'startingStateH', style='invis')

    # Add nodes for NFA states
    for key in nfa.keys():
        if key == 'startingState':
            continue
        if nfa[key]['isTerminatingState']:
            dot.node(key, key, shape='doublecircle')  # Final state
        else:
            dot.node(key, key)

    # Add edges for NFA transitions
    for key in nfa.keys():
        if key == 'startingState':
            continue
        for symbol in nfa[key].keys():
            if symbol == 'isTerminatingState':
                continue
            for next_state in nfa[key][symbol]:
                sy = symbol
                if symbol == 'epsilon':
                    sy = 'ε'  # Display epsilon as ε
                dot.edge(key, next_state, label=sy)

    dot.edge('startingStateH', nfa['startingState'])
    return dot

def draw_dfa(dfa):
    dot = graphviz.Digraph(comment='DFA')

    # Add invisible starting state
    dot.node('startingStateH', 'startingStateH', style='invis')

    # Add nodes for DFA states
    for key in dfa.keys():
        if key == 'startingState':
            continue
        if dfa[key]['isTerminatingState']:
            dot.node(key, key, shape='doublecircle')  # Final state
        else:
            dot.node(key, key)

    # Add edges for DFA transitions
    for key in dfa.keys():
        if key == 'startingState':
            continue
        for symbol in dfa[key].keys():
            if symbol == 'isTerminatingState':
                continue
            next_state = dfa[key][symbol]   
            dot.edge(key, next_state, label=symbol)

    dot.edge('startingStateH', dfa['startingState'])
    return dot

def save_json(nfa, filename):
    # Serializing the NFA or DFA to a JSON file
    json_object = json.dumps(nfa, indent=4) 
    with open(filename, "w") as outfile:
        outfile.write(json_object)

def display_and_save_image(nfa, fileName):
    # Determine whether it's an NFA or DFA and render accordingly
    if fileName == 'nfa_graph':
        dot = draw_nfa(nfa)
    else:
        dot = draw_dfa(nfa)

    dot.format = 'png'
    dot.render(fileName)

    # Display the generated image
    img = mpimg.imread(fileName + '.png')
    imgplot = plt.imshow(img)
    plt.axis('off')
    plt.figure(figsize=(15, 15))
    plt.show()
