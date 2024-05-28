import streamlit as st
from streamlit_app.ui_elements.sidebar import sidebar
from streamlit_app.ui_elements.show_references import show_references
from streamlit_app.core.qa import get_answer
from streamlit_app.core.caching import bootstrap_caching
from streamlit_app.ui_elements.suggested_prompts import suggested_prompts, selected_persona


st.set_page_config(page_title="Vector Search", page_icon="🔮", layout="wide")
cols = st.columns([6, 6])
cols[0].markdown(
    """
    <h1 style='font-size: 3em; font-family: Arial, sans-serif; color: #ffffff;'>
        Vector Search
    </h1>
    """,
    unsafe_allow_html=True,
)
cols[1].image("./streamlit_app/media/img_2.png", width=400)

# Enable caching for expensive functions
# bootstrap_caching()

sidebar()

# Example prompts and help texts

# Initialize button_pressed variable
button_pressed = ""
# Create a grid of buttons
st.divider()
st.write("##### Example Prompts to start with")

# Create a single row with evenly spaced columns
cols = st.columns(len(suggested_prompts.get(st.session_state.mode)))
for i, prompt in enumerate(suggested_prompts.get(st.session_state.mode)):
    if cols[i].button(prompt):
        button_pressed = prompt

# Handle user input
if prompt := (st.chat_input("What are you looking for?") or button_pressed):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Create an assistant message container and a placeholder for the response
    with st.chat_message("assistant"):
        assistant_response = st.empty()
        
        with st.spinner("Analysing..."):
            result = get_answer(query=prompt, custom_persona=selected_persona.get(st.session_state.mode))
        
        # Update the assistant's message with the actual response
        assistant_response.markdown(result.answer)
        show_references(result.sources)
