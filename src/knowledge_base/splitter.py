import re

# 标题的匹配规则，下标即层级：0 -> "一、xxx"，1 -> "1. xxx"
heading_patterns = [
    re.compile(r"^[一二三四五六七八九十百]+、\s*(.+)$"),
    re.compile(r"^\d+[.．、]\s*(.+)$"),
]
sentence_end_chars = "。！？；.!?;"   # 以句末标点结尾的编号行是正文条目，不是标题
max_heading_char_number = 50          # 标题的最大长度


def match_heading(line: str):
    """判断一行是否为标题
            return (层级, 标题文本)，不是标题返回None
    """
    if len(line) > max_heading_char_number or line[-1] in sentence_end_chars:
        return None
    for level, pattern in enumerate(heading_patterns):
        matched = pattern.match(line)
        if matched:
            return level, matched.group(1)
    return None


def split_by_heading(text: str) -> list[tuple[list[str], str]]:
    """按标题将文本切成小节
            return [(标题路径, 正文), ...]，标题路径从上级到本级，没有标题的正文其路径为空列表
    """
    sections = []
    path = {}     # 层级 -> 当前所处的标题
    body = []     # 当前小节的正文行

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
        # 遇到新标题：结束上一小节，并丢弃同级及更深层级的旧标题
        flush()
        level, title = heading
        path = {k: v for k, v in path.items() if k < level}
        path[level] = title
    flush()

    return sections


def format_heading_path(titles: list[str]) -> str:
    """将标题路径拼成一行，如：夏季服装 > 真丝材质（夏季连衣裙、衬衫）"""
    # 上级标题括号里是下属小节的罗列，拼进来会干扰向量语义，只保留本级标题的括号
    parents = [re.sub(r"[（(][^（）()]*[）)]$", "", title) for title in titles[:-1]]
    return " > ".join(parents + titles[-1:])
