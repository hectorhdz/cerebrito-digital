from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from lib.git_commands import GitCommands


def load_config(config_path: Path) -> dict:
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_client(config: dict) -> GitCommands:
    repo_cfg = config.get("repo", {})
    auth_cfg = config.get("auth", {})
    git_cfg = config.get("git", {})

    token_env_name = auth_cfg.get("access_token_env", "GITLAB_TOKEN")
    env_token = os.getenv(token_env_name, "")
    cfg_token = auth_cfg.get("access_token", "")
    token = env_token or cfg_token

    return GitCommands(
        remote_name=repo_cfg.get("remote_name", "origin"),
        remote_url=repo_cfg.get("remote_url", ""),
        default_branch=repo_cfg.get("default_branch", "main"),
        access_token=token,
        use_token_auth=auth_cfg.get("use_token_auth", False),
        git_executable=git_cfg.get("executable", "git"),
    )


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Config-driven Git remote CLI")
    p.add_argument(
        "--config",
        default="cfg/config.json",
        help="Path to config JSON (default: cfg/config.json)",
    )

    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("list-remotes", help="Show configured remotes")
    sub.add_parser("set-remote", help="Set remote URL from config")
    sub.add_parser("fetch", help="Fetch from configured remote")

    pull_p = sub.add_parser("pull", help="Pull from configured remote")
    pull_p.add_argument("--branch", default=None, help="Override branch")

    push_p = sub.add_parser("push", help="Push to configured remote")
    push_p.add_argument("--branch", default=None, help="Override branch")

    return p


def main() -> int:
    args = parser().parse_args()
    config_path = Path(args.config)

    if not config_path.exists():
        print(f"Config file not found: {config_path}")
        return 1

    config = load_config(config_path)
    client = build_client(config)

    if args.command == "list-remotes":
        return client.list_remotes()
    if args.command == "set-remote":
        return client.set_remote()
    if args.command == "fetch":
        return client.fetch()
    if args.command == "pull":
        return client.pull(branch=args.branch)
    if args.command == "push":
        return client.push(branch=args.branch)

    return 2


if __name__ == "__main__":
    sys.exit(main())
