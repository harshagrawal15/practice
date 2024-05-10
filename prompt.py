import openai
import pandas as pd

# Set your OpenAI API key
openai.api_key = 'sk-proj-9sZFpGhxMuYUryvwRmgJT3BlbkFJ00QZvgler9J8iU4PbDLW'

# Function to run OpenAI prompt
def run_openai_prompt(prompt):
    response = openai.Completion.create(
        engine="davinci-002",
        prompt=prompt,
        max_tokens=300
    )
    return response.choices[0].text.strip()

# Read CSV file
df = pd.read_csv('company.csv')

# Iterate over each row
for index, row in df.iterrows():
    # Get company information
    company_name = row['Company Name']
    company_website = row['Company Website']
    homepage_info = row['Description']

    # Prompt 1
    prompt1 = f"Here's the raw homepage information of my target company, {company_name}. I need you to convert this into a 200 word summary that is organized in the following manner:\n\n- Company overview\n- Product and service offering recap\n- Potential target industries for this company\n- What is their core USP\n- How many times have they used the word 'AI' in their homepage.\n\nHere's the homepage information:\n\n{homepage_info}"
    output1 = run_openai_prompt(prompt1)

    # Prompt 2
    prompt2 = f"I will give you the company overview of a target company I'm trying to pitch to, {company_name}. Can you read through their offering and create a potential sales opportunity for me?\n\nMy company offers custom HR training and modules.\n\nYour potential sales opportunity analysis should be 150 words. It should have multiple bullet points and tell me how I can posit my solution. Ensure it is highly custom built and includes the target company's industry terminology.\n\nHere's the summary:\n\n{output1}"
    output2 = run_openai_prompt(prompt2)

    # Prompt 3
    prompt3 = f"I will give you a potential sales opportunity analysis for a company I'm targeting, {company_name}.\n\nYou have to create a custom 100 word sales email.\n\nThe email has to look at elements about what the company offers from ###Company overview### and should include potential sales hooks from ###sales opportunity analysis###.\n\nKeep the text extremely human and to the point.\n\n###Company overview###\n{output1}\n\n###sales opportunity analysis###\n{output2}"
    output3 = run_openai_prompt(prompt3)

    # Store or use the outputs as needed
    df.at[index, 'Prompt 1 Output'] = output1
    df.at[index, 'Prompt 2 Output'] = output2
    df.at[index, 'Prompt 3 Output'] = output3

# Save the updated DataFrame
df.to_csv('company_data_with_outputs.csv', index=False)
