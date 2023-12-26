import autogen

config_list_mistral = [
    {
        'base_url': "http://0.0.0.0:8000",
        'api_key': "NULL"
    }
]

config_list_codellama = [
    {
        'base_url': "http://0.0.0.0:35614",
        'api_key': "NULL"
    }
]

llm_config_mistral={
    "config_list": config_list_mistral,
}

llm_config_codellama={
    "config_list": config_list_codellama,
}

assistant = autogen.AssistantAgent(
    name="Assistant",
    llm_config=llm_config_mistral
)

coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config_codellama
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web"},
    llm_config=llm_config_mistral,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)

task="""
Write a python script to finetune a model designed for code generation.
"""
groupchat = autogen.GroupChat(agents=[user_proxy, assistant, coder], messages=[], max_round=12)
product_manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config_mistral)
user_proxy.initiate_chat(product_manager, message=task)