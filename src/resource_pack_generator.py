import json
import os

from src.text_utils import add_indexes_to_format_strings, add_pinyin, contains_chinese


def _generate_language_file(
    chinese_json: dict[str, str], english_json: dict[str, str]
) -> dict[str, str]:
    """Process the input file, adding pinyin and English translations, and save the output."""
    # Process each line, adding pinyin and corresponding English translations if available
    modified_content = {}
    for key, value in chinese_json.items():
        if contains_chinese(value):
            pinyin_text = add_pinyin(value)
            english_translation = english_json.get(key)
            if english_translation:
                modified_content[key] = (
                    f"{pinyin_text} [{add_indexes_to_format_strings(english_translation)}]"
                )
            else:
                modified_content[key] = pinyin_text
        else:
            modified_content[key] = value

    return modified_content


def generate_language_resource_pack(
    chinese_json: dict[str, str], english_json: dict[str, str], resource_pack_dir: str
) -> None:
    """Generate a Minecraft resource pack with Chinese pinyin and English translations."""
    # Generate the language file
    language_info = _generate_language_file(
        chinese_json=chinese_json, english_json=english_json
    )

    # Make the folder structure for the resource pack
    assets_folder = os.path.join(resource_pack_dir, "assets", "minecraft", "lang")
    os.makedirs(assets_folder, exist_ok=True)
    lang_file_path = os.path.join(assets_folder, "zh_ln.json")
    with open(lang_file_path, "w") as outfile:
        json.dump(language_info, outfile, indent=4, ensure_ascii=False)

    # Step 3: Create the pack.mcmeta file with a custom language
    pack_meta_file = os.path.join(resource_pack_dir, "pack.mcmeta")
    with open(pack_meta_file, "w", encoding="utf-8") as mcmeta_file:
        json.dump(
            {
                "pack": {
                    "pack_format": 34,  # The version number for Minecraft 1.20+
                    "description": "Chinese for learners Resource Pack",
                },
                "language": {
                    "zh_ln": {
                        "name": "Chinese for learners",
                        "region": "中国大陆",
                        "bidirectional": False,
                    }
                },
            },
            mcmeta_file,
            indent=4,
            ensure_ascii=False,
        )
