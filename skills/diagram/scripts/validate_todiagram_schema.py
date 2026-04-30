#!/usr/bin/env python3
"""Validate .todiagram JSON against the live schema plus strict canonical checks.

Usage:
  python scripts/validate_todiagram_schema.py diagram.json
  python scripts/validate_todiagram_schema.py a.json b.json --schema-only
  python scripts/validate_todiagram_schema.py diagram.json --schema-file /path/schema.json
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.request import urlopen


DEFAULT_SCHEMA_URL = "https://todiagram.com/schemas/todiagram.json"
ALLOWED_DIRECTIONS = {"RIGHT", "LEFT", "UP", "DOWN"}


@dataclass
class Issue:
  path: list[Any]
  code: str
  message: str


def _json_pointer(path: list[Any]) -> str:
  if not path:
    return "$"
  escaped: list[str] = []
  for part in path:
    part_str = str(part).replace("~", "~0").replace("/", "~1")
    escaped.append(part_str)
  return "$/" + "/".join(escaped)


def _load_json_file(path: Path) -> Any:
  with path.open("r", encoding="utf-8") as f:
    return json.load(f)


def _load_schema(schema_url: str, schema_file: str | None, timeout: int) -> dict[str, Any]:
  if schema_file:
    data = _load_json_file(Path(schema_file))
    if not isinstance(data, dict):
      raise ValueError("Schema file must contain a top-level JSON object")
    return data

  try:
    with urlopen(schema_url, timeout=timeout) as response:
      raw = response.read().decode("utf-8")
  except URLError as exc:
    curl_bin = shutil.which("curl")
    if not curl_bin:
      raise RuntimeError(f"Failed to fetch schema from {schema_url}: {exc}") from exc

    try:
      curl = subprocess.run(
        [curl_bin, "-fsSL", schema_url],
        check=True,
        capture_output=True,
        text=True,
      )
      raw = curl.stdout
    except subprocess.CalledProcessError as curl_exc:
      raise RuntimeError(
        f"Failed to fetch schema from {schema_url} via urllib ({exc}) and curl ({curl_exc})"
      ) from curl_exc

  data = json.loads(raw)
  if not isinstance(data, dict):
    raise ValueError("Downloaded schema is not a top-level JSON object")
  return data


def _validate_with_jsonschema(instance: Any, schema: dict[str, Any]) -> list[Issue]:
  try:
    from jsonschema import FormatChecker
    from jsonschema.validators import validator_for
  except ModuleNotFoundError as exc:
    raise RuntimeError(
      "Missing dependency: jsonschema. Install with:\n"
      "  python3 -m pip install --user jsonschema"
    ) from exc

  validator_cls = validator_for(schema)
  validator_cls.check_schema(schema)
  validator = validator_cls(schema, format_checker=FormatChecker())
  errors = sorted(validator.iter_errors(instance), key=lambda err: list(err.path))
  return [Issue(path=list(err.path), code="schema", message=err.message) for err in errors]


def _validate_strict_canonical(diagram: Any) -> list[Issue]:
  issues: list[Issue] = []
  ids_seen: dict[str, list[Any]] = {}

  if not isinstance(diagram, dict):
    return [Issue(path=[], code="canonical.type", message="Top-level value must be an object")]

  direction = diagram.get("direction")
  if direction is not None and direction not in ALLOWED_DIRECTIONS:
    issues.append(
      Issue(
        path=["direction"],
        code="canonical.direction",
        message="direction should be one of RIGHT, LEFT, UP, DOWN",
      )
    )

  def walk_node(node: Any, path: list[Any]) -> None:
    if not isinstance(node, dict):
      issues.append(Issue(path=path, code="canonical.node_type", message="Node must be an object"))
      return

    if "children" in node:
      issues.append(
        Issue(
          path=path + ["children"],
          code="canonical.children_alias",
          message="Use `nodes`, not `children`",
        )
      )

    if "imageUrl" in node and "fields" in node:
      issues.append(
        Issue(
          path=path + ["fields"],
          code="canonical.image_fields_conflict",
          message="`imageUrl` cannot be combined with `fields` (image replaces row display)",
        )
      )

    if "imageUrl" in node and node.get("imageUrl") is None:
      issues.append(
        Issue(
          path=path + ["imageUrl"],
          code="canonical.null_image",
          message="Omit `imageUrl` when unused; do not set null",
        )
      )

    if "iconUrl" in node and node.get("iconUrl") is None:
      issues.append(
        Issue(
          path=path + ["iconUrl"],
          code="canonical.null_icon",
          message="Omit `iconUrl` when unused; do not set null",
        )
      )

    node_id = node.get("id")
    if isinstance(node_id, str):
      first_path = ids_seen.get(node_id)
      if first_path is None:
        ids_seen[node_id] = path + ["id"]
      else:
        issues.append(
          Issue(
            path=path + ["id"],
            code="canonical.duplicate_id",
            message=f"Duplicate node id `{node_id}` (first seen at {_json_pointer(first_path)})",
          )
        )

    child_nodes = node.get("nodes")
    if child_nodes is not None:
      if not isinstance(child_nodes, list):
        issues.append(
          Issue(
            path=path + ["nodes"],
            code="canonical.nodes_type",
            message="`nodes` must be an array when present",
          )
        )
      elif len(child_nodes) == 0:
        issues.append(
          Issue(
            path=path + ["nodes"],
            code="canonical.empty_nodes",
            message="Omit `nodes` on leaf nodes instead of using an empty array",
          )
        )
      else:
        for index, child in enumerate(child_nodes):
          walk_node(child, path + ["nodes", index])

  nodes = diagram.get("nodes")
  if isinstance(nodes, list):
    for index, node in enumerate(nodes):
      walk_node(node, ["nodes", index])

  edges = diagram.get("edges")
  if isinstance(edges, list):
    for index, edge in enumerate(edges):
      if not isinstance(edge, dict):
        issues.append(
          Issue(path=["edges", index], code="canonical.edge_type", message="Edge must be an object")
        )
        continue

      if "source" in edge:
        issues.append(
          Issue(
            path=["edges", index, "source"],
            code="canonical.source_alias",
            message="Use `from`, not `source`",
          )
        )
      if "target" in edge:
        issues.append(
          Issue(
            path=["edges", index, "target"],
            code="canonical.target_alias",
            message="Use `to`, not `target`",
          )
        )

      edge_from = edge.get("from")
      edge_to = edge.get("to")
      if isinstance(edge_from, str) and edge_from not in ids_seen:
        issues.append(
          Issue(
            path=["edges", index, "from"],
            code="canonical.unknown_from",
            message=f"`from` references unknown node id `{edge_from}`",
          )
        )
      if isinstance(edge_to, str) and edge_to not in ids_seen:
        issues.append(
          Issue(
            path=["edges", index, "to"],
            code="canonical.unknown_to",
            message=f"`to` references unknown node id `{edge_to}`",
          )
        )

  return issues


def validate_file(
  file_path: Path,
  schema: dict[str, Any],
  schema_only: bool,
) -> tuple[bool, list[Issue]]:
  try:
    diagram = _load_json_file(file_path)
  except FileNotFoundError:
    return False, [Issue(path=[], code="io.not_found", message=f"File not found: {file_path}")]
  except json.JSONDecodeError as exc:
    return False, [
      Issue(
        path=[],
        code="json.parse",
        message=f"Invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}",
      )
    ]
  except OSError as exc:
    return False, [Issue(path=[], code="io.read", message=f"Unable to read file: {exc}")]

  issues: list[Issue] = []
  issues.extend(_validate_with_jsonschema(diagram, schema))
  if not schema_only:
    issues.extend(_validate_strict_canonical(diagram))

  return len(issues) == 0, issues


def main() -> int:
  parser = argparse.ArgumentParser(
    description="Validate ToDiagram JSON files against official schema and strict canonical rules."
  )
  parser.add_argument("files", nargs="+", help="One or more .json/.todiagram files to validate")
  parser.add_argument(
    "--schema-url",
    default=DEFAULT_SCHEMA_URL,
    help=f"Remote schema URL (default: {DEFAULT_SCHEMA_URL})",
  )
  parser.add_argument(
    "--schema-file",
    default=None,
    help="Use local schema file instead of downloading from --schema-url",
  )
  parser.add_argument(
    "--schema-only",
    action="store_true",
    help="Validate only against JSON Schema (skip strict canonical lint checks)",
  )
  parser.add_argument(
    "--timeout",
    type=int,
    default=10,
    help="HTTP timeout in seconds when downloading schema (default: 10)",
  )
  args = parser.parse_args()

  try:
    schema = _load_schema(args.schema_url, args.schema_file, args.timeout)
  except Exception as exc:  # noqa: BLE001
    print(f"ERROR: {exc}", file=sys.stderr)
    return 2

  any_failed = False
  for raw_file in args.files:
    file_path = Path(raw_file)
    ok, issues = validate_file(file_path, schema=schema, schema_only=args.schema_only)
    if ok:
      print(f"PASS {file_path}")
      continue

    any_failed = True
    print(f"FAIL {file_path} ({len(issues)} issue{'s' if len(issues) != 1 else ''})")
    for issue in issues:
      print(f"  - [{issue.code}] {_json_pointer(issue.path)}: {issue.message}")

  return 1 if any_failed else 0


if __name__ == "__main__":
  raise SystemExit(main())
