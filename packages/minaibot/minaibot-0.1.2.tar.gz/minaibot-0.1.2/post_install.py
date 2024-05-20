import os
import shutil


def create_directories_and_files():
    source_bot_dir = os.path.join(os.path.dirname(__file__), 'minaibot', 'bot')
    target_bot_dir = os.path.join(os.getcwd(), 'bot')

    if not os.path.exists(target_bot_dir):
        os.makedirs(target_bot_dir)

    for item in os.listdir(source_bot_dir):
        s = os.path.join(source_bot_dir, item)
        d = os.path.join(target_bot_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)


if __name__ == "__main__":
    create_directories_and_files()
