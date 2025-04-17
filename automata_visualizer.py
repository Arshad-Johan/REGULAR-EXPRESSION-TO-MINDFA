import graphviz
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import json

def generate_nfa_diagram(nfa_data):
    dot = graphviz.Digraph(comment="NFA Representation")
    dot.node('entryHidden', '', style='invis')

    for state in nfa_data:
        if state == 'startingState':
            continue
        shape = 'doublecircle' if nfa_data[state].get('isTerminatingState', False) else 'circle'
        dot.node(state, state, shape=shape)

    for state in nfa_data:
        if state == 'startingState':
            continue
        for symbol, targets in nfa_data[state].items():
            if symbol == 'isTerminatingState':
                continue
            label = 'ε' if symbol == 'epsilon' else symbol
            for destination in targets:
                dot.edge(state, destination, label=label)

    dot.edge('entryHidden', nfa_data['startingState'])
    return dot

def generate_dfa_diagram(dfa_data):
    dot = graphviz.Digraph(comment="DFA Representation")
    dot.node('entryHidden', '', style='invis')

    for state in dfa_data:
        if state == 'startingState':
            continue
        shape = 'doublecircle' if dfa_data[state].get('isTerminatingState', False) else 'circle'
        dot.node(state, state, shape=shape)

    for state in dfa_data:
        if state == 'startingState':
            continue
        for symbol, target in dfa_data[state].items():
            if symbol == 'isTerminatingState':
                continue
            dot.edge(state, target, label=symbol)

    dot.edge('entryHidden', dfa_data['startingState'])
    return dot

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

from PIL import Image
import streamlit as st

def render_automata_image(automaton_data, base_filename, is_nfa=True):
    diagram = generate_nfa_diagram(automaton_data) if is_nfa else generate_dfa_diagram(automaton_data)
    diagram.format = 'png'
    filepath = diagram.render(base_filename)

    # Load and render image with controlled width
    img = Image.open(filepath)
    st.image(img, caption=base_filename.replace("_", " ").title(), width=200)  # You can adjust width as needed
