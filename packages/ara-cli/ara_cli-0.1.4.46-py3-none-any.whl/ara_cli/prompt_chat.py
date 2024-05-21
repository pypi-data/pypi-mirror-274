import os
import shutil
from ara_cli.chat import Chat
from ara_cli.classifier import Classifier

def initialize_prompt_chat_mode(classifier, param):
    sub_directory = Classifier.get_sub_directory(classifier)
    artefact_data_path = os.path.join("ara", sub_directory, f"{param}.data") # f"ara/{sub_directory}/{parameter}.data"
    prompt_data_path = os.path.join(artefact_data_path, "prompt.data")  # f"ara/{sub_directory}/{parameter}.data/prompt.data"
    
    if not os.path.exists(prompt_data_path):
        os.makedirs(prompt_data_path)

    prompt_config_givens = os.path.join(prompt_data_path, "config_prompt_givens.md")
    prompt_config_templates = os.path.join(prompt_data_path, "config_prompt_templates.md")
    classifier_chat_file = os.path.join(artefact_data_path, f"{classifier}_chat.md")

    create_or_update_file(prompt_config_givens)
    create_or_update_file(prompt_config_templates)
    create_or_update_file(classifier_chat_file)

    start_chat_session(classifier_chat_file)

def create_or_update_file(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("")
    else:
        choice = input(f"{file_path} already exists. Do you want to overwrite (o) or update (u)? ")
        if choice.lower() == 'o':
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write("")
        elif choice.lower() == 'u':
            append_new_content(file_path)

def append_new_content(file_path):
    new_content = input(f"Enter new content to append to {file_path}: ")
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(new_content)

def start_chat_session(chat_file):
    chat = Chat(chat_file)
    chat.start()