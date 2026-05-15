#!/usr/bin/env bash

# Weather.sh

printf "\nUsing Google Gemini ...\n\n"
GoogleGemini/Weather.sh google_genai:gemini-2.5-flash-lite pune

printf "\nUsing OpenAI ...\n\n"
OpenAI/Weather.sh openai:gpt-5.4 pune

echo
