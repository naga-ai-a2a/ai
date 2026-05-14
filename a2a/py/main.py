# import os
import requests
from langchain_ollama import ChatOllama
from langchain.tools import tool
# from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from python_a2a import A2AServer, TaskState, TaskStatus, skill, agent, run_server
# from python_a2a.types import TaskStatus, TaskState
from langchain.agents import create_agent
from langchain_classic.agents import AgentExecutor

# 1. Define the External Service Tool (Weather)
@tool
def get_weather(location: str) -> str:
    """Get the current weather for a specified location."""
    # Using a free weather API for demonstration
    api_key = "YOUR_OPENWEATHERMAP_API_KEY" # Replace with actual key
    url = f"http://openweathermap.org{location}&appid={api_key}&units=metric"
    try:
        response = requests.get(url).json()
        temp = response['main']['temp']
        desc = response['weather'][0]['description']
        return f"The weather in {location} is {temp}°C with {desc}."
    except Exception as e:
        return f"Could not find weather for {location}. Error: {e}"

# 2. Configure Llama 3.1 via Ollama
llm = ChatOllama(model="llama3.1", temperature=0)
tools = [get_weather]

# 3. Create the Agentic Workflow
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful weather assistant. Use tools to find real-time data."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# Create the LangChain agent
# agent_executor = create_tool_calling_agent(llm, tools, prompt)
agent_executor = create_agent(model="ollama:llama3.1")
agent_executor = AgentExecutor(agent=agent_executor, tools=tools, verbose=True)

# 4. Define the A2A Agent Server
@agent(
    name="WeatherAgent",
    description="An agent that provides real-time weather information using Llama 3.1"
)
class WeatherA2AAgent(A2AServer):
    @skill(name="AskWeather", description="Get weather for a city")
    def handle_task(self, task):
        user_input = task.message.get("content", {}).get("text", "")
        
        # Invoke LangChain Agent
        result = agent_executor.invoke({"input": user_input})
        
        # Structure the A2A response
        task.artifacts = [{"parts": [{"type": "text", "text": result["output"]}]}]
        task.status = TaskStatus(state=TaskState.COMPLETED)
        return task

# 5. Run the Agent
if __name__ == "__main__":
    # This runs the agent as an A2A compliant server
    # run_server(WeatherA2AAgent("https://jisnukrsna.world:7878/gw"))
    a2aserver = A2AServer.
    print("OK")
