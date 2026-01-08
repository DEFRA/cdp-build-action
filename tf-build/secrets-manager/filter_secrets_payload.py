#!/usr/bin/env python3
"""
Filter Secrets Manager Payload for GitHub Actions

Usage (in GitHub Actions workflow):
    python filter_secrets_payload.py <environment>

Environment variable required:
    GITHUB_WORKSPACE - GitHub Actions workspace directory
"""

import json
import os
import sys
from pathlib import Path


def filter_secrets_services(environment, workspace_dir):
    """
    Filter tenant services to include only the zone field.

    Args:
        environment: The environment name (e.g., 'dev', 'test', 'prod')
        workspace_dir: GitHub Actions workspace directory

    Returns:
        Path: Path to the filtered payload file
    """
    workspace = Path(workspace_dir)
    tenants_dir = workspace / "environments" / environment / "tenants"
    output_file = workspace / "environments" / environment / "filtered_secrets_payload.json"

    if not tenants_dir.exists():
        print(f"Error: Tenants directory not found: {tenants_dir}")
        sys.exit(1)

    # Read tenant JSON files
    tenant_files = sorted(tenants_dir.glob("*.json"))

    if not tenant_files:
        print(f"Error: No tenant files found in {tenants_dir}")
        sys.exit(1)

    print(f"Found {len(tenant_files)} tenant files in {environment} environment")

    # Get filtered services
    filtered_services = []
    total_services = 0
    filtered_count = 0

    for tenant_file in tenant_files:
        try:
            with open(tenant_file, 'r') as f:
                service_config = json.load(f)

            service_name = tenant_file.stem
            total_services += 1

            # Extract zone field
            zone = service_config.get("zone")

            if zone:
                filtered_services.append({
                    service_name: {
                        "zone": zone
                    }
                })
                filtered_count += 1

        except json.JSONDecodeError as e:
            print(f"Warning: Failed to parse {tenant_file.name}: {e}")
            continue
        except Exception as e:
            print(f"Warning: Error processing {tenant_file.name}: {e}")
            continue

    # GUARDRAIL 1: Ensure we have at least some services
    if filtered_count == 0:
        print(f"ERROR: No services with 'zone' field found!")
        print(f"Total services processed: {total_services}")
        print(f"This would result in an empty payload - ABORTING")
        sys.exit(1)

    # GUARDRAIL 2: Exit if suspiciously low count
    if filtered_count < 50:
        print(f"WARNING: Only {filtered_count} services with 'zone' field")
        print(f"Expected most/all services to have zone - please verify this is correct")
        sys.exit(1) 

    # output payload
    output_payload = filtered_services

    # GUARDRAIL 3: Validate JSON structure
    try:
        json_str = json.dumps(output_payload)
    except (TypeError, ValueError) as e:
        print(f"ERROR: Output payload is not valid JSON: {e}")
        sys.exit(1)

    # Write filtered payload
    with open(output_file, 'w') as f:
        json.dump(output_payload, f, indent=2)

    # Calculate size
    output_size = output_file.stat().st_size

    # GUARDRAIL 4: Check payload size
    if output_size > 200 * 1024:
        print(f"WARNING: Filtered payload is {output_size / 1024:.1f} KB")
        print(f"Approaching SNS limit of 256KB!")

    print(f"Total services: {total_services}")
    print(f"Filtered services (with zone): {filtered_count}")
    print(f"Output file: {output_file}")
    print(f"Output size: {output_size / 1024:.1f} KB")

    return output_file


def main():
    """Main entry point for GitHub Actions."""
    if len(sys.argv) != 2:
        print("Usage: python filter_secrets_payload.py <environment>")
        sys.exit(1)

    environment = sys.argv[1]

    # Get GitHub workspace dir
    workspace_dir = os.environ.get('GITHUB_WORKSPACE')
    if not workspace_dir:
        print("Error: GITHUB_WORKSPACE environment variable not set")
        sys.exit(1)

    print(f"Filtering Secrets Manager services for environment: {environment}")

    output_file = filter_secrets_services(environment, workspace_dir)

    # Output file path
    print(f"Filtered payload ready: {output_file}")


if __name__ == "__main__":
    main()
