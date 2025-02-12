import glob
import json
import os
import re

from src.asset_db_parser import get_other_language_file_paths
from src.en_us_extracter import get_en_us_json_from_jar
from src.resource_pack_generator import generate_language_resource_pack


def get_latest_minecraft_jar_path(base_path: str) -> str:
    base_path = os.path.expanduser(base_path)
    jar_files = glob.glob(
        os.path.join(
            base_path, "libraries/com/mojang/minecraft/*/minecraft-*-client.jar"
        )
    )
    if not jar_files:
        raise FileNotFoundError("No Minecraft JAR files found in the specified path.")

    def extract_version(jar_path: str) -> str:
        match = re.search(r"minecraft-(\d+\.\d+\.\d+)-client\.jar", jar_path)
        if match:
            return match.group(1)
        else:
            raise ValueError(f"Failed to extract version from {jar_path}")

    latest_jar = max(jar_files, key=extract_version)
    return latest_jar


def main():
    # Search for the correct `.minecraft` directory for this installation
    for minecraft_path in [
        # PrimsLauncher
        "~/.local/share/PrismLauncher",
        # Vanilla Launcher
        "~/.minecraft",
        # Flatpak Launcher
        "~/.var/app/com.mojang.Minecraft/.minecraft",
        # Windows Launcher
        os.path.join(os.getenv("APPDATA", ""), ".minecraft"),
        # Mac Launcher
        "~/Library/Application Support/minecraft",
    ]:
        minecraft_path = os.path.expanduser(minecraft_path)
        if os.path.exists(minecraft_path):
            english_language_pack = get_en_us_json_from_jar(
                jar_path=get_latest_minecraft_jar_path(minecraft_path)
            )

            other_language_paths = get_other_language_file_paths(minecraft_path)
            break
    else:
        raise FileNotFoundError(
            "None of the specified paths for the `.minecraft` directory exist."
        )

    for language_pack, language_file_path in other_language_paths.items():
        with open(language_file_path, "r") as file:
            chinese_language_pack = json.load(file)

        language_pack_output_dir = (
            f"output_folder/pinyin_resource_pack_{language_pack.name}"
        )
        generate_language_resource_pack(
            chinese_json=chinese_language_pack,
            english_json=english_language_pack,
            resource_pack_dir=language_pack_output_dir,
        )
        print(
            "Generated resource pack for",
            language_pack.name,
            "at",
            language_pack_output_dir,
        )


if __name__ == "__main__":
    main()
