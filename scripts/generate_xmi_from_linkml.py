#!/usr/bin/env python3
"""Generate an XMI 2.1 UML model from the LinkML schemas under ./src.

The script walks all LinkML YAML files in the provided source directory,
reconstructs package/class hierarchies, and emits a simplified UML/XMI
representation that mirrors the content we previously imported from the
Enterprise Architect export.
"""

from __future__ import annotations

import argparse
import hashlib
import os
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
import xml.etree.ElementTree as ET

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: PyYAML is required. Install with `pip install pyyaml`."
    ) from exc

UML_NS = "http://schema.omg.org/spec/UML/2.1"
XMI_NS = "http://schema.omg.org/spec/XMI/2.1"
NSMAP = {"xmi": XMI_NS, "uml": UML_NS}
BASE_ID_PREFIX = "https://w3id.org/novari/fint/"

PRIMITIVE_HREF = {
    "string": "http://schema.omg.org/spec/UML/2.1/uml.xml#String",
    "integer": "http://schema.omg.org/spec/UML/2.1/uml.xml#Integer",
    "boolean": "http://schema.omg.org/spec/UML/2.1/uml.xml#Boolean",
    "float": "http://schema.omg.org/spec/UML/2.1/uml.xml#Real",
    "double": "http://schema.omg.org/spec/UML/2.1/uml.xml#Double",
    "decimal": "http://schema.omg.org/spec/UML/2.1/uml.xml#Real",
    "date": "http://schema.omg.org/spec/UML/2.1/uml.xml#Date",
    "time": "http://schema.omg.org/spec/UML/2.1/uml.xml#Time",
    "datetime": "http://schema.omg.org/spec/UML/2.1/uml.xml#DateTime",
}

# Ensure consistent namespace prefixes in serialized XML output
ET.register_namespace("xmi", XMI_NS)
ET.register_namespace("uml", UML_NS)


@dataclass
class Slot:
    name: str
    range: str
    required: bool = False
    multivalued: bool = False
    description: Optional[str] = None


@dataclass
class SchemaClass:
    name: str
    package_path: Tuple[str, ...]
    description: Optional[str]
    abstract: bool
    is_a: Optional[str]
    attributes: List[Slot] = field(default_factory=list)
    stereotypes: List[str] = field(default_factory=list)


def sanitize_attribute_text(text: Optional[str]) -> Optional[str]:
    if text is None:
        return None
    return text.replace('\r\n', '\n').replace('\r', '\n')


def find_yaml_files(src_dir: Path) -> Iterable[Path]:
    for path in sorted(src_dir.glob("**/*.yaml")):
        if path.is_file():
            yield path


def load_schema(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def parse_package_path(schema_id: str) -> Tuple[str, ...]:
    if not schema_id.startswith(BASE_ID_PREFIX):
        raise ValueError(f"Schema id '{schema_id}' does not start with {BASE_ID_PREFIX}")
    rest = schema_id[len(BASE_ID_PREFIX):]
    return tuple(segment for segment in rest.strip("/").split("/") if segment)


def collect_classes(src_dir: Path) -> Tuple[List[SchemaClass], Dict[str, List[SchemaClass]]]:
    classes: List[SchemaClass] = []
    name_index: Dict[str, List[SchemaClass]] = defaultdict(list)

    for yaml_path in find_yaml_files(src_dir):
        schema = load_schema(yaml_path)
        schema_id = schema.get("id")
        if not schema_id:
            continue
        package_path = parse_package_path(schema_id)
        class_defs = schema.get("classes", {}) or {}
        for class_name, class_info in class_defs.items():
            attributes: List[Slot] = []
            for slot_name, slot_info in (class_info.get("attributes") or {}).items():
                slot = Slot(
                    name=slot_name,
                    range=(slot_info.get("range") or "string"),
                    required=bool(slot_info.get("required")),
                    multivalued=bool(slot_info.get("multivalued")),
                    description=slot_info.get("description"),
                )
                attributes.append(slot)
            stereos = class_info.get("stereotypes") or class_info.get("stereotype")
            if stereos is None:
                stereotype_list = ["hovedklasse"]
            elif isinstance(stereos, (list, tuple)):
                stereotype_list = [str(s) for s in stereos if s]
            else:
                stereotype_list = [str(stereos)]

            schema_class = SchemaClass(
                name=class_name,
                package_path=package_path,
                description=class_info.get("description"),
                abstract=bool(class_info.get("abstract")),
                is_a=class_info.get("is_a"),
                attributes=attributes,
                stereotypes=stereotype_list or ["hovedklasse"],
            )
            classes.append(schema_class)
            name_index[class_name].append(schema_class)
    return classes, name_index


def resolve_class_reference(
    ref_name: str,
    current_package: Tuple[str, ...],
    name_index: Dict[str, List[SchemaClass]],
) -> Optional[SchemaClass]:
    candidates = name_index.get(ref_name, [])
    if not candidates:
        return None
    # Prefer same package
    for candidate in candidates:
        if candidate.package_path == current_package:
            return candidate
    # Otherwise return first occurrence (deterministic thanks to load order)
    return candidates[0]


def make_id(kind: str, *components: str) -> str:
    base = "::".join(components)
    digest = hashlib.sha1(base.encode("utf-8")).hexdigest()[:18]
    return f"EAID_{kind}_{digest}"


def build_package_hierarchy(classes: List[SchemaClass]) -> Dict[Tuple[str, ...], Dict[str, List[SchemaClass]]]:
    packages: Dict[Tuple[str, ...], Dict[str, List[SchemaClass]]] = defaultdict(lambda: {"classes": []})
    for schema_class in classes:
        pkg_path = schema_class.package_path
        packages[pkg_path]["classes"].append(schema_class)
        # Ensure ancestors are present
        for depth in range(1, len(pkg_path)):
            ancestor = pkg_path[:depth]
            packages.setdefault(ancestor, {"classes": []})
    return packages


def add_comment(parent: ET.Element, text: str, comment_id: str) -> None:
    comment = ET.SubElement(parent, "ownedComment", {
        f"{{{XMI_NS}}}type": "uml:Comment",
        f"{{{XMI_NS}}}id": comment_id,
    })
    body = ET.SubElement(comment, "body")
    body.text = text


def set_slot_type(
    attr_el: ET.Element,
    slot: Slot,
    owner: SchemaClass,
    class_id_map: Dict[Tuple[str, ...], str],
    name_index: Dict[str, List[SchemaClass]],
) -> None:
    rng_name = slot.range or "string"
    rng_lower = rng_name.lower()
    if rng_lower in PRIMITIVE_HREF:
        ET.SubElement(attr_el, "type", {"href": PRIMITIVE_HREF[rng_lower]})
        return

    target_cls = resolve_class_reference(rng_name, owner.package_path, name_index)
    if target_cls:
        target_key = target_cls.package_path + (target_cls.name,)
        target_id = class_id_map.get(target_key)
        if target_id:
            ET.SubElement(attr_el, "type", {f"{{{XMI_NS}}}idref": target_id})
            return

    # Fallback to string when no class match was found
    ET.SubElement(attr_el, "type", {"href": PRIMITIVE_HREF["string"]})


def indent(elem: ET.Element, level: int = 0) -> None:
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for child in elem:
            indent(child, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def build_xmi(classes: List[SchemaClass], name_index: Dict[str, List[SchemaClass]]) -> ET.ElementTree:
    packages = build_package_hierarchy(classes)

    base_prefix = ("Model", "FINT")
    top_level_application_schemas = {name.casefold() for name in (
        "fullmakt",
        "arkiv",
        "administrasjon",
        "økonomi",
        "okonomi",
        "ressurs",
        "personvern",
        "felles",
        "utdanning",
    )}

    def ensure_prefix_path(target: Dict[Tuple[str, ...], Dict[str, List[SchemaClass]]], path: Tuple[str, ...]) -> None:
        target.setdefault(path, {"classes": []})

    prefixed_packages: Dict[Tuple[str, ...], Dict[str, List[SchemaClass]]] = defaultdict(lambda: {"classes": []})
    for depth in range(1, len(base_prefix) + 1):
        ensure_prefix_path(prefixed_packages, base_prefix[:depth])

    for pkg_path, data in packages.items():
        new_path = base_prefix + pkg_path
        prefixed_packages[new_path] = {"classes": data["classes"]}
        for depth in range(1, len(new_path) + 1):
            ensure_prefix_path(prefixed_packages, new_path[:depth])

    packages = prefixed_packages

    # Map (package_path) -> xmi:id og (package_path, class_name) -> xmi:id
    package_id_map: Dict[Tuple[str, ...], str] = {}
    class_id_map: Dict[Tuple[str, ...], str] = {}

    for pkg_path in sorted(packages.keys(), key=lambda p: (len(p), p)):
        name = pkg_path[-1] if pkg_path else "FINT"
        package_id_map[pkg_path] = make_id("PKG", "/".join(pkg_path) or "FINT")
        for schema_class in packages[pkg_path]["classes"]:
            key = pkg_path + (schema_class.name,)
            class_id_map[key] = make_id("CLS", "/".join(pkg_path), schema_class.name)

    root = ET.Element(f"{{{XMI_NS}}}XMI", {f"{{{XMI_NS}}}version": "2.1"})

    # Viktig: gi modellen xmi:type slik at TS-parseren setter Model-prototypen
    model = ET.SubElement(root, f"{{{UML_NS}}}Model", {
        f"{{{XMI_NS}}}type": "uml:Model",
        f"{{{XMI_NS}}}id": make_id("MODEL", "EA_Model"),
        "name": "EA_Model",
    })

    # Global Extension-container på rotnivå (EN gang)
    xmi_ext = ET.SubElement(root, f"{{{XMI_NS}}}Extension", {
        "extender": "Enterprise Architect",
        "extenderID": "6.5",
    })
    ext_elements = ET.SubElement(xmi_ext, "elements")

    package_elements: Dict[Tuple[str, ...], ET.Element] = {(): model}

    def is_top_level_application_schema(path: Tuple[str, ...]) -> bool:
        return (
            len(path) == len(base_prefix) + 1
            and path[: len(base_prefix)] == base_prefix
            and path[-1].casefold() in top_level_application_schemas
        )

    for pkg_path in sorted(packages.keys(), key=lambda p: (len(p), p)):
        parent_path = pkg_path[:-1]
        parent_element = package_elements.get(parent_path, model)
        schema_name = pkg_path[-1] if pkg_path else "FINT"
        apply_application_schema = is_top_level_application_schema(pkg_path)

        # Selve pakken i UML-delen
        pkg_element = ET.SubElement(parent_element, "packagedElement", {
            f"{{{XMI_NS}}}type": "uml:Package",
            f"{{{XMI_NS}}}id": package_id_map[pkg_path],
            "name": schema_name,
        })
        # Stereotype-kilde for TS-parseren: element-stubb i GLOBAL extension
        pkg_ext = ET.SubElement(ext_elements, "element", {
            f"{{{XMI_NS}}}idref": package_id_map[pkg_path],
            f"{{{XMI_NS}}}type": "uml:Package",
            "name": schema_name,
            "scope": "public",
        })
        ET.SubElement(pkg_ext, "tags")
        if apply_application_schema:
            ET.SubElement(pkg_ext, "properties", {"stereotype": "ApplicationSchema"})

        package_elements[pkg_path] = pkg_element

        # Klasser i pakken
        for schema_class in packages[pkg_path]["classes"]:
            class_key = pkg_path + (schema_class.name,)
            class_el = ET.SubElement(pkg_element, "packagedElement", {
                f"{{{XMI_NS}}}type": "uml:Class",
                f"{{{XMI_NS}}}id": class_id_map[class_key],
                "name": schema_class.name,
            })
            if schema_class.abstract:
                class_el.set("isAbstract", "true")

            # Valgfritt: properties på UML-noden (dokumentasjon)
            props_attrs = {}
            doc_text = sanitize_attribute_text(schema_class.description)
            if doc_text:
                props_attrs["documentation"] = doc_text
            if schema_class.stereotypes:
                props_attrs["stereotype"] = schema_class.stereotypes[0]
            if props_attrs:
                ET.SubElement(class_el, "properties", props_attrs)

            # Stereotype-kilde for TS-parseren: element-stubb i GLOBAL extension
            class_ext = ET.SubElement(ext_elements, "element", {
                f"{{{XMI_NS}}}idref": class_id_map[class_key],
                f"{{{XMI_NS}}}type": "uml:Class",
                "name": schema_class.name,
                "scope": "public",
            })
            ET.SubElement(class_ext, "tags")
            class_props = {}
            if doc_text:
                class_props["documentation"] = doc_text
            if schema_class.stereotypes:
                class_props["stereotype"] = schema_class.stereotypes[0]
            if class_props:
                ET.SubElement(class_ext, "properties", class_props)

            class_attributes_ext = ET.SubElement(class_ext, "attributes")

            if schema_class.description:
                add_comment(class_el, schema_class.description, make_id("CMT", "/".join(class_key)))

            if schema_class.is_a:
                superclass = resolve_class_reference(schema_class.is_a, schema_class.package_path, name_index)
                if superclass:
                    super_key = superclass.package_path + (superclass.name,)
                    super_id = class_id_map.get(super_key)
                    if super_id:
                        ET.SubElement(class_el, "generalization", {
                            f"{{{XMI_NS}}}type": "uml:Generalization",
                            f"{{{XMI_NS}}}id": make_id("GEN", "/".join(class_key)),
                            "general": super_id,
                        })

            # Attributter
            for slot in schema_class.attributes:
                attr_id = make_id("PRP", "/".join(class_key), slot.name)
                attr_el = ET.SubElement(class_el, "ownedAttribute", {
                    f"{{{XMI_NS}}}type": "uml:Property",
                    f"{{{XMI_NS}}}id": attr_id,
                    "name": slot.name,
                    "visibility": "public",
                })

                set_slot_type(attr_el, slot, schema_class, class_id_map, name_index)

                lower_value = "1" if slot.required else "0"
                ET.SubElement(attr_el, "lowerValue", {
                    f"{{{XMI_NS}}}type": "uml:LiteralInteger",
                    f"{{{XMI_NS}}}id": make_id("LWR", attr_id),
                    "value": lower_value,
                })

                if slot.multivalued:
                    ET.SubElement(attr_el, "upperValue", {
                        f"{{{XMI_NS}}}type": "uml:LiteralUnlimitedNatural",
                        f"{{{XMI_NS}}}id": make_id("UPR", attr_id),
                        "value": "*",
                    })
                else:
                    ET.SubElement(attr_el, "upperValue", {
                        f"{{{XMI_NS}}}type": "uml:LiteralInteger",
                        f"{{{XMI_NS}}}id": make_id("UPR", attr_id),
                        "value": "1",
                    })

                if slot.description:
                    add_comment(attr_el, slot.description, make_id("CMT", attr_id))

                attr_ext = ET.SubElement(class_attributes_ext, "attribute", {
                    f"{{{XMI_NS}}}idref": attr_id,
                    "name": slot.name,
                })
                ET.SubElement(attr_ext, "tags")

    indent(root)
    return ET.ElementTree(root)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a UML XMI 2.1 model from LinkML YAML schemas.")
    parser.add_argument("--src", default="src", help="Directory containing LinkML YAML schemas (default: src)")
    parser.add_argument("--out", default="FINT-informasjonsmodell.generated.xml", help="Output XMI file path")

    args = parser.parse_args()
    src_dir = Path(args.src)
    if not src_dir.exists():
        raise SystemExit(f"Source directory {src_dir} does not exist")

    classes, name_index = collect_classes(src_dir)
    if not classes:
        raise SystemExit("No classes found in provided LinkML sources")

    tree = build_xmi(classes, name_index)
    tree.write(args.out, encoding="windows-1252", xml_declaration=True)
    print(f"Wrote XMI to {args.out}")


if __name__ == "__main__":
    main()
