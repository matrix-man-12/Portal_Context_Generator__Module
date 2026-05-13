import streamlit as st

st.title("Test Chat Input")
res = st.chat_input("Upload", accept_file="multiple")
if res:
    st.write(type(res))
    if hasattr(res, "text"):
        st.write("Text:", res.text)
    if hasattr(res, "files"):
        st.write("Files:", [f.name for f in res.files])
