def _to_bool(x) -> bool:
    if isinstance(x, bool):
        return x
    if isinstance(x, str):
        v = x.strip().lower()
        if v in ("1","true","t","yes","y","on"):
            return True
        if v in ("0","false","f","no","n","off"):
            return False
    raise ValueError("stream must be a bool or one of: true/false/yes/no/1/0")