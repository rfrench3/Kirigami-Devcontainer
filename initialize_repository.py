import os
import datetime
from typing import Callable

BASE_PATH: str = os.path.dirname(__file__)


def ensureInRepository() -> None:
    """Refuse to run if outside of intended repository."""
    git_path = os.path.join(BASE_PATH, '.git')
    if not os.path.isdir(git_path):
        print("Error: .git folder not found in repository root")
        exit(1)
    
def inGitIgnore() -> list[str]:
    """return list of entries in the .gitignore, if that file exists."""
    gitignore_path = os.path.join(BASE_PATH, '.gitignore')
    if os.path.isfile(gitignore_path):
        with open(gitignore_path, 'r') as f:
            return [".git", "build"] + f.read().splitlines()
    else:
        return [".git", "build"]

class File:
    def __init__(self, path, new_info: NewInfo):
        self.path = path
        self.name = os.path.basename(path)
        self.new_info = new_info

    def __str__(self) -> str:
        return self.path

    def renameSelf(self):
        """Replace all instances of newproject in the file name with new_info.replaceProject()"""
        new_name = self.name
        for old in self.new_info.OLD_NAMES:
            new_name = new_name.replace(old, self.new_info.replaceProject(old))
        if new_name != self.name:
            new_path = os.path.join(os.path.dirname(self.path), new_name)
            os.rename(self.path, new_path)
            self.path = new_path
            self.name = new_name

    def renameContents(self):
        try:
            with open(self.path, 'r') as f:
                contents = f.read()
        except UnicodeDecodeError:
            print(f"Skipping binary file: {self.name}")
            return

        new_contents = contents
        for old in self.new_info.OLD_NAMES:
            new_contents = new_contents.replace(old, self.new_info.replaceProject(old))
        new_contents = new_contents.replace("%{AUTHOR}", self.new_info.author)
        new_contents = new_contents.replace("%{EMAIL}", self.new_info.email)
        new_contents = new_contents.replace("%{CURRENT_YEAR}", str(datetime.date.today().year))

        if new_contents != contents:
            with open(self.path, 'w') as f:
                f.write(new_contents)

class Dir:
    def __init__(self, base_dir, new_info: NewInfo):
        # self.name = os.path.basename(base_dir)
        self.contents: list = []
        ignored = inGitIgnore()
        for entry in os.scandir(base_dir):
            if entry.name in ignored:
                continue
            elif entry.is_symlink():
                print(f"symlink {entry.name} detected, ignored!")
                continue
            elif entry.is_file():
                self.contents.append(File(entry.path, new_info))
            elif entry.is_dir():
                self.contents.append(Dir(entry.path, new_info))

    def process(self):
        for item in self.contents:
            if isinstance(item, File):
                item.renameContents()
                item.renameSelf()
            elif isinstance(item, Dir):
                item.process()

class NewInfo:
    OLD_NAMES: dict[str, Callable[[str], str]] = {
        "newproject": lambda s: ''.join(c.lower() for c in s if c.isalpha()),
        "NewProject": lambda s: ''.join(c for c in s if c.isalpha()),
        "NEWPROJECT": lambda s: ''.join(c.upper() for c in s if c.isalpha()),
    }

    def __init__(self, display_name: str, author: str, email: str) -> None:
        self.name = display_name
        self.author = author
        self.email = email

    def replaceProject(self, old: str) -> str:
        """Returns the new string to use when passed the old string."""
        if old in self.OLD_NAMES:
            return self.OLD_NAMES[old](self.name)
        else:
            return old
        
def addSelfToGitIgnore():
    """Runs on successful completion of initialization script."""
    gitignore_path = os.path.join(BASE_PATH, '.gitignore')
    if "initialize_repository.py" not in inGitIgnore():
        with open(gitignore_path, 'a') as f:
            f.write("\ninitialize_repository.py\n")


def main():
    print(
        "This initializer script makes it much quicker to go from newproject to a ready-to-go starting template!\n"
        "It is only intended to work on a fully untouched instance of the included newproject template.\n"
        "Only alphabet characters and spaces are supported in the project name!\n"
    )

    project = input("Project name (alphabet and spaces only): ")
    if not all(c.isalpha() or c.isspace() for c in project):
        print("Error: Project name must contain only alphabet characters and spaces.")
        exit(1)

    author = input("Author name: ")
    email = input("Author email: ")

    confirmation_prompt = (
        f"Project name: {project}\n"
        f"Author name: {author}\n"
        f"Email: {email}\n"
        "Proceed? (Y/n) "
    )
    if input(confirmation_prompt) in ["y", "Y"]:
        new_info = NewInfo(project, author, email)
        root = Dir(BASE_PATH, new_info)
        root.process()
        print("Done!")
        addSelfToGitIgnore()
    else:
        print("Cancelled.")

if __name__ == '__main__':
    ensureInRepository()
    if "initialize_repository.py" in inGitIgnore():
        print("The initializer has already been used, and cannot be used again.")
        exit(1)
    main()
