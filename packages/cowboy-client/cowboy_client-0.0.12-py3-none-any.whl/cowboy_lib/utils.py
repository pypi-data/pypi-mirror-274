from pathlib import Path
import subprocess
import os
import uuid
import random
import string


def get_current_git_commit(repo_path: Path) -> str:
    """
    Uses subprocess to get the current git commit hash.

    Returns:
        str: The current git commit hash.
    """
    try:
        commit_hash = (
            subprocess.check_output(
                ["cd", str(repo_path.resolve()), "&&", "git", "rev-parse", "HEAD"],
                shell=True,
            )
            .strip()
            .decode("utf-8")
        )
        return commit_hash
    except subprocess.CalledProcessError as e:
        print(f"Error getting current git commit: {e}")
        return ""


def testfiles_in_coverage(base_cov, src_repo) -> bool:
    """
    Check if the test files are accidentally included in the coverage
    """
    for test_file in src_repo.test_files:
        for cov in base_cov.cov_list:
            if cov.filename.split(os.sep)[-1] == test_file.path.name:
                return True
    return False


def generate_id():
    """
    Generates a random UUID
    """
    return str(uuid.uuid4())


def gen_random_name():
    """
    Generates a random name using ASCII, 8 characters in length
    """

    return "".join(random.choices(string.ascii_lowercase, k=8))
