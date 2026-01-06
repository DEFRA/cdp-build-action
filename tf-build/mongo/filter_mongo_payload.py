"""
Filter MongoDB IAM Users Payload for lambda function

Usage (in GitHub Actions workflow):
    python filter_mongo_payload.py <environment>

Environment variable required:
    GITHUB_WORKSPACE - GitHub Actions workspace directory
"""

import json
import os
import sys
from pathlib import Path


def filter_mongo_services(environment, workspace_dir):
    """
    Filter tenant services to include only protected zone services with MongoDB enabled.
    
    Args:
        environment: The environment name (e.g., 'dev', 'test', 'prod')
        workspace_dir: GitHub Actions workspace directory
    
    Returns:
        Path: Path to the filtered payload file
    """
    # Define paths relative to workspace
    workspace = Path(workspace_dir)
    tenants_dir = workspace / "environments" / environment / "tenants"
    output_file = workspace / "environments" / environment / "filtered_mongo_payload.json"
    
    if not tenants_dir.exists():
        print(f"Error: Tenants directory not found: {tenants_dir}")
        sys.exit(1)
    
    # Read all tenant JSON files
    tenant_files = sorted(tenants_dir.glob("*.json"))
    
    if not tenant_files:
        print(f"Error: No tenant files found in {tenants_dir}")
        sys.exit(1)
    
    print(f"Found {len(tenant_files)} tenant files in {environment} environment")
    
    # Collect filtered services
    filtered_services = {}
    total_services = 0
    filtered_count = 0
    
    for tenant_file in tenant_files:
        try:
            with open(tenant_file, 'r') as f:
                service_config = json.load(f)
            
            service_name = tenant_file.stem
            total_services += 1
            
            # Filter: only protected zone and mongo enabled
            zone = service_config.get("zone")
            mongo = service_config.get("mongo", False)
            
            if zone == "protected" and mongo is True:
                # Extract required fields
                filtered_services[service_name] = {
                    "zone": zone,
                    "mongo": mongo
                }
                filtered_count += 1
                
        except json.JSONDecodeError as e:
            print(f"Warning: Failed to parse {tenant_file.name}: {e}")
            continue
        except Exception as e:
            print(f"Warning: Error processing {tenant_file.name}: {e}")
            continue
    
    # Output in format expected by lambda: [{ service1: {...}, service2: {...} }]
    output_payload = [filtered_services]
    
    # Write filtered payload to output file
    with open(output_file, 'w') as f:
        json.dump(output_payload, f, indent=2)
    
    # Stats
    output_size = output_file.stat().st_size
    print(f"Total services: {total_services}")
    print(f"Filtered services (protected + mongo): {filtered_count}")
    print(f"Services removed: {total_services - filtered_count}")
    print(f"Output file: {output_file}")
    print(f"Output size: {output_size / 1024:.1f} KB")
    
    return output_file


def main():
    """Main entry point for GitHub Actions."""
    if len(sys.argv) != 2:
        print("Usage: python filter_mongo_payload.py <environment>")
        sys.exit(1)
    
    environment = sys.argv[1]
    
    # Get githuub workspace dir
    workspace_dir = os.environ.get('GITHUB_WORKSPACE')
    if not workspace_dir:
        print("Error: GITHUB_WORKSPACE environment variable not set")
        sys.exit(1)
    
    print(f"Filtering MongoDB services for env: {environment}")
    
    output_file = filter_mongo_services(environment, workspace_dir)
    
    # Output file path
    print(f"Filtered payload: {output_file}")


if __name__ == "__main__":
    main()
