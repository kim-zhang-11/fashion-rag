import os
import json
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
from typing import Sequence


def get_history(session_id):
    return FileChatMessageHistory(session_id, "./chat_history")

class FileChatMessageHistory(BaseChatMessageHistory):

    def __init__(self,session_id,storage_path):
        self.session_id=session_id
        self.storage_path=storage_path
        # full file path
        self.file_path =os.path.join(self.storage_path,self.session_id)
        # make sure the folder exists
        os.makedirs(os.path.dirname(self.file_path),exist_ok=True)
    def add_messages(self, messages: Sequence[BaseMessage])->None:
        # Sequence: similar to list \ tuple
        all_messages=list(self.messages) # the existing messages
        all_messages.extend(messages)    # merge new and existing messages into one list
        #
        # new_messages=[]
        # for message in all_messages:
        #     d=message_to_dirt(message)
        #     new_messages.append(d)d
        new_messages=[message_to_dict(message) for message in all_messages]
        # write the data to the file
        with open(self.file_path,"w",encoding="utf-8")as f:
            json.dump(new_messages,f)
    @property     # the decorator turns the messages method into an attribute
    def messages(self)-> list[BaseMessage]:
        # the file holds: list[dict]
        try:
            with open(self.file_path,"r",encoding="utf-8")as f:
                message_data= json.load(f)    # the return value is a list of dicts
                return messages_from_dict(message_data)
        except (FileNotFoundError,json.JSONDecodeError):        # catching only FileNotFoundError would leave JSONDecodeError and the like unhandled

            """When the history file exists but is empty or corrupted, e.g. cleared by hand or partially written, json.load(f) raises JSONDecodeError and crashes the system"""

            return []

    def clear(self) -> None:
        with open(self.file_path,"w",encoding="utf-8")as f:
                json.dump([],f)

