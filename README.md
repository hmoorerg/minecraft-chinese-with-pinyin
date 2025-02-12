# Minecraft Chinese with Pinyin Language Pack
This project generates a Mandarin Chinese language pack with both English and pinyin to help you learn Mandarin.

![image](https://github.com/user-attachments/assets/6ad92979-f827-43bb-88ca-e2fcc7e4c048)

# Why?
It is useful for language learners who want to learn new words in Mandarin Chinese while playing Minecraft. Pinyin teaches pronunciation while the English translation teaches the meaning.

# Is there a direct download available for this language pack?
Not at the moment due to these reasons:
- The language pack is created using the game's official Chinese and English language files which are not contained in this repo.
- Any downloads might go out-of-date when a new version of Minecraft is released unless I set up a pipeline. That's overkill for now unless this repo is used by more users.
- Learning Chinese is already hard so setting up a python project is the least of our worries :(

# How do I generate the language pack?
## Option 1: Pipenv
1. Install the dependencies using `pipenv install`.
2. Use `pipenv run python main.py` to run the project.

## Option 2: Global python install
1. Just install `pypinyin` using pip since that is currently the only dependency.
2. Run `python main.py`.

Once you've completed either of these steps, a `output_folder` folder should appear in the project directory that contains all of the generated language pack. Pick the one with the locale that you prefer and drag it into the Minecraft resource pack folder.

# Possible future features:
- More native language options other than American English. For example: a native Spanish speaker could generate a language pack that displays Both Chinese and Spanish.
- More language learning options other than Mandarin Chinese. Potentially all Minecraft languages could be supported (after removing the pinyin output).
- A custom format option. This would allow you to hide Pinyin or English to make the text shorter.
- The resource pack could be autoinstalled.
