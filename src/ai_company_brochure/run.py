import argparse

def add_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--name", default="world", help="Name to greet")
    parser.add_argument("--times", type=int, default=1, help="How many times")

def run(args: argparse.Namespace) -> None:
    for _ in range(args.times):
        print(f"[module-1] Hello, {args.name}!")