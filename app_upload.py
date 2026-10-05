"""
Web upload service built on Streamlit

Streamlit: whenever a page element changes the script reruns from the top, so state is not kept
"""
import streamlit as st
import time


from src.knowledge_base.base import KnowledgeBaseService


# add the page title
st.title("知识库更新服务")

# file_uploader
uploader_files=st.file_uploader(
    "请上传TXT文件",
    type=['txt'],
    accept_multiple_files=True,   # True allows uploading multiple files
)

if "service" not in st.session_state:          # session state dict; session_state itself is a dict too
    st.session_state["service"]=KnowledgeBaseService()

if uploader_files is not None and len(uploader_files) > 0:
    # process each uploaded file one by one
    for uploader_file in uploader_files:
        # extract the file info
        file_name = uploader_file.name
        file_type = uploader_file.type
        file_size = uploader_file.size /1024
        st.subheader(f"文件名:{file_name}")
        st.write(f"格式:{file_type}  | 大小:{file_size:.2f}KB")

        # get_value -> bytes -> decode("utf-8")
        text=uploader_file.getvalue().decode("utf-8")

        with st.spinner(f"载入知识库中...({file_name})"):     # a spinner animation shows while the code inside runs, for a better user experience
            time.sleep(1)
            result= st.session_state["service"].upload_by_str(text,file_name)
            st.write(result)
