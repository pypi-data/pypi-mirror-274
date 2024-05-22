import os
from pathlib import Path
import streamlit as st
import importlib
import importlib.metadata
import toml
import git


def load_project_toml():
    try:
        pyproject_toml = Path(os.curdir) / "pyproject.toml"
        if not pyproject_toml.exists():
            return None
        with open(pyproject_toml) as f:
            data = toml.load(f)
            return data
    except BaseException:
        return None


def get_version():
    try:
        return importlib.metadata.version("vizkit")
    except importlib.metadata.PackageNotFoundError:
        config = load_project_toml()
        if config:
            version = config.get("tool", {}).get("poetry", {}).get("version")
            if version is not None:
                return version
        return None


def get_git_hash():
    config = load_project_toml()
    if not config:
        return None
    name = config.get("tool", {}).get("poetry", {}).get("name")
    if name != "vizkit":
        return None
    try:
        git_repo = git.Repo(path=Path(os.curdir))
        return git_repo.head.commit.hexsha
    except git.InvalidGitRepositoryError:
        # This is probably running on Heroku.
        return os.environ.get("HEROKU_BUILD_COMMIT", None)


def get_version_string():
    if "__version__" in st.session_state:
        return st.session_state["__version__"]
    ver = get_version()
    commit = get_git_hash()
    if commit:
        commit_with_link = f'<a href="https://github.com/wenyuzhao/vizkit/commit/{commit}">git-{commit[:7]}</a>'
    else:
        commit_with_link = ""
    if ver:
        ver_with_link = f'<a href="https://pypi.org/project/vizkit/{ver}/">{ver}</a>'
    else:
        ver_with_link = ""
    if ver and commit:
        result = f"Ver. {ver_with_link} ({commit_with_link})"
    elif commit:
        result = f"Ver. {commit_with_link}"
    elif ver:
        result = f"Ver. {ver_with_link}"
    else:
        result = "Ver. <unknown>"
    st.session_state["__version__"] = result
    return result


def footer():
    ver = get_version_string()
    st.html(
        f"""
            <style>
                footer {{
                    color: grey;
                }}
                footer a {{
                    color: grey;
                }}
                footer > a, footer > span {{
                    margin: 1rem;
                }}
                footer a:visited {{
                    color: grey;
                }}
                footer a:hover {{
                    color:rgb(255, 75, 75);
                }}


            </style>
            <footer style="display:flex;flex-direction:row;justify-content:center;align-items:center">
                <div style="flex:1;height: 0.5px; background: grey"></div>
                <span>{ver}</span>
                •
                <span><a href="https://github.com/wenyuzhao/vizkit/blob/main/README.md">Documentation</a></span>
                •
                <span><a href="https://github.com/wenyuzhao/harness">Harness Bench</a></span>
                <div style="flex:1;height: 0.5px; background: grey"></div>
            </footer>
        """
    )  # type: ignore
    # pass
