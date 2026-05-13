import streamlit as st
import inspect
sig = inspect.signature(st.chat_input)
print("accept_file in sig:", "accept_file" in sig.parameters)
print("Signature:", sig)
