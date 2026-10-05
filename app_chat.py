import streamlit as  st
from src.chatbot.rag import RagService
from src import config
import time

# title
st.title("智能客服")
# divider
st.divider()

# keep the objects in session_state to avoid the cost of rebuilding them
if "message" not in st.session_state:
    st.session_state["message"]=[{"role":"assistant","content":"你好，有什么可以帮助你？"}]

if "rag" not in st.session_state:
    st.session_state["rag"]= RagService()
# loop over and render the history, which would otherwise be recorded but not shown on the page
for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])
# user input box at the bottom of the page
prompt= st.chat_input()

if prompt :
    # render the user's question on the page
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role":"user","content":prompt})

    ai_res_list= []
    with st.spinner("AI 思考中......."):
        # call the RAG service

        # direct (non-streaming) output
        # res= st.session_state["rag"].chain.invoke({"input":prompt},config.session_config)
        #
        # st.chat_message("assistant").write(res)
        # st.session_state["message"].append({"role":"assistant","content":res})

        # streaming output
        res_stream = st.session_state["rag"].chain.stream({"input": prompt}, config.session_config)

        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk
        st.chat_message("assistant").write_stream(capture(res_stream,ai_res_list))
        st.session_state["message"].append({"role": "assistant", "content": "".join(ai_res_list)})

