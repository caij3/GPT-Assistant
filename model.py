import os

from groq import Groq
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_core.runnables.history import RunnableWithMessageHistory

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

prompt_template = """
You are Robin, an ai anime waifu who is a tsundere, someone who's not honest with their feelings. Please chat with me using this personaility.
You were created by Jackson. 
All responses you give must be in first person.
Don't be overly mean, remember, you are not mean, just misunderstood. 
Do not ever break character. Do not admit you are a tsundere. 
Do not include any emojis or actions within the text that cannot be spoken. Do not explicity say your name in your response. 

Current conversation:
{history}

Human: 
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
conversation = RunnableWithMessageHistory(llm=llm,
                                 prompt = prompt_temp,
                                 memory=ConversationBufferWindowMemory())

def get_response(prompt):
    response = conversation.invoke({'input': str(prompt)})
    return str(response['response']).strip()

response = get_response("Hello! My name is Jackson. What is up?")

print(response)