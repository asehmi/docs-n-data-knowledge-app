# CONSTANTS --------------------------------------------------------------------

_BASE_DB_PATH = '.'
_DB_PATH = 'db'
_DB_NAME = 'gptdb.sqlite3'

DB_FILE = '{}/{}/{}'.format(_BASE_DB_PATH, _DB_PATH, _DB_NAME)
DB_TABLE = 'data'

# curl https://api.openai.com/v1/models -H "Content-Type: application/json" -H "Authorization: Bearer %OPENAI_API_KEY%"
# Actual model names used in app for selectors
OPENAI_MODELS_CHAT = ['gpt-4-1106-preview', 'gpt-4']
OPENAI_MODELS_COMPLETIONS = ['gpt-3.5-turbo-instruct']

DEFAULT_MODEL_CONFIG = {
    'chat_model': OPENAI_MODELS_CHAT[0],
    'completions_model': OPENAI_MODELS_COMPLETIONS[0],
    'temperature': 0.1,
    'top_p': 0.9,
    'max_tokens': 2048,
}

# Mapping from friendly name to actual model name
LANG_MODELS = {
    # Friendly aliases used in app
    'gpt-4': 'gpt-4',
    'gpt-4-turbo': 'gpt-4-1106-preview',
    # Actual model names used in app
    'gpt-4-1106-preview': 'gpt-4-1106-preview',
    'gpt-3.5-turbo-instruct': 'gpt-3.5-turbo-instruct',
}

# See: https://openai.com/pricing
LANG_MODEL_PRICING = {
    # Friendly aliases used in app
    'gpt-4': {'input': 0.03, 'output': 0.06},                       # per 1000 tokens
    'gpt-4-turbo': {'input': 0.01, 'output': 0.03},                 # per 1000 tokens
    # Actual model names used in app
    'gpt-4-1106-preview': {'input': 0.01, 'output': 0.03},          # per 1000 tokens
    'gpt-3.5-turbo-instruct': {'input': 0.0015, 'output': 0.002},   # per 1000 tokens
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
