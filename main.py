import re
import streamlit as st

# Import your own modules
from lexer import *
from AST import *
from parser import *
from NFA import *
from DFA import *
from minimizedDFA import *
from visualize import *

def is_valid_regex(regex):
    try:
        re.compile(regex)
        return True
    except re.error:
        return False
    
def req1(regex):
    print('Req 1 : regex to NFA')
    regexlexer = regexLexer(regex)
    tokenStream = regexlexer.lexer()
   
    parseRegex = ParseRegex(tokenStream)
    ## handle Exception
    throwException = False
    try:
        AST = parseRegex.parse()
    except Exception as e:
        print(e)
        throwException = True
    if throwException:
        print('Invalid regex')
        return
    print_ast(AST)
    nfa = ThompsonConstruction(AST).construct().to_dict()
    save_json(nfa, "nfa.json")
    print('NFA for regex: ', regex)
    display_and_save_image(nfa,"nfa_graph")

def req2(regex):
    print('Req 2 : NFA to minimized DFA')
    regexlexer = regexLexer(regex)
    tokenStream = regexlexer.lexer()
    print('AST for regex: ', regex)
    parseRegex = ParseRegex(tokenStream)
    ## handle Exception
    throwException = False
    try:
        AST = parseRegex.parse()
    except Exception as e:
        print(e)
        throwException = True
    if throwException:
        print('Invalid regex')

    nfa = ThompsonConstruction(AST).construct().to_dict()
    converter = NFAtoDFAConverter(nfa)
    dfa = converter.convert().to_dict()
    save_json(dfa, "dfa.json")
    display_and_save_image(dfa,"dfa_graph")

    minimizer = DFAMinimizer(dfa).to_dict()
    save_json(minimizer, "minimized_dfa.json")
    display_and_save_image(minimizer,"minimized_dfa_graph")
    
    return AST

def visualize_regex(regex):
    
    req1(regex)
    req2(regex)
    
def plot_image(file_name):
    try:
        img = mpimg.imread(file_name + '.png')
        fig = plt.figure(figsize=(10, 10))
        plt.imshow(img)
        plt.axis('off')
        st.pyplot(fig)
    except FileNotFoundError:
        st.error(f"Image file '{file_name}.png' not found. Make sure the graph was rendered and saved correctly.")
        
# ---------------------------
# Streamlit UI
# ---------------------------
st.title("Regex to Minimized DFA Visualizer")

regex = st.text_input("Enter a regular expression:", "ab(b|c)*d+")

if st.button("Generate DFA"):
    if not is_valid_regex(regex):
        st.error("Invalid regular expression.")
    else:
        visualize_regex(regex)

        st.subheader("NFA Graph")
        plot_image('nfa_graph')

        st.subheader("DFA Graph")
        plot_image('dfa_graph')

        st.subheader("Minimized DFA Graph")
        plot_image('minimized_dfa_graph')

