"""This module only contains the pyemmo package version"""
# /!\ Increase the number before a release
# See https://www.python.org/dev/peps/pep-0440/
# Examples :
# First alpha of the release 0.1.0 : 0.1.0a1
# First beta of the release 1.0.0 : 1.0.0b1
# Second release candidate of the release 2.6.4 : 2.6.4rc2
# Release 1.1.0 : 1.1.0
# First post release of the release 1.1.0 : 1.1.0.post1
try:
    import git
except ModuleNotFoundError:
    sha = ""
else:
    from git import InvalidGitRepositoryError
    try:
        repo = git.Repo(search_parent_directories=True)
        sha = repo.head.object.hexsha
    except InvalidGitRepositoryError:
        sha = "Repo not found"

__version__ = "1.2.10"
