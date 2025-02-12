import json
import logging
import os
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class LanguagePack:
    name: str
    filename: str


NATIVE_LANGUAGE_PACK = LanguagePack("en_us", "minecraft/lang/en_us.json")

OUTPUT_LANGUAGE_PACKS = [
    LanguagePack("zh_cn", "minecraft/lang/zh_cn.json"),
    LanguagePack("zh_hk", "minecraft/lang/zh_hk.json"),
    LanguagePack("zh_tw", "minecraft/lang/zh_tw.json"),
]


def _extract_hashes(file_path: str) -> dict[LanguagePack, str]:
    with open(file_path, "r") as language_file:
        objects = json.load(language_file)["objects"]

    hashes = {}
    for language_file in OUTPUT_LANGUAGE_PACKS:
        language_pack_metadata = objects[language_file.filename]
        hashes[language_file] = str(language_pack_metadata["hash"])

    logging.debug(f"Found language file hashes: {hashes}")
    return hashes


def _extract_hashes_for_language_packs(
    minecraft_folder_path: str,
) -> dict[LanguagePack, str]:
    index_folder = os.path.join(minecraft_folder_path, "assets", "indexes")
    for filename in os.listdir(index_folder):
        try:
            if filename.endswith(".json"):
                file_path = os.path.join(index_folder, filename)
                return _extract_hashes(file_path)
        except Exception as e:
            print(f"Error processing file {filename}", e)
    else:
        raise FileNotFoundError(
            "No file hash metadata was found in any of the indexes."
        )


def _get_file_by_hash(minecraft_folder_path: str, hash: str) -> str:
    folder_path = os.path.join(minecraft_folder_path, "assets", "objects")
    for filename in os.listdir(folder_path):
        if filename.startswith(hash[:2]):
            file_path = os.path.join(folder_path, filename, hash)
            return file_path
    else:
        raise FileNotFoundError(f"Failed to find file with hash {hash}.")


def get_other_language_file_paths(
    minecraft_folder_path: str,
) -> dict[LanguagePack, str]:
    hashes = _extract_hashes_for_language_packs(
        minecraft_folder_path=minecraft_folder_path
    )

    language_file_paths = {}
    for language_file in OUTPUT_LANGUAGE_PACKS:
        hash = hashes[language_file]
        file_path = _get_file_by_hash(minecraft_folder_path, hash)
        logging.debug(f"Found language file {language_file} at {file_path}")
        language_file_paths[language_file] = file_path

    return language_file_paths


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    get_other_language_file_paths(
        os.path.expanduser("~/.local/share/PrismLauncher/assets")
    )
