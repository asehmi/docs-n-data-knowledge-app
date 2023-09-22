# CONSTANTS --------------------------------------------------------------------

_BASE_DB_PATH = '.'
_DB_PATH = 'db'
_DB_NAME = 'gptdb.sqlite3'

DB_FILE = '{}/{}/{}'.format(_BASE_DB_PATH, _DB_PATH, _DB_NAME)
DB_TABLE = 'data'

# curl https://api.openai.com/v1/models -H "Content-Type: application/json" -H "Authorization: Bearer %OPENAI_API_KEY%"
OPENAI_MODELS_CHAT = ['gpt-3.5-turbo-16k', 'gpt-4']
# Was 'text-davinci-003' whihc is deprecated (see: https://platform.openai.com/docs/deprecations/)
OPENAI_MODELS_COMPLETIONS = ['gpt-3.5-turbo-instruct']

DEFAULT_MODEL_CONFIG = {
    'chat_model': OPENAI_MODELS_CHAT[1],
    'completions_model': OPENAI_MODELS_COMPLETIONS[0],
    'temperature': 0.1,
    'top_p': 0.9,
    'max_tokens': 2048,
}

LANG_MODEL_PRICING = {
    'gpt-3.5-turbo-16k': 0.003,     # per 1000 tokens
    'gpt-4': 0.03,                  # per 1000 tokens
    'gpt-3.5-turbo-instruct': 0.02, # per 1000 tokens
}

VECTOR_STORE = 'Weaviate' # 'Weaviate' | 'Local'

SAMPLE_QUESTIONS = [
    "None",
    "Summarize the most important concepts in a high performance software application",
    "Summarize the Wardley mapping technique",
    "Summarize the Viewpoints and Perspectives software solutions design methodology",
    "What are the most important considerations when architecting a software solution",
    "Build a 5-part learning plan on how to become a software architect. Detail each part with a short description and bullet points.",
    "Machine learning model training, deployment and operations",
    "What is a knowledge graph",
    "What is a graph neural network",
    "https://en.wikipedia.org/wiki/Graph_theory",
    "Most important factors of high performing teams",
]
