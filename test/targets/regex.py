import re   # pragma: no cover

def regex(string):
    """This function returns at least one matching digit."""
    pattern = re.compile(r"^(\d+)") # For brevity, this is the same as r"\d+"
    result = pattern.match(string)
    if result:
        return  result.group()
    return None

