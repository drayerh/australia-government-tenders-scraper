# File: tenders/utils/selector_versioning.py
import git
from pathlib import Path

class SelectorHistory:
    def __init__(self):
        self.repo = git.Repo(Path(__file__).parent.parent)
        self.selector_dir = Path('config/selectors')

    def commit_changes(self, message):
        self.repo.index.add([str(self.selector_dir)])
        self.repo.index.commit(message)

    def rollback(self, commit_hash):
        self.repo.git.checkout(
            commit_hash,
            str(self.selector_dir)
        )