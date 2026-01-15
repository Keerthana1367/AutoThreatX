def parse_numbered_list(text: str) -> list[str]:
    lines = []
    for l in text.splitlines():
        l = l.strip()
        if len(l) > 2 and l[0].isdigit() and l[1] == ".":
            lines.append(l.split(".", 1)[1].strip())
    return lines
