import streamlit as st

def main():
    c1, _, c3, _ = st.columns([2,0.25,1,1])
    with c1:
        with open('./README.md', 'r', encoding='utf-8') as f:
            readme_lines = f.readlines()
            readme_buffer = []
            for line in readme_lines:
                if '![snapshot](./images/snapshot-01.png)' in line:
                    st.markdown(' '.join(readme_buffer))
                    st.image('./images/snapshot-01.png')
                    readme_buffer.clear()
                elif '![st_demo](./images/app-demo.gif)' in line:
                    st.markdown(' '.join(readme_buffer))
                    st.image('./images/app-demo.gif')
                    readme_buffer.clear()
                else:
                    readme_buffer.append(line)
            st.markdown(' '.join(readme_buffer), unsafe_allow_html=True)

    with c3:
        st.markdown('''
            ### About 🎈Streamlit

            Streamlit is a Python library that allows the creation of interactive, data-driven web applications in Python.
            [Streamlit](https://streamlit.io) is an open-source app framework for Machine Learning and Data Science teams. 
            You can create beautiful data apps in minutes, not weeks. All in pure Python. It's not just for Data Science, though.

            With its component extensibility architecture, you can build and integrate most kinds of web frontends into Streamlit apps. 
            
            Streamlit is fast-becoming a de facto standard for building Generative AI and LLM apps in Python.
                         
            ##### Resources

            - [Build powerful generative AI apps with Streamlit](https://streamlit.io/generative-ai)
            - [Streamlit Documentation](https://docs.streamlit.io/)
            - [Streamlit Blog](https://blog.streamlit.io/)
            - [Cheat sheet](https://docs.streamlit.io/library/cheatsheet)
            - [Book](https://www.amazon.com/dp/180056550X) (Getting Started with Streamlit for Data Science)
            - [Blog](https://blog.streamlit.io/how-to-master-streamlit-for-data-science/) (How to master Streamlit for data science)

            ##### Deploy

            Once you've created an app you can use the [Community Cloud](https://streamlit.io/cloud) to deploy, manage, and share your app, in just a few clicks. ''')
