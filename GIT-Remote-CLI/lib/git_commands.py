from __future__ import annotations

import subprocess
from urllib.parse import urlparse, urlunparse


class GitCommands:
    """Reusable helper class for common remote Git operations."""

    def __init__(
        self,
        remote_name: str,
        remote_url: str,
        default_branch: str = "main",
        access_token: str = "",
        use_token_auth: bool = False,
        git_executable: str = "git",
    ) -> None:
        self.remote_name = remote_name
        self.remote_url = remote_url
        self.default_branch = default_branch
        self.access_token = access_token
        self.use_token_auth = use_token_auth
        self.git_executable = git_executable

    def _run(self, args: list[str]) -> int:
        cmd = [self.git_executable, *args]
        print(f"$ {' '.join(cmd)}")
        result = subprocess.run(cmd, check=False)
        return result.returncode

    def _remote_url_with_token(self) -> str:
        if not self.access_token or not self.remote_url.startswith(("http://", "https://")):
            return self.remote_url

        parsed = urlparse(self.remote_url)
        netloc = f"oauth2:{self.access_token}@{parsed.netloc}"
        return urlunparse((parsed.scheme, netloc, parsed.path, parsed.params, parsed.query, parsed.fragment))

    def resolved_remote_url(self) -> str:
        if self.use_token_auth:
            return self._remote_url_with_token()
        return self.remote_url

    def list_remotes(self) -> int:
        return self._run(["remote", "-v"])

    def set_remote(self) -> int:
        target_url = self.resolved_remote_url()
        return self._run(["remote", "set-url", self.remote_name, target_url])

    def fetch(self) -> int:
        return self._run(["fetch", self.remote_name])

    def pull(self, branch: str | None = None) -> int:
        target_branch = branch or self.default_branch
        return self._run(["pull", self.remote_name, target_branch])

    def push(self, branch: str | None = None) -> int:
        target_branch = branch or self.default_branch
        return self._run(["push", self.remote_name, target_branch])
