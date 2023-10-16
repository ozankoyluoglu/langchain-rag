import streamlit as st
import faiss
import pickle
from langchain import OpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import RetrievalQAWithSourcesChain



# load document index
index = faiss.read_index("docs.index")
with open("faiss_index.pkl", "rb") as file:
    store = pickle.load(file)
store.index = index

# llm using temperature 0 to minimize generative nature
llm=OpenAI(temperature=0)

# memory of conversation
memory = ConversationBufferMemory(
    #llm=llm, 
    output_key='answer',
    input_key='question', 
    human_prefix="User",
    ai_prefix="AI",
    memory_key='chat_history'
    )

with open("template_combine_prompt.txt", "rb") as file:
    combine_prompt_template=file.read()

# template for final combine prompt in RetrievalQAWithSourcesChain
combine_prompt = PromptTemplate(
    input_variables=['summaries', 'question', 'chat_history'], 
    template=combine_prompt_template
    )

# load llm chain using RetrievalQAWithSourcesChain
chain = RetrievalQAWithSourcesChain.from_llm(
    llm=llm, 
    retriever=store.as_retriever(), 
    combine_prompt=combine_prompt,
    memory=memory,
    verbose=True
    )

# streamlit
st.set_page_config(
    page_title="Documents Q&A",
    page_icon=":shark:"
    )
st.header("Documents Q&A")

iteration = 0 
input = st.text_input('User: ', key=iteration)
while input:
    output = chain({
        "question": input
    })
    response = f"{output['answer']}\nSources: {output['sources']}"
    st.write("AI: ")
    st.write(response)

    with st.expander('Chat History'):
        st.info(memory.dict())

    iteration += 1
    input = st.text_input('User: ', key=iteration)

