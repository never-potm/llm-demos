import argparse
import os

from dotenv import load_dotenv

from providers.ollama import OllamaProvider
from utils.website import Website
from providers.openai import OpenAIProvider

model = "gpt-5-nano"


def generate_brochure_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--name", default="Google", help="Website name")
    parser.add_argument("--url", default="https://www.google.com", help="Website URL")
    parser.add_argument("--provider", default="ollama", help="Select Provider - openai, ollama")


def run(args: argparse.Namespace) -> None:
    print(f"Generate company summary for {args.name} with {args.url}")

    load_dotenv(override=True)

    website_name = args.name
    save_to_file = f"outputs/{website_name.lower()}.md"

    provider = get_provider(args.provider)
    summary = summarize(provider, args.url)

    print_summary(summary, save_to_file)


def user_prompt_for(website):
    user_prompt = f"You are looking at a website titled {website.title}"
    user_prompt += "\nThe contents of this website is as follows; please provide a short summary of this website in markdown. If it includes news or announcements, then summarize these too."
    user_prompt += website.text
    return user_prompt


def summarize(provider, url):
    website = Website(url)
    return provider.generate(messages_for(website))


def messages_for(website):
    return [
        {"role": "system",
         "content": "You are an assistant that analyzes the contents of a website and provides a short summary, ignoring text that might be navigation related. Respond in markdown."},
        {"role": "user", "content": user_prompt_for(website)}
    ]


def print_summary(summary="", save_to_file=None):
    # Also save to file if path is given
    if save_to_file:
        with open(save_to_file, "w", encoding="utf-8") as f:
            f.write(summary)

    print("Summary saved to", save_to_file)

def get_provider(name: str):
    if name == "openai":
        provider = OpenAIProvider(model)
    elif name == "ollama":
        provider = OllamaProvider("llama3.2")
    else:
        raise ValueError(f"Unknown provider: {name}")

    return provider
