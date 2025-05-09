#!/usr/bin/env python3
"""
update_us_congressional_data.py

Fetch the static legislators-current.csv (via HTTP) into ../cached_data/us/,
cache it for 24 hours (touching its mtime), load into a pandas DataFrame,
build a nested dictionary of senators by state and representatives by district,
and write that dictionary out as JSON.

By default, all fields are kept in the JSON output. Use --keep-fields or --delete-fields
to filter which fields are included in the output.
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union

import pandas as pd
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
)


def get_current_congress_legislators(
    csv_dir: Path = Path(__file__).parent.parent / "cached_data" / "us",
    csv_name: str = "legislators-current.csv",
    url: str = "https://unitedstates.github.io/congress-legislators/legislators-current.csv",
) -> pd.DataFrame:
    """
    Download (if missing or >24 hours old) the legislators-current.csv into csv_dir,
    update its timestamp, then read into a pandas DataFrame and return it.
    """
    csv_dir = csv_dir.resolve()
    csv_dir.mkdir(parents=True, exist_ok=True)
    csv_path = csv_dir / csv_name

    def download():
        logging.info(f"Downloading {url} -> {csv_path}")
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        csv_path.write_bytes(resp.content)
        now_ts = datetime.now().timestamp()
        os.utime(csv_path, (now_ts, now_ts))

    if not csv_path.exists():
        download()
    else:
        mtime = datetime.fromtimestamp(csv_path.stat().st_mtime)
        if datetime.now() - mtime > timedelta(hours=24):
            download()
        else:
            logging.info(f"Using cached {csv_path.name}, last updated {mtime}")

    return pd.read_csv(csv_path)


def filter_fields(
    row: Union[pd.Series, Dict[str, Any]],
    keep_fields: Optional[Set[str]] = None,
    delete_fields: Optional[Set[str]] = None,
) -> Dict[str, Any]:
    """
    Filter fields in a row based on keep_fields or delete_fields.

    Args:
        row: The pandas Series or dictionary to filter
        keep_fields: Set of field names to keep (if specified, only these fields are kept)
        delete_fields: Set of field names to delete (if specified, these fields are deleted)

    Returns:
        Dictionary with filtered fields
    """
    # Convert row to dictionary if it's a Series
    row_dict = row.to_dict() if isinstance(row, pd.Series) else row

    # Apply field filtering based on the specified mode
    if keep_fields:
        # Keep only the specified fields
        return {k: v for k, v in row_dict.items() if k in keep_fields}
    elif delete_fields:
        # Delete the specified fields
        return {k: v for k, v in row_dict.items() if k not in delete_fields}
    else:
        # Keep all fields
        return row_dict


def build_legislators_dict(
    df: pd.DataFrame,
    keep_fields: Optional[Set[str]] = None,
    delete_fields: Optional[Set[str]] = None,
) -> Dict[str, Any]:
    """
    Build a nested dict with two top-level keys:
      - 'states': mapping state code -> {'senators': [<legislator data>]}
      - 'districts': mapping 'ST-D' -> {'representative': <legislator data>}

    Only rows where `district` is NaN are treated as senators. All numeric districts
    (including 0 for at‑large) are treated as House members.

    Args:
        df: DataFrame containing legislator data
        keep_fields: Set of field names to keep (if specified, only these fields are kept)
        delete_fields: Set of field names to delete (if specified, these fields are deleted)

    Returns:
        Dictionary with filtered legislator data organized by state and district
    """
    data = {"states": {}, "districts": {}}

    for _, row in df.iterrows():
        state = row.get("state") or row.get("state_code")
        dist = row.get("district")

        # Filter the row data based on the specified fields
        filtered_data = filter_fields(row, keep_fields, delete_fields)

        if pd.isna(dist):
            # senator: only when district is truly missing
            data["states"].setdefault(state, {}).setdefault("senators", []).append(
                filtered_data
            )
        else:
            # house representative (including at‑large district 0)
            key = f"{state}-{int(dist)}"
            data["districts"][key] = {"representative": filtered_data}

    return data


def setup_argparser() -> argparse.ArgumentParser:
    """Set up and return the argument parser for command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Download and process US congressional legislator data."
    )

    field_group = parser.add_mutually_exclusive_group()
    field_group.add_argument(
        "--keep-fields",
        nargs="+",
        help="List of fields to keep in the output (all others will be removed)",
        metavar="FIELD",
    )
    field_group.add_argument(
        "--delete-fields",
        nargs="+",
        help="List of fields to delete from the output (all others will be kept)",
        metavar="FIELD",
    )

    parser.add_argument(
        "--output",
        help="Custom output file path",
        default=None,
    )

    return parser


if __name__ == "__main__":
    # Parse command line arguments
    parser = setup_argparser()
    args = parser.parse_args()

    # Convert field lists to sets if provided
    keep_fields = set(args.keep_fields) if args.keep_fields else None
    delete_fields = set(args.delete_fields) if args.delete_fields else None

    # Load CSV
    df = get_current_congress_legislators()

    # Get column names for validation
    available_fields = set(df.columns)

    # Validate field names if specified
    if keep_fields and not keep_fields.issubset(available_fields):
        invalid_fields = keep_fields - available_fields
        logging.error(
            f"Invalid field(s) specified in --keep-fields: {', '.join(invalid_fields)}"
        )
        logging.error(f"Available fields: {', '.join(sorted(available_fields))}")
        sys.exit(1)

    if delete_fields and not delete_fields.issubset(available_fields):
        invalid_fields = delete_fields - available_fields
        logging.error(
            f"Invalid field(s) specified in --delete-fields: {', '.join(invalid_fields)}"
        )
        logging.error(f"Available fields: {', '.join(sorted(available_fields))}")
        sys.exit(1)

    # Build nested dict with field filtering
    leg_dict = build_legislators_dict(df, keep_fields, delete_fields)

    # Determine output file path
    if args.output:
        out_path = Path(args.output)
    else:
        out_path = (
            Path(__file__).parent.parent
            / "cached_data"
            / "us"
            / "legislators-lookup.json"
        )

    # Create parent directories if needed
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Write JSON
    logging.info(f"Writing JSON dictionary to {out_path}")
    with open(out_path, "w") as fp:
        json.dump(leg_dict, fp, indent=2)

    # Print summary
    num_states = len(leg_dict["states"])
    num_dists = len(leg_dict["districts"])
    field_info = ""
    if keep_fields:
        field_info = f" (keeping only: {', '.join(sorted(keep_fields))})"
    elif delete_fields:
        field_info = f" (excluding: {', '.join(sorted(delete_fields))})"

    print(
        f"Generated dictionary: {num_states} states, {num_dists} districts written to {out_path}{field_info}"
    )
