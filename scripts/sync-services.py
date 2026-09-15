"""Sync domain-only service rules and publish successful MRS outputs."""

import argparse
import json
from pathlib import Path
import subprocess
import tempfile
from urllib.request import urlopen

import yaml


ROOT = Path(__file__).resolve().parents[1]

SERVICES = (
    "Pixiv",
    "LinkedIn",
    "Threads",
)

MAX_UPSTREAM_SIZE = 2_000_000


def domains(payload):
    """Validate and normalize domain-only rules."""
    if not isinstance(payload, list) or not payload:
        raise ValueError("empty or invalid upstream payload")

    result = set()

    for rule in payload:
        parts = rule.split(",") if isinstance(rule, str) else []

        if len(parts) != 2 or parts[0] not in (
            "DOMAIN",
            "DOMAIN-SUFFIX",
        ):
            raise ValueError(
                f"unsupported rule, refusing partial conversion: {rule!r}"
            )

        domain = parts[1].lower()

        if (
            not domain
            or any(
                c not in "abcdefghijklmnopqrstuvwxyz0123456789-."
                for c in domain
            )
            or "." not in domain
        ):
            raise ValueError(f"invalid domain: {domain!r}")

        result.add(
            ("+." if parts[0] == "DOMAIN-SUFFIX" else "") + domain
        )

    return sorted(result)


def service_url(service):
    """Return the upstream rule URL for a service."""
    return (
        "https://raw.githubusercontent.com/"
        f"blackmatrix7/ios_rule_script/master/rule/Clash/"
        f"{service}/{service}.yaml"
    )


def sync_service(
    service,
    additions,
    binary,
    temp,
):
    """Download, validate, convert, and publish one service.

    A failure is raised to the caller so the caller can continue
    with the remaining services.
    """
    url = service_url(service)

    print(f"::group::{service}: syncing")

    try:
        print(f"{service}: downloading upstream rules")

        with urlopen(url, timeout=60) as response:
            source = response.read(MAX_UPSTREAM_SIZE + 1)

        if len(source) > MAX_UPSTREAM_SIZE:
            raise ValueError(
                f"upstream exceeds {MAX_UPSTREAM_SIZE:,} byte limit"
            )

        parsed = yaml.safe_load(source)

        entries = domains(
            parsed.get("payload")
            if isinstance(parsed, dict)
            else None
        )

        extra = additions.get(service, [])

        if extra:
            entries = sorted(
                set(entries + domains(extra))
            )

        filename = service + "_Domain"

        yaml_path = temp / (filename + ".yaml")
        mrs_path = temp / (filename + ".mrs")

        yaml_path.write_text(
            f"# Source: {url}\n"
            "# Author: blackmatrix7; "
            "local additions: Rules/service-additions.json\n"
            + yaml.safe_dump(
                {"payload": entries},
                sort_keys=False,
            ),
            encoding="utf-8",
        )

        print(
            f"{service}: converting "
            f"{len(entries)} domains to MRS"
        )

        subprocess.run(
            [
                binary,
                "convert-ruleset",
                "domain",
                "yaml",
                str(yaml_path),
                str(mrs_path),
            ],
            check=True,
        )

        if not mrs_path.exists():
            raise ValueError(
                "converter did not create MRS output"
            )

        if mrs_path.stat().st_size == 0:
            raise ValueError(
                "converter returned empty MRS"
            )

        destination_yaml = (
            ROOT / "Rules" / yaml_path.name
        )

        destination_mrs = (
            ROOT / "MRS" / mrs_path.name
        )

        destination_yaml.write_bytes(
            yaml_path.read_bytes()
        )

        destination_mrs.write_bytes(
            mrs_path.read_bytes()
        )

        print(
            f"{service}: successfully updated "
            f"{len(entries)} domains"
        )

        return True

    finally:
        print(f"::endgroup::")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--mihomo",
        required=True,
    )

    args = parser.parse_args()

    binary = str(
        Path(args.mihomo).resolve()
    )

    additions_path = (
        ROOT / "Rules" / "service-additions.json"
    )

    try:
        additions = json.loads(
            additions_path.read_text(
                encoding="utf-8"
            )
        )

        if not isinstance(additions, dict):
            raise ValueError(
                "service-additions.json must contain an object"
            )

    except Exception as exc:
        print(
            f"::warning::Unable to load "
            f"service-additions.json: {exc}"
        )
        additions = {}

    successful = []
    failed = []

    with tempfile.TemporaryDirectory() as folder:
        temp = Path(folder)

        for service in SERVICES:
            try:
                sync_service(
                    service=service,
                    additions=additions,
                    binary=binary,
                    temp=temp,
                )

                successful.append(service)

            except Exception as exc:
                failed.append(service)

                print(
                    f"::warning::{service} sync failed: "
                    f"{type(exc).__name__}: {exc}"
                )

                # Continue with the remaining services.
                continue

    print("")
    print("Service synchronization summary:")

    if successful:
        print(
            "  Successful: "
            + ", ".join(successful)
        )
    else:
        print("  Successful: none")

    if failed:
        print(
            "  Failed: "
            + ", ".join(failed)
        )
        print(
            "  Service failures were skipped; "
            "core rule updates can continue."
        )
    else:
        print("  Failed: none")


if __name__ == "__main__":
    main()