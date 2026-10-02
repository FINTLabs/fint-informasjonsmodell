#!/usr/bin/env python3
"""
Generate release notes from LinkML model changes between two git commits.

This script compares LinkML YAML model files between two git SHAs and generates
release notes based on detected changes such as added/removed classes, attributes,
and other model modifications.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

try:
    import yaml
except ImportError:
    yaml = None


def run_git(args: List[str], cwd: Path) -> subprocess.CompletedProcess:
    """Run a git command and return the result."""
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=True,
    )


def get_files_at_commit(commit_sha: str, repo_root: Path, pattern: str = "*.yaml") -> Dict[str, str]:
    """
    Get all YAML files from a specific commit.
    
    Returns a dictionary mapping file paths to their content at that commit.
    """
    # Get list of YAML files at the commit
    if commit_sha == "-":
        return {}  # Første release sammenlignes med en tom modell.
    result = run_git(["ls-tree", "-r", "--name-only", commit_sha, "src", "models"], repo_root)
    files = [f for f in result.stdout.splitlines() if f.endswith(".yaml")]
    
    file_contents = {}
    for file_path in files:
        try:
            result = run_git(["show", f"{commit_sha}:{file_path}"], repo_root)
            file_contents[file_path] = result.stdout
        except subprocess.CalledProcessError:
            # File might not exist at this commit
            continue
    
    return file_contents


def parse_yaml(content: str) -> Any:
    """Simple YAML parser for LinkML files without external dependencies."""
    if not content:
        return {}
    
    result = {}
    current_dict = result
    stack = [result]
    key_stack = []
    
    for line in content.split('\n'):
        # Count indentation
        indent = len(line) - len(line.lstrip())
        stripped = line.strip()
        
        if not stripped or stripped.startswith('#'):
            continue
        
        # Calculate nesting level (2 spaces per level)
        level = indent // 2
        
        # Adjust stack to correct level
        while len(stack) > level + 1:
            stack.pop()
            key_stack.pop()
        
        current_dict = stack[-1]
        
        if ':' in stripped:
            # Key-value pair
            parts = stripped.split(':', 1)
            key = parts[0].strip()
            value = parts[1].strip() if len(parts) > 1 else None
            
            if value == '':
                # This is a nested structure
                new_dict = {}
                current_dict[key] = new_dict
                stack.append(new_dict)
                key_stack.append(key)
            elif value.startswith('|'):
                # Multi-line string (skip for now, take next lines)
                current_dict[key] = ""
            else:
                # Simple value
                current_dict[key] = parse_yaml_value(value)
        elif stripped.startswith('- '):
            # List item
            item = stripped[2:].strip()
            if not isinstance(current_dict, list):
                # Convert current dict to list if needed
                if current_dict:
                    list_key = key_stack[-1] if key_stack else 'items'
                    stack[-2][list_key] = [current_dict]
                    stack[-1] = stack[-2][list_key]
                    current_dict = stack[-1]
                else:
                    stack[-1] = []
                    current_dict = stack[-1]
            
            if ':' in item:
                # Nested dict in list
                new_dict = {}
                current_dict.append(new_dict)
                stack.append(new_dict)
                key_stack.append('')
            else:
                current_dict.append(parse_yaml_value(item))
    
    return result


def parse_yaml_value(value: str) -> Any:
    """Parse a YAML value to the appropriate Python type."""
    if not value:
        return None
    
    # Boolean
    if value.lower() == 'true':
        return True
    if value.lower() == 'false':
        return False
    
    # Null
    if value.lower() in ['null', 'none', '~']:
        return None
    
    # Integer
    if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
        return int(value)
    
    # Float
    try:
        if '.' in value or 'e' in value.lower():
            return float(value)
    except ValueError:
        pass
    
    # String (remove quotes if present)
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    
    return value


def parse_linkml_model(content: str) -> Dict[str, Any]:
    """Parse a LinkML YAML file."""
    if yaml is None:
        print("WARNING: PyYAML not installed. Install it with: pip install pyyaml", file=sys.stderr)
        print("Falling back to simple YAML parser (may not handle all cases)", file=sys.stderr)
        try:
            return parse_yaml(content) or {}
        except Exception:
            return {}
    try:
        return yaml.safe_load(content) or {}
    except yaml.YAMLError:
        return {}


def extract_domain_from_filename(filename: str) -> str:
    """Extract domain name from filename (e.g., 'utdanning.vurdering.yaml' -> 'Utdanning')."""
    basename = Path(filename).stem
    parts = basename.split(".")
    if parts:
        return parts[0].capitalize()
    return "Unknown"


def format_multiplicity(attr: Dict) -> str:
    """Format attribute multiplicity as X..Y notation."""
    required = attr.get("required", False)
    multivalued = attr.get("multivalued", False)
    
    if required and multivalued:
        return "1..*"
    elif required and not multivalued:
        return "1..1"
    elif not required and multivalued:
        return "0..*"
    else:
        return "0..1"


def generate_doc_url(domain: str, class_name: str, version: str = "v4.0.30") -> str:
    """Generate documentation URL for a class."""
    base_url = "https://informasjonsmodell.felleskomponent.no/docs"
    slug = f"{domain.lower()}_{class_name.lower()}"
    return f"{base_url}/{slug}?v={version}"


def compare_classes(old_classes: Dict, new_classes: Dict) -> Tuple[Set[str], Set[str], Dict[str, List[str]]]:
    """
    Compare classes between two versions.
    
    Returns:
        - Added classes
        - Removed classes
        - Modified classes with change descriptions
    """
    old_names = set(old_classes.keys())
    new_names = set(new_classes.keys())
    
    added = new_names - old_names
    removed = old_names - new_names
    common = old_names & new_names
    
    modified = {}
    for class_name in common:
        changes = []
        old_cls = old_classes[class_name]
        new_cls = new_classes[class_name]
        
        # Check for description changes
        if old_cls.get("description") != new_cls.get("description"):
            changes.append("description updated")
        
        # Check for deprecated status
        if not old_cls.get("deprecated") and new_cls.get("deprecated"):
            changes.append(f"deprecated: {new_cls['deprecated']}")
        elif old_cls.get("deprecated") and not new_cls.get("deprecated"):
            changes.append("deprecated removed")
        
        # Check for is_a changes
        if old_cls.get("is_a") != new_cls.get("is_a"):
            changes.append(f"parent changed from {old_cls.get('is_a')} to {new_cls.get('is_a')}")
        
        # Compare attributes
        old_attrs = old_cls.get("attributes", {})
        new_attrs = new_cls.get("attributes", {})
        
        old_attr_names = set(old_attrs.keys())
        new_attr_names = set(new_attrs.keys())
        
        added_attrs = new_attr_names - old_attr_names
        removed_attrs = old_attr_names - new_attr_names
        
        if added_attrs:
            changes.append(f"added attributes: {', '.join(sorted(added_attrs))}")
        if removed_attrs:
            changes.append(f"removed attributes: {', '.join(sorted(removed_attrs))}")
        
        # Check for attribute modifications
        common_attrs = old_attr_names & new_attr_names
        for attr_name in common_attrs:
            old_attr = old_attrs[attr_name]
            new_attr = new_attrs[attr_name]
            
            if old_attr.get("description") != new_attr.get("description"):
                changes.append(f"attribute `{attr_name}` description updated")
            
            if old_attr.get("range") != new_attr.get("range"):
                changes.append(f"attribute `{attr_name}` range changed from {old_attr.get('range')} to {new_attr.get('range')}")
            
            # Check for multiplicity changes
            old_mult = format_multiplicity(old_attr)
            new_mult = format_multiplicity(new_attr)
            if old_mult != new_mult:
                changes.append(f"attribute `{attr_name}` multiplicity changed from {old_mult} to {new_mult}")
            
            if not old_attr.get("deprecated") and new_attr.get("deprecated"):
                changes.append(f"attribute `{attr_name}` deprecated: {new_attr['deprecated']}")
        
        if changes:
            modified[class_name] = changes
    
    return added, removed, modified


def compare_enums(old_enums: Dict, new_enums: Dict) -> Tuple[Set[str], Set[str], Dict[str, List[str]]]:
    """
    Compare enums between two versions.
    
    Returns:
        - Added enums
        - Removed enums
        - Modified enums with change descriptions
    """
    old_names = set(old_enums.keys())
    new_names = set(new_enums.keys())
    
    added = new_names - old_names
    removed = old_names - new_names
    common = old_names & new_names
    
    modified = {}
    for enum_name in common:
        changes = []
        old_enum = old_enums[enum_name]
        new_enum = new_enums[enum_name]
        
        old_values = {pv.get("text") for pv in old_enum.get("permissible_values", [])}
        new_values = {pv.get("text") for pv in new_enum.get("permissible_values", [])}
        
        added_values = new_values - old_values
        removed_values = old_values - new_values
        
        if added_values:
            changes.append(f"added values: {', '.join(sorted(added_values))}")
        if removed_values:
            changes.append(f"removed values: {', '.join(sorted(removed_values))}")
        
        if changes:
            modified[enum_name] = changes
    
    return added, removed, modified


def generate_release_notes(old_commit: str, new_commit: str, repo_root: Path) -> str:
    """Generate release notes by comparing models between two commits."""
    print(f"Comparing {old_commit} -> {new_commit}...")
    
    # Get files at both commits
    old_files = get_files_at_commit(old_commit, repo_root)
    new_files = get_files_at_commit(new_commit, repo_root)
    
    # Get all files that exist in either commit
    all_files = set(old_files.keys()) | set(new_files.keys())
    
    # Organize changes by domain
    domain_changes: Dict[str, Dict[str, Any]] = {}
    
    for file_path in sorted(all_files):
        domain = extract_domain_from_filename(file_path)
        
        if domain not in domain_changes:
            domain_changes[domain] = {
                "added_classes": set(),
                "removed_classes": set(),
                "modified_classes": {},
                "added_enums": set(),
                "removed_enums": set(),
                "modified_enums": {},
            }
        
        old_content = old_files.get(file_path, "")
        new_content = new_files.get(file_path, "")
        
        old_model = parse_linkml_model(old_content) if old_content else {}
        new_model = parse_linkml_model(new_content) if new_content else {}
        
        # Compare classes
        old_classes = old_model.get("classes", {})
        new_classes = new_model.get("classes", {})
        
        added_classes, removed_classes, modified_classes = compare_classes(old_classes, new_classes)
        
        domain_changes[domain]["added_classes"].update(added_classes)
        domain_changes[domain]["removed_classes"].update(removed_classes)
        domain_changes[domain]["modified_classes"].update(modified_classes)
        
        # Compare enums
        old_enums = old_model.get("enums", {})
        new_enums = new_model.get("enums", {})
        
        added_enums, removed_enums, modified_enums = compare_enums(old_enums, new_enums)
        
        domain_changes[domain]["added_enums"].update(added_enums)
        domain_changes[domain]["removed_enums"].update(removed_enums)
        domain_changes[domain]["modified_enums"].update(modified_enums)
    
    # Generate markdown release notes grouped by domain
    notes = []
    
    for domain, changes in sorted(domain_changes.items()):
        domain_notes = []
        
        # Added classes
        if changes["added_classes"]:
            domain_notes.append("")
            domain_notes.append("**Added classes**")
            for cls in sorted(changes["added_classes"]):
                domain_notes.append(f"- `{cls}`")
        
        # Removed classes (breaking changes)
        if changes["removed_classes"]:
            domain_notes.append("")
            domain_notes.append("**Removed classes**")
            for cls in sorted(changes["removed_classes"]):
                domain_notes.append(f"- `{cls}`")
        
        # Added enums
        if changes["added_enums"]:
            domain_notes.append("")
            domain_notes.append("**Added enums**")
            for enum in sorted(changes["added_enums"]):
                domain_notes.append(f"- {enum}")
        
        # Removed enums
        if changes["removed_enums"]:
            domain_notes.append("")
            domain_notes.append("**Removed enums**")
            for enum in sorted(changes["removed_enums"]):
                domain_notes.append(f"- {enum}")
        
        # Organize class modifications by type
        # Flere attributtbeskrivelser kan være endret på samme klasse.
        # Oppsummer klassen én gang under «Description updated».
        description_updates = set()
        attributes_added = {}  # class -> list of attributes
        attributes_removed = {}  # class -> list of attributes
        multiplicity_changes = []  # multiplicity changes
        attribute_changes = []  # other attribute changes (range, etc.)
        parent_changes = []
        deprecated_items = []
        
        for cls, mods in sorted(changes["modified_classes"].items()):
            for mod in mods:
                if "description updated" in mod:
                    description_updates.add(cls)
                elif mod.startswith("added attributes:"):
                    attrs = mod.replace("added attributes: ", "").split(", ")
                    attributes_added[cls] = attrs
                elif mod.startswith("removed attributes:"):
                    attrs = mod.replace("removed attributes: ", "").split(", ")
                    attributes_removed[cls] = attrs
                elif "multiplicity changed" in mod:
                    multiplicity_changes.append(f"{cls}: {mod}")
                elif "deprecated" in mod and "deprecated removed" not in mod:
                    deprecated_items.append(f"{cls}: {mod}")
                elif mod.startswith("parent changed"):
                    parent_changes.append(f"{cls}: {mod}")
                else:
                    # Other attribute changes (range, etc.)
                    attribute_changes.append(f"{cls}: {mod}")
        
        if description_updates:
            domain_notes.append("")
            domain_notes.append("**Description updated**")
            for cls in sorted(description_updates):
                domain_notes.append(f"- `{cls}`")
        
        if attributes_added:
            domain_notes.append("")
            domain_notes.append("**Attributes added**")
            for cls, attrs in sorted(attributes_added.items()):
                for attr in sorted(attrs):
                    domain_notes.append(f"- `{attr}` (to `{cls}`)")
        
        if attributes_removed:
            domain_notes.append("")
            domain_notes.append("**Attributes removed**")
            for cls, attrs in sorted(attributes_removed.items()):
                for attr in sorted(attrs):
                    domain_notes.append(f"- `{attr}` (from `{cls}`)")
        
        if multiplicity_changes:
            domain_notes.append("")
            domain_notes.append("**Multiplicity changed**")
            for change in sorted(multiplicity_changes):
                # Parse "ClassName: attribute 'attr' multiplicity changed from X..Y to A..B"
                if ":" in change:
                    cls_part, rest = change.split(":", 1)
                    cls_name = cls_part.strip()
                    domain_notes.append(f"- `{cls_name}`: {rest}")
                else:
                    domain_notes.append(f"- {change}")
        
        if attribute_changes:
            domain_notes.append("")
            domain_notes.append("**Other attribute changes**")
            for change in attribute_changes:
                # Parse "ClassName: attribute 'attr' range changed from X to Y"
                if ":" in change:
                    cls_part, rest = change.split(":", 1)
                    cls_name = cls_part.strip()
                    domain_notes.append(f"- `{cls_name}`: {rest}")
                else:
                    domain_notes.append(f"- {change}")
        
        if parent_changes:
            domain_notes.append("")
            domain_notes.append("**Parent changes**")
            for change in parent_changes:
                # Parse "ClassName: parent changed from X to Y"
                if ":" in change:
                    cls_part, rest = change.split(":", 1)
                    cls_name = cls_part.strip()
                    domain_notes.append(f"- `{cls_name}`: {rest}")
                else:
                    domain_notes.append(f"- {change}")
        
        if deprecated_items:
            domain_notes.append("")
            domain_notes.append("**Deprecated**")
            for item in sorted(deprecated_items):
                # Parse "ClassName: deprecated: message"
                if ":" in item:
                    cls_part, rest = item.split(":", 1)
                    cls_name = cls_part.strip()
                    domain_notes.append(f"- `{cls_name}`: {rest}")
                else:
                    domain_notes.append(f"- {item}")
        
        # Enum modifications
        enum_changes = []
        for enum, mods in sorted(changes["modified_enums"].items()):
            enum_changes.append(f"{enum}: {', '.join(mods)}")
        
        if enum_changes:
            domain_notes.append("")
            domain_notes.append("**Enum changes**")
            for change in enum_changes:
                domain_notes.append(f"- {change}")
        
        if domain_notes:
            notes.append(f"## {domain}")
            for note in domain_notes:
                notes.append(note)
            notes.append("")
    
    if not notes:
        notes.append("No changes detected in LinkML models.")
    
    return "\n".join(notes)


def main():
    parser = argparse.ArgumentParser(
        description="Generate release notes from LinkML model changes between two git commits."
    )
    parser.add_argument("old_commit", help="Old git commit SHA or tag")
    parser.add_argument("new_commit", help="New git commit SHA or tag")
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1], 
                       help="Path to git repository (default: script parent directory)")
    parser.add_argument("--output", "-o", type=Path, help="Output file for release notes")
    args = parser.parse_args()
    
    repo_root = args.repo.resolve()
    
    if not repo_root.exists():
        print(f"ERROR: Repository path does not exist: {repo_root}", file=sys.stderr)
        sys.exit(1)
    
    if not (repo_root / ".git").exists():
        print(f"ERROR: Not a git repository: {repo_root}", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Validate commits exist
        if args.old_commit != "-":
            run_git(["rev-parse", args.old_commit], repo_root)
        run_git(["rev-parse", args.new_commit], repo_root)
    except subprocess.CalledProcessError:
        print(f"ERROR: One or both commits do not exist", file=sys.stderr)
        sys.exit(1)
    
    try:
        notes = generate_release_notes(args.old_commit, args.new_commit, repo_root)
    except Exception as exc:
        print(f"ERROR: Failed to generate release notes: {exc}", file=sys.stderr)
        sys.exit(1)
    
    if args.output:
        args.output.write_text(notes)
        print(f"Release notes written to: {args.output}")
    else:
        print("\n" + notes)


if __name__ == "__main__":
    main()
