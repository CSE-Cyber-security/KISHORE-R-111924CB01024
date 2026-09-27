"""
Cybersecurity Asset Inventory System
Weekly Mini Project - 01

A menu-driven Python application for adding, displaying, searching,
updating and deleting IT assets while classifying risk and security status.
"""

import json
import ipaddress
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "assets.json"

ASSET_TYPES = ("Workstation", "Server", "Router", "Switch", "Application")
RISK_LEVELS = ("Low", "Medium", "High", "Critical")
SECURITY_STATUSES = ("Secure", "Warning", "Vulnerable")


def load_assets():
    """Load assets from JSON storage."""
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_assets(assets):
    """Persist assets to JSON storage."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(assets, file, indent=4)


def validate_choice(value, choices, field_name):
    """Validate a categorical field."""
    value = value.strip()
    if value not in choices:
        raise ValueError(
            f"{field_name} must be one of: {', '.join(choices)}"
        )
    return value


def validate_ip(value):
    """Validate an IPv4/IPv6 address."""
    value = value.strip()
    try:
        ipaddress.ip_address(value)
    except ValueError as exc:
        raise ValueError("IP Address is invalid.") from exc
    return value


def validate_required(value, field_name):
    value = value.strip()
    if not value:
        raise ValueError(f"{field_name} cannot be empty.")
    return value


def display_assets(assets):
    """Display assets in the required report format."""
    print("\n" + "=" * 41)
    print("  CYBERSECURITY ASSET INVENTORY")
    print("=" * 41)

    if not assets:
        print("No assets found.")
    else:
        for asset in assets:
            print(f"Asset ID : {asset['asset_id']}")
            print(f"Asset Name : {asset['asset_name']}")
            print(f"Asset Type : {asset['asset_type']}")
            print(f"IP Address : {asset['ip_address']}")
            print(f"OS : {asset['operating_system']}")
            print(f"Department : {asset['department']}")
            print(f"Risk Level : {asset['risk_level']}")
            print(f"Status : {asset['security_status']}")
            print("-" * 41)

    print(f"Total Assets : {len(assets)}")
    print(f"Critical Assets : {sum(a['risk_level'] == 'Critical' for a in assets)}")
    print(f"High Risk Assets : {sum(a['risk_level'] == 'High' for a in assets)}")
    print(f"Medium Risk Assets : {sum(a['risk_level'] == 'Medium' for a in assets)}")
    print(f"Vulnerable Assets : {sum(a['security_status'] == 'Vulnerable' for a in assets)}")
    print("=" * 41)


def add_asset(assets, asset=None):
    """Add an asset after validation."""
    if asset is None:
        asset = {
            "asset_id": validate_required(input("Asset ID: "), "Asset ID"),
            "asset_name": validate_required(input("Asset Name: "), "Asset Name"),
            "asset_type": validate_choice(input("Asset Type: "), ASSET_TYPES, "Asset Type"),
            "ip_address": validate_ip(input("IP Address: ")),
            "operating_system": validate_required(
                input("Operating System: "), "Operating System"
            ),
            "department": validate_required(
                input("Owner/Department: "), "Owner/Department"
            ),
            "risk_level": validate_choice(input("Risk Level: "), RISK_LEVELS, "Risk Level"),
            "security_status": validate_choice(
                input("Security Status: "), SECURITY_STATUSES, "Security Status"
            ),
        }

    if any(a["asset_id"].lower() == asset["asset_id"].lower() for a in assets):
        raise ValueError("Asset ID already exists.")

    assets.append(asset)
    save_assets(assets)


def search_assets(assets, query):
    """Search by Asset ID, Asset Name, IP Address, or Department."""
    query = query.strip().lower()
    return [
        asset for asset in assets
        if any(
            query in str(asset[key]).lower()
            for key in ("asset_id", "asset_name", "ip_address", "department")
        )
    ]


def update_asset(assets, asset_id):
    """Update an existing asset. Blank input keeps the current value."""
    for asset in assets:
        if asset["asset_id"].lower() == asset_id.strip().lower():
            print("Press Enter to keep the current value.")
            fields = [
                ("asset_name", "Asset Name", None),
                ("asset_type", "Asset Type", ASSET_TYPES),
                ("ip_address", "IP Address", "ip"),
                ("operating_system", "Operating System", None),
                ("department", "Owner/Department", None),
                ("risk_level", "Risk Level", RISK_LEVELS),
                ("security_status", "Security Status", SECURITY_STATUSES),
            ]

            for key, label, validator in fields:
                current = asset[key]
                value = input(f"{label} [{current}]: ").strip()
                if not value:
                    continue
                if validator == "ip":
                    value = validate_ip(value)
                elif isinstance(validator, tuple):
                    value = validate_choice(value, validator, label)
                else:
                    value = validate_required(value, label)
                asset[key] = value

            save_assets(assets)
            return True

    return False


def delete_asset(assets, asset_id):
    """Delete an asset by Asset ID."""
    original_count = len(assets)
    assets[:] = [
        asset for asset in assets
        if asset["asset_id"].lower() != asset_id.strip().lower()
    ]
    if len(assets) == original_count:
        return False
    save_assets(assets)
    return True


def print_menu():
    print("\n" + "-" * 45)
    print("CYBERSECURITY ASSET INVENTORY SYSTEM")
    print("-" * 45)
    print("1. Add Asset")
    print("2. Display Assets")
    print("3. Search Asset")
    print("4. Update Asset")
    print("5. Delete Asset")
    print("6. Exit")
    print("-" * 45)


def main():
    assets = load_assets()

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                add_asset(assets)
                print("Asset added successfully.")
            elif choice == "2":
                display_assets(assets)
            elif choice == "3":
                query = input("Enter Asset ID, name, IP, or department: ")
                results = search_assets(assets, query)
                display_assets(results)
            elif choice == "4":
                asset_id = input("Enter Asset ID to update: ")
                if update_asset(assets, asset_id):
                    print("Asset updated successfully.")
                else:
                    print("Asset not found.")
            elif choice == "5":
                asset_id = input("Enter Asset ID to delete: ")
                if delete_asset(assets, asset_id):
                    print("Asset deleted successfully.")
                else:
                    print("Asset not found.")
            elif choice == "6":
                print("Exiting Cybersecurity Asset Inventory System.")
                break
            else:
                print("Invalid choice. Please select 1-6.")
        except ValueError as exc:
            print(f"Validation Error: {exc}")


if __name__ == "__main__":
    main()
