import argparse
import json

from dotenv import load_dotenv

from providers.ollama import OllamaProvider
from utils.file import create_file_with
from utils.website import Website
from providers.openai import OpenAIProvider


def generate_brochure_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--name", default="Google", help="Website name")
    parser.add_argument("--url", default="https://www.google.com", help="Website URL")
    parser.add_argument("--provider", default="ollama", help="Select Provider - openai, ollama")
    parser.add_argument("--stream", default="False", help="Stream contents to file ( default: False )")
    parser.add_argument("--language", default="English", help="Convert brochure to language ( default: English )")


def run(args: argparse.Namespace) -> None:
    print(f"Generate company brochure for {args.name} with {args.url} in {args.language}")

    load_dotenv(override=True)

    website_name = args.name
    save_to_file = f"outputs/brochures/{website_name.lower()}/{website_name.lower()}_{args.language}.md"
    provider = get_provider(args.provider, args.stream)
    # website_link_content = get_website_links(provider, args.url)

    brochure_details = create_brochure(provider, args.name, args.url, args.language, args.stream)

    create_file_with(brochure_details, save_to_file)


def create_brochure(provider, company_name, url, language, stream=False):
    prompt = get_brochure_user_prompt(provider, company_name, url, language)
    return provider.chat(prompt)


def get_brochure_user_prompt(provider, company_name, url, language):
    user_prompt = f"You are looking at a company called: {company_name}\n"
    user_prompt += f"Here are the contents of its landing page and other relevant pages. Use this information to build a short brochure of the company in markdown. Do not output anything other than company information in the output file. Do not include any signin/ signup information in the brochure. And convert the brochure to {language}\n"
    user_prompt += get_all_website_details(provider, url)
    user_prompt = user_prompt[:6_000]  # Truncate if more than 5,000 characters
    return user_prompt


def get_all_website_details(provider, url):
    result = "Landing page:\n"
    result += Website(url).get_contents()
    links = get_website_links(provider, url)
    for link in links["links"]:
        result += f"\n\n{link['type']}\n"
        result += Website(link["url"]).get_contents()
        print(f"Getting info for link: {link}, URL: {link['url']}")

    return result


def get_website_links(provider, url):
    website = Website(url)
    prompt = prompt_to_scrape_links_for(website)
    content = provider.chat(prompt)
    return json.loads(content)


def prompt_create_brochure_for(website):
    system_prompt = "You are an assistant that analyzes the contents of several relevant pages from a company website \
    and creates a short brochure about the company for prospective customers, investors and recruits. Respond in markdown.\
    Include details of company culture, customers and careers/jobs if you have the information."

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": get_brochure_user_prompt(website)}
    ]


def prompt_to_scrape_links_for(website):
    link_system_prompt = "You are provided with a list of links found on a webpage. \
    You are able to decide which of the links would be most relevant to include in a brochure about the company, \
    such as links to an About page, or a Company page, or Careers/Jobs pages.\n"
    link_system_prompt += "You should respond in JSON as in this example. It should be strictly JSON, do not include any other text."
    link_system_prompt += """
    {
        "links": [
            {"type": "about page", "url": "https://full.url/goes/here/about"},
            {"type": "careers page", "url": "https://another.full.url/careers"}
        ]
    }
    """

    return [
        {"role": "system", "content": link_system_prompt},
        {"role": "user", "content": user_prompt_for(website)}
    ]


def user_prompt_for(website):
    user_prompt = f"Here is the list of links on the website of {website.url} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. \
    Do not include Terms of Service, Privacy, email links.\n"
    user_prompt += "Links (some might be relative links):\n"
    user_prompt += "\n".join(website.links)
    return user_prompt


def get_provider(model_name: str, stream: bool):
    if model_name == "openai":
        provider = OpenAIProvider(stream)
    elif model_name == "ollama":
        provider = OllamaProvider(stream)
    else:
        raise ValueError(f"Unknown provider: {model_name}")

    return provider
