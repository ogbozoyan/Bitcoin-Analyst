import autogen

# https://www.phind.com/search?cache=wfun3ekgjysi1ehqbpk2kiad
# -------------------------------------------------- CONSTANTS --------------------------------------------------
OPENAI_API_KEY = "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"
CRYPTO_PANIC_API_KEY = "dfb5a55ca0113013b4c12b868878b60c314b83cd"
GNEWS_PANIC_API_KEY = "9b1f2b7c8f47fba64b98e1e52ebf8eb4"
MAX_ROUNDS = 12
# CONFIGS
config_list = [
    {
        # gpt-4-32k-0613
        # gpt-4-0613
        # gpt-4-32k
        # gpt-4
        'model': 'gpt-4-1106-preview',
        'api_key': OPENAI_API_KEY,
    }
]
DEFAULT_LLM_CONFIG = {
    "seed": 43,  # seed for caching and reproducibility
    "config_list": config_list,  # a list of OpenAI API configurations
    "temperature": 0,  # temperature for sampling
}
ANALYST_LLM_CONFIG = {
    "seed": 43,  # seed for caching and reproducibility
    "config_list": config_list,  # a list of OpenAI API configurations
    "temperature": 0.5,  # temperature for sampling
}
# /CONFIGS

USER_PROXY_NAME = "user_proxy"
CODER_NAME = "coder"
SENIOR_NAME = "seniorAssistant"
CRITIC_NAME = "criticAssistant"
JUNIOR_NAME = "juniorAssistant"

CODER_ROLE = """
                   Professional parser coder. I will return the news in 
                                {source} - {date}: {news} 
                   in the following format.
                   """
USER_PROXY_ROLE = """
                Initiating the data retrieval process with the Parser which gives Coder and passing the 
                information through the analyst hierarchy: 
                junior -> critic -> senior
    """
SENIOR_ROLE = """
        You are the most experienced analyst and know how to analyze the news and the value of cryptocurrencies
        You have been given news, from a junior analyst, from a critic.
        You need to collect yourself, take a deep breath and based on all these data to make an informed decision,
         on which depends a lot, mistakes can be very costly, so you need to take it very seriously and 
         when you are 99.9 percent confident
        in your analysis to give an answer:
            I, as a senior analyst, think WHAT:
            {answer}
        You can't tell me that it's not possible to make an informed decision, you must always give a logical answer.
    """
CRITIC_ROLE = """
        You are an experienced analyst and know how to analyze news and the value of cryptocurrencies 
        You have been given an analysis from a less experienced juniorAssistant, please give your constructive criticism 
        and offer your hypothesis.Your task is to analyze the news about cryptocurrencies and determine what caused 
        the change in their price.You must propose a hypothesis about possible factors based on this news, 
        provide evidence for your hypothesis and make a buy or sell recommendation.
    """
JUNIOR_ROLE = """
        You are an experienced analyst and know how to analyze news and the value of cryptocurrencies 
        Your task is to analyze the news about cryptocurrencies and determine what caused the change in their price.
        You must propose a hypothesis about possible factors based on this news, provide evidence for your hypothesis and
        make a buy or sell recommendation.
    """
# -------------------------------------------------- /CONSTANTS --------------------------------------------------

# create an AssistantAgent named "assistant"
juniorAssistant = autogen.AssistantAgent(
    system_message=JUNIOR_ROLE,
    name=JUNIOR_NAME,
    llm_config=ANALYST_LLM_CONFIG,
)
criticAssistant = autogen.AssistantAgent(
    system_message=CRITIC_ROLE,
    name=CRITIC_NAME,
    llm_config=ANALYST_LLM_CONFIG,
)
seniorAssistant = autogen.AssistantAgent(
    system_message=SENIOR_ROLE,
    name=SENIOR_NAME,
    llm_config=ANALYST_LLM_CONFIG,
)
coderAgent = autogen.AssistantAgent(
    # system_message=CODER_ROLE,
    name=CODER_NAME,
    llm_config=DEFAULT_LLM_CONFIG,
)

userProxy = autogen.UserProxyAgent(
    name=USER_PROXY_NAME,
    system_message=USER_PROXY_ROLE,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=MAX_ROUNDS,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        # "work_dir": "./",
        "use_docker": False,  # Assuming local execution
    },
)

groupChat = autogen.GroupChat(
    agents=[userProxy, coderAgent, seniorAssistant, juniorAssistant, criticAssistant],
    messages=[],
    max_round=MAX_ROUNDS
)

if __name__ == "__main__":
    manager = autogen.GroupChatManager(groupchat=groupChat, llm_config=DEFAULT_LLM_CONFIG)
    userProxy.initiate_chat(
        manager,
        message="""
            Please fetch the last 7 days of Bitcoin data from the specified sources:
            - https://cryptopanic.com/
            - https://gnews.io/
            cryptopanic api token: {}
            gnews api token: {}
            also don't forget to add current bitcoin price to the news
            """.format(CRYPTO_PANIC_API_KEY, GNEWS_PANIC_API_KEY)
    )