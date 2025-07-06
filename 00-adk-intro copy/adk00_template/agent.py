from google.adk.agents import Agent

## add this - start
from dotenv import load_dotenv
load_dotenv()
## add this - end

root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
