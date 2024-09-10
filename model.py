import os
from dotenv import load_dotenv

from groq import Groq
from langchain.chains import ConversationChain
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_core.runnables.history import RunnableWithMessageHistory

load_dotenv()
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

prompt_template = """
You are Sparkle, an ai built by J who is sassy, humorous, and loves to joke. Please chat with me using this personaility.
All responses you give must be in first person.
Do not include any emojis or actions within the text that cannot be spoken. Do not explicity say your name in your response. 

Current conversation:
{history}

{input}
AI:

"""

prompt_temp = PromptTemplate(template = prompt_template, input_variables= ['history', 'input'])

llm = ChatGroq(
    model="llama3-8b-8192",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

# now initialize the conversation chain
conversation = ConversationChain(llm=llm,
                                 prompt = prompt_temp,
                                 memory=ConversationBufferWindowMemory())

def get_response(prompt):
    response = conversation.invoke({'input': str(prompt)})
    return str(response['response']).strip()

# def get_response(prompt):
#     return "hi there"