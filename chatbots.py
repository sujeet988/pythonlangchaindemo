import os
from dotenv import load_dotenv
load_dotenv() # Load environment variables from a .env file
groq_api_key = os.getenv("GROQ_API_KEY")
print(groq_api_key)

from langchain_groq import ChatGroq

model = ChatGroq(model="llama-3.1-8b-instant",groq_api_key=groq_api_key)
print(model)
## langhain core using 
from langchain_core.messages import HumanMessage
result =model.invoke([HumanMessage(content="Hi , My name is sujet and I am a Chief AI Engineer")])
#print(result)

## mix message for human and ai for maintain the context
from langchain_core.messages import AIMessage
response = model.invoke(
    [
        HumanMessage(content="Hi , My name is sujet and I am a Chief AI Engineer"),
        AIMessage(content="Nice to meet you, Sujet. As a Chief AI Engineer, you're likely at the forefront of developing and implementing cutting-edge AI solutions. What brings you here today? Are you working on a specific project, exploring new AI technologies, or perhaps looking for insights on the latest AI trends? I'm all ears (or rather, all text)."),
        HumanMessage(content="Hey What's my name and what do I do?")
    ]
)
##print("mix message response")   
##print(response)

## message History
#pip install langchain_community
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

store ={} # In-memory dictionary store for chat histories 
def get_session_history(session_id:str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

with_message_history = RunnableWithMessageHistory(model,get_session_history)
## creating config for login session
config ={"configurable":{"session_id":"user_1234"}}

response=with_message_history.invoke(
    [HumanMessage(content="Hi , My name is sujeet and I am a Chief AI Engineer")],
    config=config
)
#print("message history response: " + response.content)

## same session id appending or ask another so they can give response from context
result = with_message_history.invoke(
    [HumanMessage(content="What's my name?")],
    config=config,
)
#print("same session id response: " + result.content)

## change the config-->session id
config1={"configurable":{"session_id":"user_2"}}

response=with_message_history.invoke(
    [HumanMessage(content="Whats my name")],
    config=config1
)
#print(response.content) ## it will not remember the context as session id is different

response=with_message_history.invoke(
    [HumanMessage(content="Hey My name is John")],
    config=config1
)
#print(response.content) ## it will not remember the context as session id is different
response=with_message_history.invoke(
    [HumanMessage(content="Whats my name")],
    config=config1
)
#print(response.content) ## now it will remember the context as session id is same as previous one
print("---------------------------------prompt templates------------------")

## Prompt templates 

from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant.Amnswer all the question to the nest of your ability"),
        MessagesPlaceholder(variable_name="messages")

    ]
)
chain = prompt|model
response =chain.invoke({"messages": [HumanMessage(content="my name is sujeet kumar")]})
#print( response)

with_message_history = RunnableWithMessageHistory(chain,get_session_history)

config = {"configurable": {"session_id": "chat3"}}
response=with_message_history.invoke(
    [HumanMessage(content="Hi My name is Krish")],
    config=config
)

#print(response)

response = with_message_history.invoke(
    [HumanMessage(content="What's my name?")],
    config=config,
)

#print(response.content)

## Add more complexity
prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Answer all questions to the best of your ability in {language}."
        ),
        MessagesPlaceholder(variable_name="messages")
    ]
)
chain = prompt | model
response = chain.invoke({"messages": [HumanMessage(content="My name is sujeet")], "language": "Hindi"})
#print(response.content)

# more complexity with history
with_message_history=RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="messages"
)
config = {"configurable": {"session_id": "chat4"}}
repsonse=with_message_history.invoke(
    {'messages': [HumanMessage(content="Hi,I am Krish")],"language":"Hindi"},
    config=config
)
#print(repsonse.content)

response = with_message_history.invoke(
    {"messages": [HumanMessage(content="whats my name?")], "language": "Hindi"},
    config=config,
)
#print(response.content)
# Managing the conversion history
print("-----------------trim messages-------------------")
from langchain_core.messages import SystemMessage,trim_messages

def token_counter(messages):
    # safe fallback, no transformers
    return sum(len(m.content.split()) for m in messages)
trimmer = trim_messages(
    max_tokens=45,
    strategy="last",
    token_counter = model,
    include_system=True,
    allow_partial=False,
    start_on="human"
)
messages = [
    SystemMessage(content="you're a good assistant"),
    HumanMessage(content="hi! I'm bob"),
    AIMessage(content="hi!"),
    HumanMessage(content="I like vanilla ice cream"),
    AIMessage(content="nice"),
    HumanMessage(content="whats 2 + 2"),
    AIMessage(content="4"),
    HumanMessage(content="thanks"),
    AIMessage(content="no problem!"),
    HumanMessage(content="having fun?"),
    AIMessage(content="yes!"),
]
response = trimmer.invoke(messages)
#print(response)
from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough

chain = (
    RunnablePassthrough.assign(messages=itemgetter("messages")|trimmer)
    |prompt
    |model
)
response=chain.invoke(
    {
    "messages":messages + [HumanMessage(content="What ice cream do i like")],
    "language":"English"
    }
)
response.content
#print(response.content)

response = chain.invoke(
    {
        "messages": messages + [HumanMessage(content="what math problem did i ask")],
        "language": "English",
    }
)
##print(response.content)

## Lets wrap this in the MEssage History
with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="messages",
)
config={"configurable":{"session_id":"chat5"}}

response = with_message_history.invoke(
    {
        "messages": messages + [HumanMessage(content="whats my name?")],
        "language": "English",
    },
    config=config,
)

##print(response.content)  ## I don't think you mentioned your name earlier. You're a new conversation partner. How about we start fresh? What's your name?

response = with_message_history.invoke(
    {
        "messages": [HumanMessage(content="what math problem did i ask?")],
        "language": "English",
    },
    config=config,
)

print(response.content) ## You didn't ask a math problem. Our conversation just started, and you asked about your name.