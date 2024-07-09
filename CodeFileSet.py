import os

import requests

from consts import SOURCE_FILE_EXTENSION, GITHUB_TOKEN


class CodeFileSet(object):
    def __init__(self):
        self._paths = None

    def get_file_paths(self):
        return self._paths

    def path_to_code(self, path):
        raise NotImplementedError()

    def get_content(self):
        for path in self._paths:
            yield path, self.path_to_code(path)


class LocalCodeFileSet(CodeFileSet):
    def __init__(self, root_dir_path=None, file_path=None):
        super().__init__()

        if root_dir_path is None and file_path is None:
            raise Exception("No parameters provided for CodeFileSet")

        if file_path is not None:
            self.__root = None
            self._paths = [file_path]
        else:
            self.__root = root_dir_path
            self._paths = []
            for root, _, files in os.walk(self.__root):
                for file in files:
                    if file.endswith(SOURCE_FILE_EXTENSION):
                        self._paths.append(os.path.join(root, file))

    def path_to_code(self, path):
        return open(path).read()


class GithubCodeFileSet(CodeFileSet):
    def __init__(self, github_url=None, file_path=None):
        super().__init__()

        # TODO: code duplication with the previous class
        if github_url is None and file_path is None:
            raise Exception("No parameters provided for CodeFileSet")

        if file_path is not None:
            self.__url = None
            self._paths = [file_path]
        else:
            self.__url = github_url
            self._paths = self.__list_files_in_github_directory()

    def __recursive_get_files(self, url, headers):
        urls = []
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            contents = response.json()
            for item in contents:
                if item['type'] == 'file' and item['name'].endswith(SOURCE_FILE_EXTENSION):
                    urls.append(item['download_url'])
                elif item['type'] == 'dir':
                    urls.extend(self.__recursive_get_files(item['url'], headers))
            return urls
        return None

    def __list_files_in_github_directory(self):
        request_headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github.v3+json',
        }

        # Extract the owner and repo from the URL
        path_parts = self.__url.rstrip('/').split('/')
        owner = path_parts[3]
        repo = path_parts[4]

        dir_path_parts = path_parts[5:]

        while len(dir_path_parts) > 0:
            dir_path = "/".join(dir_path_parts)
            api_url = f'https://api.github.com/repos/{owner}/{repo}/contents/{dir_path}'

            file_urls = self.__recursive_get_files(api_url, request_headers)
            if file_urls is not None:
                return file_urls

            dir_path_parts = dir_path_parts[1:]

        raise Exception(f'Github URL {self.__url} couldn\'t be resolved.')

    @staticmethod
    def __convert_to_raw_url(url):
        if 'github.com' in url and '/blob/' in url:
            # Convert the GitHub URL to the raw content URL
            return url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
        return url

    @staticmethod
    def __fetch_file_content(url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            response.raise_for_status()

    def path_to_code(self, path):
        raw_url = self.__convert_to_raw_url(path)
        try:
            file_content = self.__fetch_file_content(raw_url)
            return file_content
        except requests.exceptions.RequestException as e:
            print(f"Error fetching file: {e}")
