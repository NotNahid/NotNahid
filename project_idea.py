import google.generativeai as genai
import os
import re

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

prompt = "Generate a fun and challenging project idea for a front-end developer. The idea should be described in one or two sentences."
response = model.generate_content(prompt)

project_idea = response.text

with open("PROFILE_README.md", "r") as f:
    content = f.read()

new_content = re.sub(
    r"(?<=<!-- PROJECT-IDEA-START -->\n).*(?=\n<!-- PROJECT-IDEA-END -->)",
    f"```\n{project_idea}\n```",
    content,
    flags=re.DOTALL,
)

with open("PROFILE_README.md", "w") as f:
    f.write(new_content)
