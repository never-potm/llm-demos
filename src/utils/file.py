from pathlib import Path


def create_file_with(content="", save_to_file=None):
    # Also save to file if path is given
    if save_to_file:
        p = Path(save_to_file).expanduser()
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
        print("File content saved at ", save_to_file)
