import streamlit as st
from regex_lexer import Tokenizer
from regex_parser import RegexParser
from regex_ast import debug_ast_structure
from nfa_builder import ThompsonBuilder
from dfa_converter import NFAtoDFA
from dfa_minimizer import DFAReducer
from automata_visualizer import save_to_json, render_automata_image

import re

def validate_regex(expression):
    try:
        re.compile(expression)
        return True
    except re.error:
        return False

def process_regex_pipeline(expression):
    if not validate_regex(expression):
        st.error("Invalid regular expression format.")
        return

    st.write("🔁 Converting Regex to NFA")
    tokenizer = Tokenizer(expression)
    token_stream = tokenizer.tokenize()

    parser = RegexParser(token_stream)
    try:
        ast_tree = parser.parse()
    except Exception as err:
        st.error(f"Parsing Error: {err}")
        return

    st.write("📐 AST Structure:")
    debug_ast_structure(ast_tree)

    nfa_graph = ThompsonBuilder(ast_tree).construct_nfa()
    nfa_dict = nfa_graph.to_dict()
    save_to_json(nfa_dict, "output_nfa.json")
    render_automata_image(nfa_dict, "nfa_diagram", is_nfa=True)

    st.write("⚙️ Translating NFA to DFA")
    dfa = NFAtoDFA(nfa_dict).convert_to_dfa()
    dfa_dict = dfa.to_serialized_dict()
    save_to_json(dfa_dict, "output_dfa.json")
    render_automata_image(dfa_dict, "dfa_diagram", is_nfa=False)

    st.write("🧹 Minimizing DFA")
    minimized = DFAReducer(dfa_dict).to_dict()
    save_to_json(minimized, "output_min_dfa.json")
    render_automata_image(minimized, "min_dfa_diagram", is_nfa=False)

# ─────────────────────────────────────
# STREAMLIT UI
# ─────────────────────────────────────
st.title("Regex to NFA, DFA, and Minimized DFA 🔍")
user_input = st.text_input("Enter your regular expression below:")

if st.button("Visualize Automata"):
    if user_input:
        process_regex_pipeline(user_input)
    else:
        st.warning("Please enter a regex to begin.")
