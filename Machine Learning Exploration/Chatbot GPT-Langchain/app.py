# Import Dependencies
import os
from apikey import api_key

import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper


os.environ['OPENAI_API_KEY'] = api_key

# App Framework
st.title('🦜🔗 Dicoding x Diskusai Chatbot')
prompt = st.text_input('Apa yang ingin anda tanyakan:')

# Buat Template Prompt
answer_template = PromptTemplate(
    input_variables= ['question'],
    template= 'Jawab pertanyaan ini "{question}" dengan jelas dan singkat'
)

sources_template = PromptTemplate(
    input_variables= ['answer', 'wikipedia_research'],
    template= 'Berikan satu atau beberapa link yang berhubungan dengan ini: "{answer}". Selain itu, berikan juga sumber wikipedia berikut: "{wikipedia_research} (jika ada)'
)

# Memory
answer_memory = ConversationBufferMemory(input_key='question', memory_key= 'chat_history')
sources_memory = ConversationBufferMemory(input_key='answer', memory_key= 'chat_history')

# LLMs
llm = OpenAI(temperature=0.9)
answer_chain = LLMChain(llm=llm, prompt=answer_template, verbose=True, output_key='answer', memory=answer_memory)
sources_chain = LLMChain(llm=llm, prompt=sources_template, verbose=True, output_key='sources', memory=sources_memory)
wiki = WikipediaAPIWrapper()

# sequential_chain = SequentialChain(chains=[answer_chain, sources_chain], input_variables=['question'], 
# output_variables=['answer','sources'], verbose=True)

# Menampilkan output jika ada input
if prompt:
    answer = answer_chain.run(prompt)
    wiki_research = wiki.run(prompt)
    sources = sources_chain.run(answer=answer, wikipedia_research=wiki_research)
    st.write(answer)
    st.write(sources)

    with st.expander('Answer History'):
        st.info(answer_memory.buffer)

    with st.expander('Sources History'):
        st.info(sources_memory.buffer)

    with st.expander('Wikipedia Research'):
        st.info(wiki_research)