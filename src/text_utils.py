import re

from pypinyin import pinyin


def add_indexes_to_format_strings(text: str) -> str:
    """
    Converts unindexed format specifiers in the input text to indexed format specifiers.
    This function is useful when appending two language texts together, as it prevents issues
    with duplicate unindexed format strings.
    Args:
        text (str): The input text containing unindexed format specifiers.
    Returns:
        str: The text with indexed format specifiers.
    """
    specifier_pattern = re.compile(r"%(\d*\$)?[ds]")

    def replacer(match, counter=iter(range(1, 100))):
        return f"%{next(counter)}$s"

    return specifier_pattern.sub(replacer, text)


def add_pinyin(hanzi_input: str) -> str:
    pinyin_output = pinyin(hanzi_input)
    flattened_output = [
        pinyin for pinyin_list in pinyin_output for pinyin in pinyin_list
    ]
    result = " ".join(flattened_output)
    return f"{hanzi_input} ({add_indexes_to_format_strings(result)})"


def contains_chinese(text: str) -> bool:
    """Check if the text contains any Chinese characters."""
    return any("\u4e00" <= char <= "\u9fff" for char in text)
