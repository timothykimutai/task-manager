"""Version management and changelog generation script."""

import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Tuple


def get_current_version() -> str:
    """Get current version from __init__.py."""
    init_file = Path("task_manager/__init__.py")
    with open(init_file) as f:
        content = f.read()
        match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            return match.group(1)
    raise ValueError("Could not find version in __init__.py")


def update_version(new_version: str) -> None:
    """Update version in __init__.py."""
    init_file = Path("task_manager/__init__.py")
    with open(init_file) as f:
        content = f.read()
    
    new_content = re.sub(
        r'__version__\s*=\s*["\']([^"\']+)["\']',
        f'__version__ = "{new_version}"',
        content
    )
    
    with open(init_file, "w") as f:
        f.write(new_content)


def get_git_changes() -> List[Tuple[str, str]]:
    """Get list of commits since last tag."""
    import subprocess
    
    # Get last tag
    try:
        last_tag = subprocess.check_output(
            ["git", "describe", "--tags", "--abbrev=0"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
    except subprocess.CalledProcessError:
        # No tags found, get all commits
        last_tag = ""
    
    # Get commits since last tag
    if last_tag:
        cmd = ["git", "log", f"{last_tag}..HEAD", "--pretty=format:%h|%s"]
    else:
        cmd = ["git", "log", "--pretty=format:%h|%s"]
    
    output = subprocess.check_output(cmd).decode().strip()
    if not output:
        return []
    
    changes = []
    for line in output.split("\n"):
        if "|" in line:
            commit_hash, message = line.split("|", 1)
            changes.append((commit_hash, message))
    return changes


def generate_changelog(version: str, changes: List[Tuple[str, str]]) -> str:
    """Generate changelog entry."""
    date = datetime.now().strftime("%Y-%m-%d")
    changelog = f"## [{version}] - {date}\n\n"
    
    # Group changes by type
    features = []
    fixes = []
    other = []
    
    for _, message in changes:
        if message.startswith("feat:"):
            features.append(message[5:].strip())
        elif message.startswith("fix:"):
            fixes.append(message[4:].strip())
        else:
            other.append(message.strip())
    
    if features:
        changelog += "### Features\n\n"
        for feature in features:
            changelog += f"- {feature}\n"
        changelog += "\n"
    
    if fixes:
        changelog += "### Bug Fixes\n\n"
        for fix in fixes:
            changelog += f"- {fix}\n"
        changelog += "\n"
    
    if other:
        changelog += "### Other Changes\n\n"
        for change in other:
            changelog += f"- {change}\n"
        changelog += "\n"
    
    return changelog


def update_changelog(version: str) -> None:
    """Update CHANGELOG.md with new version."""
    changelog_file = Path("CHANGELOG.md")
    
    # Get changes
    changes = get_git_changes()
    if not changes:
        print("No changes found since last tag")
        return
    
    # Generate new changelog entry
    new_entry = generate_changelog(version, changes)
    
    # Update changelog file
    if changelog_file.exists():
        with open(changelog_file) as f:
            content = f.read()
        
        # Find the position to insert new entry
        if "# Changelog" in content:
            pos = content.find("# Changelog") + len("# Changelog")
            new_content = content[:pos] + "\n\n" + new_entry + content[pos:]
        else:
            new_content = "# Changelog\n\n" + new_entry + content
    else:
        new_content = "# Changelog\n\n" + new_entry
    
    with open(changelog_file, "w") as f:
        f.write(new_content)


def generate_release_notes(version: str) -> None:
    """Generate release notes for GitHub release."""
    changelog_file = Path("CHANGELOG.md")
    if not changelog_file.exists():
        print("No changelog found")
        return
    
    with open(changelog_file) as f:
        content = f.read()
    
    # Extract the latest version's changelog
    pattern = f"## [{version}]"
    if pattern in content:
        start = content.find(pattern)
        end = content.find("## [", start + 1)
        if end == -1:
            release_notes = content[start:]
        else:
            release_notes = content[start:end]
    else:
        print(f"No changelog entry found for version {version}")
        return
    
    # Write to file
    release_notes_file = Path(f"RELEASE_NOTES_{version}.md")
    with open(release_notes_file, "w") as f:
        f.write(release_notes)
    
    print(f"Release notes written to {release_notes_file}")


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python version.py <new_version>")
        sys.exit(1)
    
    new_version = sys.argv[1]
    if not re.match(r"^\d+\.\d+\.\d+$", new_version):
        print("Version must be in format X.Y.Z")
        sys.exit(1)
    
    try:
        current_version = get_current_version()
        print(f"Current version: {current_version}")
        print(f"New version: {new_version}")
        
        # Update version
        update_version(new_version)
        print("Updated version in __init__.py")
        
        # Update changelog
        update_changelog(new_version)
        print("Updated CHANGELOG.md")
        
        # Generate release notes
        generate_release_notes(new_version)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 