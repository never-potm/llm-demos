import argparse

from ai_company_brochure.run import add_args as m1_add_args, run as m1_run

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="runner", description="Run a selected module.")
    sub = parser.add_subparsers(dest="module", required=True)

    # Expose as `module-1`/`module-2` on the CLI, map to module_1/module_2 in code
    p1 = sub.add_parser("module-1", help="Run module 1")
    m1_add_args(p1)
    p1.set_defaults(func=m1_run)

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()