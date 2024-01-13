import autogen

# https://www.phind.com/search?cache=wfun3ekgjysi1ehqbpk2kiad
# -------------------------------------------------- CONSTANTS --------------------------------------------------
OPENAI_API_KEY = ""
config_list = [
    {
        'model': 'gpt-4',
        'api_key': OPENAI_API_KEY,
    }
]
DEFAULT_LLM_CONFIG = {
    "seed": 42,  # seed for caching and reproducibility
    "config_list": config_list,  # a list of OpenAI API configurations
    "temperature": 0,  # temperature for sampling
}
PARSER_ROLE = """
                   I am the professional parser coder. I will take the news and analyze it. I will fetch news from 
                   the internet and analyze it. I will return the news in 
                                {source} - {date}: {news} 
                   in the following format.
                   """
PARSER_NAME = "parserAssistant"
USER_PROXY_NAME = "user_proxy"
USER_PROXY_ROLE = """
        I act as the user, initiating the data retrieval process with the Parser and passing the 
        information through the analyst hierarchy: 
        junior -> critic -> senior
    """
SENIOR_ROLE = """
        You are the most experienced analyst and know how to analyze the news and the value of cryptocurrencies
        You have been given news, from a junior analyst, from a critic.
        You need to collect yourself, take a deep breath and based on all these data to make an informed decision, on which depends a lot,
        mistakes can be very costly, so you need to take it very seriously and when you are 99.9 percent confident
        in your analysis to give an answer:
            I, as a senior analyst, think WHAT:
            {answer}
    """
SENIOR_NAME = "seniorAssistant"
CRITIC_ROLE = """
        You are an experienced analyst and know how to analyze news and the value of cryptocurrencies 
        You have been given an analysis from a less experienced juniorAssistant, please give your constructive criticism and offer your hypothesis
        Your task is to analyze the news about cryptocurrencies and determine what caused the change in their price.
        You must propose a hypothesis about possible factors based on this news, provide evidence for your hypothesis and
        make a buy or sell recommendation.
    """
CRITIC_NAME = "criticAssistant"
JUNIOR_ROLE = """
        You are an experienced analyst and know how to analyze news and the value of cryptocurrencies 
        Your task is to analyze the news about cryptocurrencies and determine what caused the change in their price.
        You must propose a hypothesis about possible factors based on this news, provide evidence for your hypothesis and
        make a buy or sell recommendation.
    """
JUNIOR_NAME = "juniorAssistant"
# -------------------------------------------------- /CONSTANTS --------------------------------------------------

# create an AssistantAgent named "assistant"
juniorAssistant = autogen.AssistantAgent(
    system_message=JUNIOR_ROLE,
    name=JUNIOR_NAME,
    llm_config=DEFAULT_LLM_CONFIG,
    # configuration for autogen's enhanced inference API which is compatible with OpenAI API
)
criticAssistant = autogen.AssistantAgent(
    system_message=CRITIC_ROLE,
    name=CRITIC_NAME,
    llm_config=DEFAULT_LLM_CONFIG,
    # configuration for autogen's enhanced inference API which is compatible with OpenAI API
)
seniorAssistant = autogen.AssistantAgent(
    system_message=SENIOR_ROLE,
    name=SENIOR_NAME,
    llm_config=DEFAULT_LLM_CONFIG,
    # configuration for autogen's enhanced inference API which is compatible with OpenAI API
)
parserAgent = autogen.AssistantAgent(
    system_message=PARSER_ROLE,
    name=PARSER_NAME,
    llm_config=DEFAULT_LLM_CONFIG,
    # configuration for autogen's enhanced inference API which is compatible with OpenAI API
)
# create a UserProxyAgent instance named "user_proxy"
userProxy = autogen.UserProxyAgent(
    name=USER_PROXY_NAME,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,  # Assuming local execution
    },
    system_message=USER_PROXY_ROLE
)

if __name__ == "__main__":
    userProxy.initiate_chat(
        parserAgent,
        message="""
            Please fetch the last 7 days of Bitcoin data from the specified sources:
            - https://cryptopanic.com/
            - https://gnews.io/
            cryptopanic api token: dfb5a55ca0113013b4c12b868878b60c314b83cd
            gnews api token: 0f583dfc912cca75a244c9859528b8ab
            """
    )
