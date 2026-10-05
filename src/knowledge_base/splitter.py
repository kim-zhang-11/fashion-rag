import re

# heading patterns, the index is the level: 0 -> "一、xxx", 1 -> "1. xxx"
heading_patterns = [
    re.compile(r"^[一二三四五六七八九十百]+、\s*(.+)$"),
    re.compile(r"^\d+[.．、]\s*(.+)$"),
]
sentence_end_chars = "。！？；.!?;"   # a numbered line ending with sentence punctuation is a body item, not a heading
max_heading_char_number = 50          # max length of a heading


def match_heading(line: str):
    """Check whether a line is a heading
            return (level, heading text), or None if it is not a heading
    """
    if len(line) > max_heading_char_number or line[-1] in sentence_end_chars:
        return None
    for level, pattern in enumerate(heading_patterns):
        matched = pattern.match(line)
        if matched:
            return level, matched.group(1)
    return None


def split_by_heading(text: str) -> list[tuple[list[str], str]]:
    """Split text into sections by heading
            return [(heading path, body), ...]; the heading path runs from the top level down to the section's own heading, and is an empty list for body text under no heading
    """
    sections = []
    path = {}     # level -> the heading currently in effect
    body = []     # body lines of the current section

    def flush():
        if body:
            sections.append(([path[level] for level in sorted(path)], "\n".join(body)))
            body.clear()

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        heading = match_heading(line)
        if heading is None:
            body.append(line)
            continue
        # new heading: close the previous section and drop old headings at the same or deeper levels
        flush()
        level, title = heading
        path = {k: v for k, v in path.items() if k < level}
        path[level] = title
    flush()

    return sections


def format_heading_path(titles: list[str]) -> str:
    """Join a heading path into one line, e.g. 夏季服装 > 真丝材质（夏季连衣裙、衬衫）"""
    # a parent heading's parentheses list its sub-sections, which would blur the embedding; keep parentheses only on the section's own heading
    parents = [re.sub(r"[（(][^（）()]*[）)]$", "", title) for title in titles[:-1]]
    return " > ".join(parents + titles[-1:])
