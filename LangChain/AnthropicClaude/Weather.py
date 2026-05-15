# https://docs.langchain.com/oss/python/langchain/overview

# pip install -qU langchain "langchain[anthropic]"

import sys
import json_repair
from langchain.agents import create_agent
import requests


def get_weather(city: str) -> str:
    """ Get weather for a given city """
    url = "https://jisnukrsna.world:7878/gw"
    form_data = {
        'city': city,
    }
    response = requests.post(url, data=form_data)
    # print(response.status_code, response.text)
    return f"Here's weather conditions for {city} ..." + response.text


args = sys.argv

if (len(args)) != 3:
    print("\n\tNeed <model like claude-sonnet-4-6> <city like pune> as args\n")
    sys.exit()

model = sys.argv[1]
city = sys.argv[2]

agent = create_agent(
    model = model,
    tools = [get_weather],
    # description = "Current weather conditions",
    system_prompt = "You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": f"What's the weather in {city}?"}]}
)

fake_json = str(result["messages"][-1].content_blocks)

real_json = json_repair.repair_json(fake_json)

print(real_json)
