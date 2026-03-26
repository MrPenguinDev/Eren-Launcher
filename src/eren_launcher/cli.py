from __future__ import annotations

import argparse
import os
from pathlib import Path

from .auth import SessionStore
from .bedrock import BedrockProfile, BedrockProfileStore
from .downloader import ArtifactDownloader
from .gui import LauncherGUI
from .java_manager import detect_platform, download_java_runtime, fetch_release_catalog
from .instance_store import InstanceStore
from .launch import LaunchContext, build_java_launch_command
from .manifest import fetch_versions
from .microsoft_oauth import MicrosoftOAuthDeviceFlow
from .models import InstanceConfig
from .process_runner import LaunchProcessRunner
from .providers import CurseForgeProvider, ModrinthProvider
from .runtime import detect_java_runtime


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Eren Launcher (legal MVP)")
    parser.add_argument("--root", default=".eren_launcher", help="Launcher data root")

    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create-instance", help="Create a Java instance config")
    create.add_argument("name")
    create.add_argument("--version", required=True)
    create.add_argument("--loader", default="vanilla")
    create.add_argument("--min-memory", type=int, default=1024)
    create.add_argument("--max-memory", type=int, default=4096)

    sub.add_parser("list-instances", help="List configured instances")

    versions = sub.add_parser("list-versions", help="List latest Minecraft versions")
    versions.add_argument("--limit", type=int, default=15)

    launch = sub.add_parser("build-launch", help="Build Java launch command")
    launch.add_argument("name")
    launch.add_argument("--session", required=True, help="Stored session name")

    launch_exec = sub.add_parser("run-launch", help="Run Java launch command and persist structured logs")
    launch_exec.add_argument("name")
    launch_exec.add_argument("--session", required=True, help="Stored session name")

    login = sub.add_parser("save-session", help="Save authenticated account session")
    login.add_argument("name")
    login.add_argument("--username", required=True)
    login.add_argument("--uuid", required=True)
    login.add_argument("--access-token", required=True)
    login.add_argument("--ownership-verified", action="store_true", required=False)

    oauth = sub.add_parser("oauth-device-start", help="Start Microsoft OAuth device flow")
    oauth.add_argument("--client-id", required=True)
    oauth.add_argument("--scope", default="XboxLive.signin offline_access")

    java = sub.add_parser("check-java", help="Detect Java runtime")
    java.add_argument("--java", default="java")

    search = sub.add_parser("search-modrinth", help="Search Modrinth projects")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=10)

    curse = sub.add_parser("search-curseforge", help="Search CurseForge projects")
    curse.add_argument("query")
    curse.add_argument("--limit", type=int, default=10)
    curse.add_argument("--api-key", default="")

    download = sub.add_parser("download-artifact", help="Download file with optional SHA1 check")
    download.add_argument("url")
    download.add_argument("--sha1", default="")

    bedrock = sub.add_parser("save-bedrock-profile", help="Save a Bedrock addon profile")
    bedrock.add_argument("name")
    bedrock.add_argument("packs", nargs="*", default=[])

    sub.add_parser("java-releases", help="List available Temurin Java feature releases")

    java_dl = sub.add_parser("download-java", help="Download a Java runtime archive from Temurin")
    java_dl.add_argument("--major", type=int, required=True)
    java_dl.add_argument("--os", default="")
    java_dl.add_argument("--arch", default="")

    sub.add_parser("gui", help="Run XMCL-style desktop GUI")

    return parser


def main() -> None:
    args = _parser().parse_args()
    root = Path(args.root)
    store = InstanceStore(root)
    session_store = SessionStore(root / "sessions")
    bedrock_store = BedrockProfileStore(root / "bedrock_profiles")
    runner = LaunchProcessRunner(root / "logs")
    downloader = ArtifactDownloader(root / "cache")

    if args.command == "create-instance":
        config = InstanceConfig(
            name=args.name,
            minecraft_version=args.version,
            loader=args.loader,
            min_memory_mb=args.min_memory,
            max_memory_mb=args.max_memory,
        )
        path = store.save(config)
        print(f"Instance created: {path}")
        return

    if args.command == "list-instances":
        for instance_name in store.list_instances():
            print(instance_name)
        return

    if args.command == "list-versions":
        for version in fetch_versions(args.limit):
            print(f"{version.version_id}\t{version.type}\t{version.release_time}")
        return

    if args.command == "save-session":
        path = session_store.save(
            args.name,
            LaunchContext(
                username=args.username,
                uuid=args.uuid,
                access_token=args.access_token,
                ownership_verified=args.ownership_verified,
            ).to_account_session(),
        )
        print(f"Session saved: {path}")
        return

    if args.command == "build-launch":
        config = store.load(args.name)
        session = session_store.load(args.session)
        context = LaunchContext.from_account_session(session)
        command = build_java_launch_command(config, context)
        print(" ".join(command))
        return

    if args.command == "run-launch":
        config = store.load(args.name)
        session = session_store.load(args.session)
        context = LaunchContext.from_account_session(session)
        command = build_java_launch_command(config, context)
        exit_code = runner.run(command, args.name)
        print(f"Launch exited with code {exit_code}")
        return

    if args.command == "oauth-device-start":
        flow = MicrosoftOAuthDeviceFlow(client_id=args.client_id, scope=args.scope)
        device = flow.request_device_code()
        print(device.message or f"Visit {device.verification_uri} and enter {device.user_code}")
        return

    if args.command == "check-java":
        info = detect_java_runtime(args.java)
        print(f"{info.executable}\tmajor={info.major}\traw={info.raw_version}")
        return

    if args.command == "search-modrinth":
        provider = ModrinthProvider()
        for item in provider.search(args.query, args.limit):
            print(f"{item.project_id}\t{item.slug}\t{item.title}")
        return

    if args.command == "search-curseforge":
        api_key = args.api_key or os.environ.get("CURSEFORGE_API_KEY", "")
        provider = CurseForgeProvider(api_key=api_key)
        for item in provider.search(args.query, args.limit):
            print(f"{item.project_id}\t{item.slug}\t{item.title}")
        return

    if args.command == "download-artifact":
        result = downloader.download(args.url, args.sha1 or None)
        print(result)
        return

    if args.command == "save-bedrock-profile":
        path = bedrock_store.save(BedrockProfile(name=args.name, packs=args.packs))
        print(f"Bedrock profile saved: {path}")
        return

    if args.command == "java-releases":
        try:
            catalog = fetch_release_catalog()
        except Exception as exc:
            raise RuntimeError(f"Failed to fetch Java releases: {exc}")
        print(f"Available: {catalog.available_releases}")
        print(f"LTS: {catalog.available_lts_releases}")
        print(f"Most recent feature: {catalog.most_recent_feature_release}")
        return

    if args.command == "download-java":
        os_name, arch = detect_platform()
        if args.os:
            os_name = args.os
        if args.arch:
            arch = args.arch
        try:
            output = download_java_runtime(root / "java", major=args.major, os_name=os_name, arch=arch)
        except Exception as exc:
            raise RuntimeError(f"Failed to download Java runtime: {exc}")
        print(output)
        return

    if args.command == "gui":
        LauncherGUI(root).run()
        return


if __name__ == "__main__":
    main()
