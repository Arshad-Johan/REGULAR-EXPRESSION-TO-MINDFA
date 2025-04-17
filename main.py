import streamlit as st
from lexer import *
from parser import *
from AST import *
from NFA import *
from visualize import *
from DFA import *
from minizedDFA import *

import re

def is_valid_regex(regex):
    try:
        re.compile(regex)
        return True
    except re.error:
        return False

def regex_to_minimized_dfa(regex):
    
    # Step 1: Validate the regex
    if not is_valid_regex(regex):
        st.error("Invalid regex")
        return
    
    # Step 2: Process the regex to generate NFA, DFA, and Minimized DFA
    st.write('Req 1: regex to NFA')
    regexlexer = regexLexer(regex)
    tokenStream = regexlexer.lexer()
    st.write(f'AST for regex: {regex}')
    parseRegex = ParseRegex(tokenStream)
    
    try:
        AST = parseRegex.parse()
    except Exception as e:
        st.error(f"Error in parsing regex: {e}")
        return
    
    st.write("AST:")
    print_ast(AST)
    
    # Convert the AST to NFA
    nfa = ThompsonConstruction(AST).construct().to_dict()
    save_json(nfa, "nfa.json")
    st.write("NFA for regex:")
    display_and_save_image(nfa, "nfa_graph")
    
    # Step 3: Convert NFA to DFA
    st.write('Req 2: NFA to minimized DFA')
    converter = NFAtoDFAConverter(nfa)
    dfa = converter.convert().to_dict()
    save_json(dfa, "dfa.json")
    st.write("DFA for regex:")
    display_and_save_image(dfa, "dfa_graph")
    
    # Step 4: Minimize the DFA
    minimizer = DFAMinimizer(dfa).to_dict()
    save_json(minimizer, "minimized_dfa.json")
    st.write("Minimized DFA for regex:")
    display_and_save_image(minimizer, "minimized_dfa_graph")

# Streamlit app UI
st.title('Regex to NFA, DFA, and Minimized DFA Visualization')

# Step 1: Input field for regex
regex_input = st.text_input("Enter a regex:")

# Step 2: Button to trigger processing
if st.button('Generate NFA, DFA, and Minimized DFA'):
    if regex_input:
        regex_to_minimized_dfa(regex_input)
    else:
        st.error("Please enter a valid regex.")
