#!/usr/bin/env python3
"""
SuperGemini Uninstall Script
Standalone uninstall script that doesn't rely on complex imports
"""

import shutil
import json
import sys
from pathlib import Path


def uninstall_supergemini(install_dir=None, verbose=False):
    """Uninstall SuperGemini framework (sg command only)"""

    # Default to ~/.gemini directory
    if install_dir is None:
        install_dir = Path.home() / ".gemini"
    else:
        install_dir = Path(install_dir)

    # Check if gemini directory exists
    if not install_dir.exists():
        print(f"⚠️ SuperGemini installation directory not found at {install_dir}")
        return 0

    # Safety check - ensure it's the Gemini directory
    if install_dir.name != ".gemini":
        response = input(
            f"❓ Directory {install_dir} doesn't appear to be a standard SuperGemini installation. Continue? (y/N): "
        )
        if response.lower() != "y":
            print("Uninstall cancelled.")
            return 1

    # Define items to be removed
    print("\n" + "=" * 60)
    print("       SuperGemini Uninstall (sg command)")
    print("=" * 60)
    print(f"\n📂 Installation directory: {install_dir}")

    print("\n📋 Items to be removed:")
    target_items = [
        ("commands/sg", "SuperGemini command directory"),
        (".supergemini-metadata.json", "SuperGemini metadata file"),
    ]

    for item_path, description in target_items:
        print(f"  - {item_path} ({description})")

    # Check which items exist
    print("\n🔍 Checking existence of items...")
    items_to_delete = []

    for item_path, description in target_items:
        full_path = install_dir / item_path
        if full_path.exists():
            if full_path.is_file():
                size = full_path.stat().st_size
                print(f"  ✓ Found: {item_path} ({size} bytes)")
            else:
                file_count = sum(1 for _ in full_path.rglob("*") if _.is_file())
                dir_count = sum(1 for _ in full_path.rglob("*") if _.is_dir())
                print(
                    f"  ✓ Found: {item_path} ({file_count} files, {dir_count} subdirs)"
                )
            items_to_delete.append((full_path, item_path))
        else:
            print(f"  ✗ Not found: {item_path}")

    # Check if anything can be deleted
    if not items_to_delete:
        print("\n⚠️  No SuperGemini components found to remove.")
        return 0

    # Summary before deletion
    print(f"\n📊 Summary:")
    print(f"  Items found: {len(items_to_delete)}")
    print(f"  Items not found: {len(target_items) - len(items_to_delete)}")

    # Final confirmation
    print(f"\n⚠️  WARNING: This will permanently delete the following:")
    for path, item_name in items_to_delete:
        print(f"  - {item_name}")

    if "--yes" not in sys.argv and "-y" not in sys.argv:
        response = input("\nContinue with uninstall? (y/N): ")
        if response.lower() != "y":
            print("Uninstall cancelled.")
            return 1

    # Perform uninstall
    print(f"\n🗑️  Removing items...")
    errors = []
    removed_count = 0

    for path, item_name in items_to_delete:
        try:
            if path.is_file():
                path.unlink()
                print(f"  ✓ Removed: {item_name}")
            elif path.is_dir():
                shutil.rmtree(path)
                print(f"  ✓ Removed: {item_name}")
            removed_count += 1
        except Exception as e:
            errors.append(f"  ✗ Failed to remove {item_name}: {e}")
            print(f"  ✗ Failed to remove {item_name}: {e}")

    # Final summary
    if errors:
        print(
            f"\n⚠️  Uninstall completed with errors ({removed_count}/{len(items_to_delete)} items removed)"
        )
        return 1
    else:
        print(f"\n✅ Uninstall completed successfully! ({removed_count} items removed)")
        print("\nYou can reinstall anytime using:")
        print("  pip install -e . && python -m SuperGemini install")
        return 0


def main():
    """Main entry point"""
    # Parse simple command line arguments
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    # Check for custom install directory
    install_dir = None
    for i, arg in enumerate(sys.argv):
        if arg == "--install-dir" and i + 1 < len(sys.argv):
            install_dir = sys.argv[i + 1]
            break

    # Run uninstall
    return uninstall_supergemini(install_dir, verbose)


if __name__ == "__main__":
    sys.exit(main())
