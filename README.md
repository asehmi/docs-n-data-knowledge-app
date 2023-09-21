
# LLM | DOC Q&A | KNOWLEDGE GRAPH | EXCEL DATA CHAT
> _Integrated LLM-based document and data Q&A with knowledge graph visualization_

> Arvindra Sehmi, A12i (CloudOpti Ltd.) | [LinkedIn](https://www.linkedin.com/in/asehmi/)

> Updated: 21 September, 2023

---

### Introduction

I'm writing some chapters for an upcoming book on Streamlit. So, I built this app to help me digest a large quantity of information from articles and documents I had on the subject of Software Architecture. I wanted to be able to ask questions about the documents and get answers, and also to be able to visualize the answers in a knowledge graph. I also wanted to be able to upload an Excel file and ask questions about the data in the file.

The application is a typical LLM application, with the addition of a knowledge graph visualization (implemented using Streamlit custom components). The application is built in Python using Streamlit and uses the Weaviate vector store for document and data indexing, and it uses the LangChain and Llama-Index LLM programming frameworks. The application supports local filestore indexding too. OpenAI embeddings are used and the OpenAI API is called for question answering (hence you will need an OpenAI API key to use the application). Various LLM models are used for the question answering, including the GPT-3.5 Turbo and GPT-4 models (both chat and completions variants). Token usage is tracked and costs are estimated.

The application is deployed on Streamlit Cloud. In the cloud, the application uses the Weaviate cloud-based vector store. Locally, the application uses a local filestore for indexing.

![snapshot](./images/snapshot-01.png)

### Streamlit App Demo

In this demo:

1. The user selects or enters a question query over documents or data which have been indexed into Weaviate (a cloud-based vector store) 
2. The app displays the question answer and generates a knowledge graph to complement the answer
3. The user can also upload an Excel file which can be displayed an queried using natural language
4. The app allows the user to enter their OpenAI API key and select the model(s) to use for the question answering
5. The app displays a per-query cost estimate and a running total of the cost of the queries

![st_demo](./images/app-demo.gif)

### Try the demo app yourself

The application can be seen running in the Streamlit Cloud at the link below:

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://asehmi-media-explorer-app-client-app-7vk2lf.streamlitapp.com/)

**NOTE:** You will need to enter your own OpenAI API. The key is ephemeral and not stored permanently in the application. Once entered, the API Key input box will be hidden and you can start using the app. To re-enter the API Key, a button is provided to clear the current key from memory, after which you can re-enter another key. 

### Installation

Ensure you have installed package requirements with the commands:

```bash
# change to the Streamlit <app root folder>, e.g.
cd ./docs-n-data-knowledge-app
pip install -r requirements.txt
```

**Important:** Modify the `secrets.toml` file in the application `.streamlit` root based on the example available in `secrets.toml.sample`.

```bash
IS_CLOUD_DEPLOYMENT='true' # 'true' = deployed on st cloud | 'false' = deployed locally
OPENAI_API_KEY='<Your OpenAI API Key>'
WEAVIATE_API_KEY='<Your Weaviate API Key>'
WEAVIATE_CLUSTER_URL='https://<Your Weaviate Cluster ID>.weaviate.network'
```

In `globals.py` you can change the following to affects the application behaviour:

```python
LANG_MODEL_PRICING = {
    'gpt-3.5-turbo-16k': 0.003,     # per 1000 tokens
    'gpt-4': 0.03,                  # per 1000 tokens
    'gpt-3.5-turbo-instruct': 0.02, # per 1000 tokens
}

VECTOR_STORE = 'Weaviate' # 'Weaviate' | 'Local'

# Sample questions for the Document Q&A functionality, based on the topic of _my_ indexed documents
SAMPLE_QUESTIONS = [
    "None",     # required
    "Summarize the most important concepts in a high performance software application",
    "Summarize the Wardley mapping technique",
    #  :
    # ETC.
    #  :
    "Most important factors of high performing teams",
]
```

Now run Streamlit with `app.py`:

```bash
# I prefer to set the port number too
streamlit run --server.port 4010 app.py
```

### TODO
- Need to have both completions and chat model selectors, indicating which model is for which purpose
- Possibly, remove the data page functionality from app and create a separate project for it
- Implement a file upload for the doc page and enable indexing of a local folder only if the app is run locally
- Add an is_local_deployment flag to the app secrets

### Resources
- https://weaviate.io/blog/llamaindex-and-weaviate
- https://weaviate.io/developers/weaviate
- https://console.weaviate.cloud/dashboard
- https://github.com/weaviate/recipes/tree/main
- https://github.com/weaviate/recipes/tree/main/integrations/llamaindex
- https://twitter.com/weaviate_io
- https://llmstack.ai/blog/retrieval-augmented-generation
- https://community.openai.com/t/how-to-accurately-price-a-gpt-4-chatbot/347250/23
- https://platform.openai.com/docs/deprecations/

---

If you enjoyed this app, please consider starring this repository.

Thanks!

Arvindra