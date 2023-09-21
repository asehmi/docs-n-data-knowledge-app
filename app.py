import os
import logging
import streamlit as st

import streamlit_debug
streamlit_debug.set(flag=True, wait_for_client=False, host='localhost', port=7777)

st.set_page_config(page_title='ChatGPT Pandas CSV Streamlit App', page_icon='🤖', initial_sidebar_state='expanded', layout='wide')

from app_state import (state, init_app_state, reset_app_state, _set_state_cb)
init_app_state() # ensure all state variables are initialized

import app_llm_data_query, app_llm_docs_query, app_llm_knowlege_graph_gen

from globals import SAMPLE_QUESTIONS

logging.basicConfig(level=logging.INFO)

# APP CALLBACKS -----------------------------------------------------------------

def _set_openai_api_key_cb():
    if not state.text_input_openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
        return
    state.openai_api_key = state.text_input_openai_api_key
    os.environ['OPENAI_API_KEY'] = state.openai_api_key

def _clear_openai_api_key_cb():
    state.openai_api_key = ''
    os.environ['OPENAI_API_KEY'] = state.openai_api_key

# DATA CHAT PAGE ----------------------------------------------------------------

def _openai_api_key_guard():
    # Guardrail for API Key
    if not state.openai_api_key:
        st.error('🔑 Please enter your OpenAI API Key in the settings sidebar. 🔑')
        st.info(
            'This value is ephemeral and not stored permanently.\n\n'
            'Once entered, the API Key input box will be removed, and you can start using the app.\n\n'
            'To re-enter the API Key, click the global settings button to clear the current key from memory.'
        )
        with st.sidebar:
            # api key
            st.text_input(
                '🔑 OpenAI API Key', 
                value=state.openai_api_key,
                placeholder='sk-...',
                type='password',
                on_change=_set_openai_api_key_cb,
                help='Enter your OpenAI API Key',
                key='text_input_openai_api_key'
            )
            st.stop()

def start():

    # Guardrail for API Key
    _openai_api_key_guard()

    # Sidebar
    with st.sidebar:
        st.image('./images/a12i_logo_circle_transparent.png')
        top_level_options = ['Document Q&A | Knowedge Graph', 'Data Chat']
        st.subheader('What would you like to do?')
        top_level = st.radio(
            'What would you like to do?', 
            top_level_options, index=0,
            label_visibility='collapsed', horizontal=False
        )
        
    # Document Q&A | Knowledge Graph
    if top_level == top_level_options[0]:
        c1, _ = st.columns([1, 1.5])
        with c1:
            # Title and description
            st.subheader(f'Document Q&A ❣️ Knowledge Graph')
            st.caption(
                '📑 Ask a question based on pre-uploaded documents on the subject of **Software Architecture**. You can ask questions on any topic '
                'in as much detail as you like. For your convenience, some sample questions are provided below.'
            )
        c1, _, c3, _ = st.columns([1, 0.075, 1, 1.5])
        with c1:
            st.markdown('### **1️⃣ Ask a question**')
            user_input = st.text_input(
                "Enter question here...",
                placeholder="Enter text 🖋️ or URL 🔗",
                label_visibility="collapsed",
                key="user_text_input"
            )
            example_selection = st.selectbox(
                "📑 You can choose a sample question here instead",
                options=SAMPLE_QUESTIONS,
                index=0,
                key="examples_selectbox"
            )

        with c3:
            user_input_confirmed = False
            radio_options = [user_input, example_selection] if user_input and (user_input != example_selection) else ([example_selection] if example_selection != "None" else [])
            if radio_options:
                st.markdown('### **2️⃣ Confirm your question**')
                with st.form(key="confirm_input_form"):
                    st.radio(
                        "Confirm input", options=radio_options,
                        on_change=_set_state_cb(user_input="confirm_input"),
                        label_visibility="collapsed",
                        horizontal=True,
                        key="confirm_input"
                    )
                    user_input_confirmed = st.form_submit_button(
                        label="Confirm", type='primary',
                        on_click=_set_state_cb(
                            estimated_cost_doc='estimated_cost_reset',
                            estimated_cost_graph='estimated_cost_reset',
                        )
                    )

        if state.user_input:
            st.markdown(f'###### ✅ Confirmed question: _{state.user_input}_')
        else:
            st.markdown('###### ❌ No question confirmed yet')
        
        st.markdown('---')

        c1, _, c3 = st.columns([1, 0.075, 1])
        with c1:
            response = app_llm_docs_query.main('Document Q&A', user_input_confirmed)
        with c3:
            app_llm_knowlege_graph_gen.main('Knowledge Graph', user_input_confirmed, response)

    # Simple Excel Data Q&A
    if top_level == top_level_options[1]:
        c1, _ = st.columns([1, 2])
        with c1:
            st.subheader(f'🔢 Simple Excel Data Q&A')
            app_llm_data_query.main('Data Chat')

    with st.sidebar:
        st.markdown('---')

        with st.expander('#### Cost Estimation', expanded=True):
            st.markdown(f'**Cumulative: ${state.cumulative_cost:.2f}**')
            st.markdown(f'Data query: ${state.estimated_cost_data:.2f}')
            st.markdown(f'Doc query: ${state.estimated_cost_doc:.2f}')
            st.markdown(f'Graph query: ${state.estimated_cost_graph:.2f}')

        st.markdown('#### Global Settings')
        if st.button('Reset app state', type='primary', help='Clear results cache and app state (optional). Will clear cost estimations too!'):
            reset_app_state()
            app_llm_data_query.get_llm_data_query_response.clear()
            app_llm_docs_query.get_llm_doc_query_response.clear()
            app_llm_knowlege_graph_gen.get_llm_graph_data_response.clear()
            st.experimental_rerun()
        st.button('Clear OpenAI API key', on_click=_clear_openai_api_key_cb, type='primary', help='Clear OpenAI API key (optional)')

        with st.expander('Debug State (excluding private keys)', expanded=False):
            display_state = {k: v for k, v in state.items() if not ('openai' in k or 'weaviate' in k)}
            st.write(display_state)

if __name__ == '__main__':
    start()
