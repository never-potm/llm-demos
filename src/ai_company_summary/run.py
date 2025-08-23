import argparse
import os

import openai
from dotenv import load_dotenv

from utils.website import Website

model = "gpt-5-nano"


def generate_brochure_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--name", default="Google", help="Website name")
    parser.add_argument("--url", default="https://www.google.com", help="Website URL")


def run(args: argparse.Namespace) -> None:
    print(f"Generate company summary for {args.name} with {args.url}")

    load_dotenv(override=True)
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("API Key not found in .env")
    elif not api_key.startswith("sk-"):
        print("API Key was found but it does not start with 'sk-'")
    elif api_key.strip() != api_key:
        print("API Key was found but it contains leading or trailing whitespace")
    else:
        print("API Key is valid")

    website_name = args.name
    save_to_file = f"outputs/{website_name.lower()}.md"
    print_summary(args.url, save_to_file)


def user_prompt_for(website):
    user_prompt = f"You are looking at a website titled {website.title}"
    user_prompt += "\nThe contents of this website is as follows; please provide a short summary of this website in markdown. If it includes news or announcements, then summarize these too."
    user_prompt += website.text
    return user_prompt


def summarize(url):
    website = Website(url)
    response = openai.chat.completions.create(
        model=model,
        messages=messages_for(website)
    )
    return response.choices[0].message.content


def messages_for(website):
    return [
        {"role": "system",
         "content": "You are an assistant that analyzes the contents of a website and provides a short summary, ignoring text that might be navigation related. Respond in markdown."},
        {"role": "user", "content": user_prompt_for(website)}
    ]


def print_summary(url, save_to_file=None):
    summary = summarize(url)

    # Also save to file if path is given
    if save_to_file:
        with open(save_to_file, "w", encoding="utf-8") as f:
            f.write(summary)

    print("Summary saved to", save_to_file)
