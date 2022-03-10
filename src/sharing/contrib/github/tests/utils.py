import base64


def mock_github_repo(name: str, **kwargs) -> dict:
    owner, repo = name.split("/")

    repo_data = {
        "id": 1111,
        "node_id": "qwerty",
        "name": repo,
        "full_name": name,
        "owner": {
            "login": owner,
            "id": 1,
            "node_id": "MDQ6VXNlcjE=",
            "url": f"https://api.github.com/users/{owner}",
        },
        "private": False,
        "html_url": f"https://github.com/{name}",
        "description": "This your first repo!",
        "url": f"https://api.github.com/repos/{name}",
        "default_branch": "master",
        "visibility": "public",
        "pushed_at": "2011-01-26T19:06:43Z",
        "created_at": "2011-01-26T19:01:12Z",
        "updated_at": "2011-01-26T19:14:43Z",
    }

    if kwargs:
        repo_data.update(kwargs)

    return repo_data


def mock_github_file(folder, filename, repo="some/repo", **kwargs) -> dict:
    path = f"{folder}/{filename}"
    file_data = {
        "type": "file",
        "encoding": "base64",
        "size": 5362,
        "name": filename,
        "path": path,
        "content": base64.b64encode(b"example content").decode("utf-8"),
        "url": f"https://api.github.com/repos/{repo}/contents/{path}",
        "html_url": f"https://github.com/{repo}/blob/master/{path}",
        "download_url": f"https://raw.githubusercontent.com/{repo}/master/{path}",
    }
    if kwargs:
        file_data.update(kwargs)

    return file_data


def mock_github_update_file(folder, filename, repo="some/repo", **kwargs) -> dict:
    path = f"{folder}/{filename}"
    data = {
        "content": {
            "type": "file",
            "size": 5362,
            "name": filename,
            "path": path,
            "url": f"https://api.github.com/repos/{repo}/contents/{path}",
            "html_url": f"https://github.com/{repo}/blob/master/{path}",
            "download_url": f"https://raw.githubusercontent.com/{repo}/master/{path}",
        },
        "commit": {
            "sha": "18a43cd8e1e3a79c786e3d808a73d23b6d212b16",
        },
    }
    if kwargs:
        data.update(kwargs)

    return data
