import json
import zipfile


def _get_file_contents_from_jar(jar_path: str, file_to_print: str) -> str:
    with zipfile.ZipFile(jar_path, "r") as jar:
        if file_to_print in jar.namelist():
            with jar.open(file_to_print) as file:
                return file.read().decode("utf-8")
        else:
            print(f"{file_to_print} not found in the JAR file")


def get_en_us_json_from_jar(jar_path: str) -> dict[str, str]:
    return json.loads(
        _get_file_contents_from_jar(jar_path, "assets/minecraft/lang/en_us.json")
    )
