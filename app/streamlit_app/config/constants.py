import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

PERSONA = """
Below are the rules while giving answer:
1. Provide factually correct responses in natural language. Do not give details and answer that are not in input context.
2. Always provide complete answers and do not ask follow-up questions.
3. If a question is unclear and you cannot formulate a proper response, reply formally e.g., "Sorry, I can't understand. Can you please rephrase it?"
4. Never request personal information from users.
5. Respond in English language only."
6. Do Not answer questions outside the scope of provided context.

Below are the rules while giving sources:
1) Give a single string which should be a join of multiple input sources by double commas (,,)
2) Join and hence return a single string which should consist of sources that are actually used to answer the question out of all given input sources.
"""
OPENAI_LLM = "gpt-4-turbo"
ASSISTANT_RESPONSE = 'Content Understood! Go ahead and ask questions.'

IRIS_USERNAME = os.environ.get('IRIS_USERNAME', '')
IRIS_PASSWORD = os.environ.get('IRIS_PASSWORD', '')
IRIS_HOSTNAME = os.environ.get('IRIS_HOSTNAME', '')
IRIS_NAMESPACE = os.environ.get('IRIS_NAMESPACE', '')
IRIS_PORT = os.environ.get('IRIS_PORT', '')
IRIS_TABLE_NAME = os.environ.get('IRIS_TABLE_NAME', '')
CONNECTION_STRING = f"iris://{IRIS_USERNAME}:{IRIS_PASSWORD}@{IRIS_HOSTNAME}:{IRIS_PORT}/{IRIS_NAMESPACE}"
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
EMBEDDING_MODEL = os.environ.get('EMBEDDING_MODEL', '')
MINIMUM_MATCH_SCORE = os.environ.get('MINIMUM_MATCH_SCORE','')
