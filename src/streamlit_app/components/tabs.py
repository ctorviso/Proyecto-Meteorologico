import streamlit as st
from helpers.lookups import elements

tabs = [element.capitalize() for element in elements]

if "selected_element" not in st.session_state:
    st.session_state.selected_element = tabs[0].lower()

def element_tabs():
    cols = st.columns(len(tabs))

    if "selected_element" not in st.session_state:
        selected_element = tabs[0].lower()
    else:
        selected_element = st.session_state.selected_element

    for i, tab in enumerate(cols):
        def click_tab(tab_name=tabs[i]):
            st.session_state.selected_element = tab_name.lower()

        if tabs[i].lower() == selected_element:
            tab.button(tabs[i], key=f"tab_{i}", on_click=click_tab, use_container_width=True, disabled=True)
        else:
            tab.button(tabs[i], key=f"tab_{i}", on_click=click_tab, use_container_width=True)

    st.session_state.selected_element = selected_element

    return selected_element