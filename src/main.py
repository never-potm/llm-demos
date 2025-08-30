import argparse

from modules.ai_company_summary.run import generate_summary_args, run as m1_run

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="runner", description="Run a selected module.")
    sub = parser.add_subparsers(dest="module", required=True)

    p1 = sub.add_parser("ai_company_summary", help="Generate company brochure.")
    generate_summary_args(p1)
    p1.set_defaults(func=m1_run)

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()