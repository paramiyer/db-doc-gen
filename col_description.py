import os
import yaml
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import re 

def generate_column_descriptions(df_schema, config_file_path):
    # === Load config from YAML ===
    with open(config_file_path, 'r') as f:
        config = yaml.safe_load(f)

    industry = config["industry"]
    domain = config["domain"]
    user_prompt_template = config["user_prompt"]
    openai_model = config.get("openai_model", "gpt-3.5-turbo")
    dotenv_path = config.get("dotenv_path", ".env")

    # === Load .env and setup OpenAI client ===
    load_dotenv(dotenv_path)
    client = OpenAI()  # reads OPENAI_API_KEY from environment

    # === Ensure 'Description' column exists ===
    if 'Description' not in df_schema.columns:
        df_schema['Description'] = None

    # === Cache to avoid redundant calls ===
    #description_cache = {}

    # === Inner function to call LLM ===
    def get_description(table, col):
     #   if col in description_cache:
      #      return description_cache[col]

        prompt = user_prompt_template.format(
            industry=industry,
            domain=domain,
            table=table,
            col=col
        )

        try:
            response = client.chat.completions.create(
                model=openai_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=100
            )
            result = response.choices[0].message.content.strip()
            result = re.sub(r"\b(\w+)'s\b", r"\1", result)
            #description_cache[col] = result
            return result
        except Exception as e:
            return f"Error: {e}"

    # === Populate descriptions in DataFrame ===
    for idx, row in df_schema.iterrows():
        if pd.isna(row['Description']) or not row['Description']:
            df_schema.at[idx, 'Description'] = get_description(row['Table'], row['Col'])

    return df_schema
