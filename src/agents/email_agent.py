from dotenv import load_dotenv
from langchain_google_community import GmailToolkit
from langchain.chat_models import init_chat_model
from langchain_google_community.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)
from langgraph.prebuilt import create_react_agent

load_dotenv()



#pragash.jeyaratnam@gmail.com 
credentials = get_gmail_credentials(
    token_file = "token.json",
    scopes=[ 'https://www.googleapis.com/auth/gmail.compose',
            'https://www.googleapis.com/auth/gmail.modify',
            'https://www.googleapis.com/auth/gmail.send'],
    client_secrets_file="credentials.json",
)

api_resource = build_resource_service(credentials=credentials)
toolkits = GmailToolkit(api_resource=api_resource)

tools = toolkits.get_tools()

llm = init_chat_model("gpt-4o-mini",model_provider="openai")
agent_executor = create_react_agent(llm,tools)

example_query = "Draft an email to desmond80in@gmail.com thanking them for the coffee."

events = agent_executor.stream(
    {"messages": [("user",example_query)]},stream_mode= "values"
)

for event in events:
    event["messages"][-1].pretty_print()

