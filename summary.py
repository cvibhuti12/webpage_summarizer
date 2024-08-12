import google.generativeai as genai
import os

API_KEY=''

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

def get_summary(text, words):
    response = model.generate_content(
      "summarize the given text :"+text+"in"+str(words)+"words",
        generation_config=genai.types.GenerationConfig(
          candidate_count=1,
        )
    )
    all_responses = ""
    for response in response:
      for part in response.parts:
        if part.text:
          all_responses=part.text
    return all_responses
