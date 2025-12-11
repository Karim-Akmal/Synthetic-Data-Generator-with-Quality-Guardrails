import yaml
import json
import argparse
import os
import requests
from openai import OpenAI
import random
import time


# Load Yamel file 

def load_config(path: str):
    with open(path, "r") as f:
        return yaml.safe_load(f)


# HuggingFace Inference API Provider

class HFProviderAPI:
    def __init__(self, model_name: str):
        self.model_name = model_name

        self.api_url = "https://router.huggingface.co/v1/chat/completions"

        hf_key = os.getenv("HUGGINGFACE_API_KEY")
        
        self.headers = {
            "Authorization": f"Bearer {hf_key}",
            "Content-Type": "application/json"
        }

    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 200
        }

        response = requests.post(self.api_url, headers=self.headers, json=payload)

        data = response.json()

        return data["choices"][0]["message"]["content"].strip()


# OpenAI Provider
class OpenAIProvider:
    def __init__(self, model_name: str):
        self.model_name = model_name

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("ERROR: OPENAI_API_KEY not found in environment variables.")

        self.client = OpenAI()

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens = 200
        )
        return response.choices[0].message.content.strip()



# Selecting the provider

def load_provider(provider_cfg):
    provider_type = provider_cfg["provider"]
    model_name = provider_cfg["model_name"]

    if provider_type == "huggingface":
        return HFProviderAPI(model_name)

    elif provider_type == "openai":
        return OpenAIProvider(model_name)
    else:
        raise ValueError(f"Unknown provider: {provider_type}")




# Generate Reveiwws

def build_prompt(tool, persona, rating):

    prompt = (
        f"As a {persona}, write a {rating}-star review about {tool}. Make it realistic as possible and only about 20 words."
    )

    return prompt

def generate_reviews(config):
    num_reviews = config["num_reviews"]

    providers = [load_provider(p) for p in config["models"]]

    all_reviews = []
    provider_index = 0
    flag = False
    for iter in range(num_reviews):
        provider = providers[provider_index]
        tool = config["tool"]
        persona = random.choice(config["personas"])
        rating = random.choice(config["rating_distribution"])

        prompt = build_prompt(tool, persona, rating)
        review_text = provider.generate(prompt)

        all_reviews.append({
            "Persona": persona,
            "Rating": rating,
            "Review Text": review_text
        })

        provider_index = (provider_index + 1) % len(providers)
        print(iter)
        # Wait for 0.5 seconds because of rate limit
        if iter %15 == 0 and flag:
            time.sleep(60)
        flag = True
    return all_reviews



# Mian

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", default="reviews.json")
    args = parser.parse_args()

    config = load_config(args.config)
    reviews = generate_reviews(config)

    with open(args.output, "w") as f:
        json.dump(reviews, f, indent=4)

    print(f"✅ Successfully generated {len(reviews)} reviews → {args.output}")
