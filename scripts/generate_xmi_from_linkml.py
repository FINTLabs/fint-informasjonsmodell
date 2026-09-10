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

PRIMITIVE_MODEL_TYPE = {
    "string": "string",
    "integer": "long",
    "boolean": "boolean",
    "float": "float",
    "double": "double",
    "decimal": "double",
    "date": "date",
    "time": "time",
    "datetime": "datetime",
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
    inverse: Optional[str] = None
    primary_relation: bool = False
    writeable: bool = False
    description: Optional[str] = None
    deprecated: Optional[str] = None


@dataclass
class SchemaClass:
    name: str
    package_path: Tuple[str, ...]
    import_paths: set[str]
    explicit_stereotype: Optional[str]
    description: Optional[str]
    abstract: bool
    is_a: Optional[str]
    attributes: List[Slot] = field(default_factory=list)
    stereotypes: List[str] = field(default_factory=list)
    deprecated: Optional[str] = None


def sanitize_attribute_text(text: Optional[str]) -> Optional[str]:
    if text is None:
        return None
    return text.replace('\r\n', '\n').replace('\r', '\n')


def normalize_metadata_text(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    text = sanitize_attribute_text(str(value))
    if text is None:
        return None
    stripped = text.strip()
    return stripped or None


def to_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes", "y", "on"}
    if isinstance(value, (int, float)):
        return bool(value)
    return False


def append_deprecated_tag(parent: ET.Element, text: Optional[str]) -> None:
    if not text:
        return
    ET.SubElement(parent, "tag", {
        "name": "DEPRECATED",
        "value": text,
    })


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
    return tuple(segment.replace("-", "") for segment in rest.strip("/").split("/") if segment)


def normalize_import_path(import_name: str) -> str:
    parts = [part.replace("-", "") for part in str(import_name).split(".") if part]
    return ".".join(parts)


def normalize_class_stereotype(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    token = str(value).strip().lower()
    if token == "kompleks-datatype":
        return "datatype"
    if token in {"hovedklasse", "datatype", "abstrakt", "referanse"}:
        return token
    return None


def display_package_name(segment: str) -> str:
    if not segment:
        return segment
    return segment[0].upper() + segment[1:]


def should_emit_class_stereotype(value: str) -> bool:
    token = (value or "").strip().lower()
    # EA kildefil markerer normalt ikke komplekse datatyper med stereotypeverdi.
    # De fremgår av modellstruktur/pakker. Behold eksplisitte stereotyper for øvrige klasser.
    return token in {"hovedklasse", "abstrakt", "referanse"}


def collect_classes(src_dir: Path) -> Tuple[List[SchemaClass], Dict[str, List[SchemaClass]]]:
    classes: List[SchemaClass] = []
    name_index: Dict[str, List[SchemaClass]] = defaultdict(list)

    for yaml_path in find_yaml_files(src_dir):
        schema = load_schema(yaml_path)
        schema_id = schema.get("id")
        if not schema_id:
            continue
        package_path = parse_package_path(schema_id)
        imports = schema.get("imports", []) or []
        normalized_imports = {normalize_import_path(imp) for imp in imports if isinstance(imp, str)}
        class_defs = schema.get("classes", {}) or {}
        for class_name, class_info in class_defs.items():
            attributes: List[Slot] = []
            for slot_name, slot_info in (class_info.get("attributes") or {}).items():
                annotations = slot_info.get("annotations") or {}
                slot = Slot(
                    name=slot_name,
                    range=(slot_info.get("range") or "string"),
                    required=bool(slot_info.get("required")),
                    multivalued=bool(slot_info.get("multivalued")),
                    inverse=(str(slot_info.get("inverse")).strip() if slot_info.get("inverse") else None),
                    primary_relation=to_bool(annotations.get("primaryRelation")),
                    writeable=to_bool(annotations.get("writeable")),
                    description=slot_info.get("description"),
                    deprecated=normalize_metadata_text(slot_info.get("deprecated")),
                )
                attributes.append(slot)
            schema_class = SchemaClass(
                name=class_name,
                package_path=package_path,
                import_paths=normalized_imports,
                explicit_stereotype=normalize_class_stereotype(
                    (class_info.get("annotations") or {}).get("stereotype")
                    or (class_info.get("annotations") or {}).get("fintStereotype")
                ),
                description=class_info.get("description"),
                abstract=bool(class_info.get("abstract")),
                is_a=class_info.get("is_a"),
                attributes=attributes,
                stereotypes=[],
                deprecated=normalize_metadata_text(class_info.get("deprecated")),
            )
            classes.append(schema_class)
            name_index[class_name].append(schema_class)
    return classes, name_index


def has_identifikator_attribute(schema_class: SchemaClass) -> bool:
    return any((slot.range or "").lower() == "identifikator" for slot in schema_class.attributes)


def is_identifiable_class(
    schema_class: SchemaClass,
    name_index: Dict[str, List[SchemaClass]],
    memo: Dict[Tuple[str, ...], bool],
    visiting: set,
) -> bool:
    key = schema_class.package_path + (schema_class.name,)
    if key in memo:
        return memo[key]
    if key in visiting:
        return False

    visiting.add(key)
    result = has_identifikator_attribute(schema_class)

    if not result and schema_class.is_a:
        parent = resolve_class_reference(
            schema_class.is_a,
            schema_class.package_path,
            name_index,
            schema_class.import_paths,
        )
        if parent is not None:
            result = is_identifiable_class(parent, name_index, memo, visiting)

    visiting.remove(key)
    memo[key] = result
    return result


def apply_default_stereotypes(classes: List[SchemaClass], name_index: Dict[str, List[SchemaClass]]) -> None:
    memo: Dict[Tuple[str, ...], bool] = {}
    for schema_class in classes:
        if schema_class.explicit_stereotype:
            schema_class.stereotypes = [schema_class.explicit_stereotype]
            continue
        if schema_class.abstract:
            schema_class.stereotypes = ["abstrakt"]
            continue
        if is_identifiable_class(schema_class, name_index, memo, set()):
            schema_class.stereotypes = ["hovedklasse"]
        else:
            schema_class.stereotypes = ["datatype"]


def is_datatype_class(schema_class: Optional[SchemaClass]) -> bool:
    if schema_class is None:
        return False
    return any(st.lower() == "datatype" for st in schema_class.stereotypes)


def resolve_class_reference(
    ref_name: str,
    current_package: Tuple[str, ...],
    name_index: Dict[str, List[SchemaClass]],
    current_imports: Optional[set[str]] = None,
) -> Optional[SchemaClass]:
    candidates = name_index.get(ref_name, [])
    if not candidates:
        return None
    # Prefer same package
    for candidate in candidates:
        if candidate.package_path == current_package:
            return candidate
    if current_imports:
        imported_candidates = [
            candidate
            for candidate in candidates
            if ".".join(candidate.package_path) in current_imports
        ]
        if len(imported_candidates) == 1:
            return imported_candidates[0]
        if imported_candidates:
            return imported_candidates[0]
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
    class_id_lookup: Dict[Tuple[str, ...], str],
    name_index: Dict[str, List[SchemaClass]],
) -> None:
    rng_name = slot.range or "string"
    rng_lower = rng_name.lower()
    if rng_lower in PRIMITIVE_HREF:
        ET.SubElement(attr_el, "type", {"href": PRIMITIVE_HREF[rng_lower]})
        return

    target_cls = resolve_class_reference(rng_name, owner.package_path, name_index, owner.import_paths)
    if target_cls:
        target_key = target_cls.package_path + (target_cls.name,)
        target_id = class_id_lookup.get(target_key)
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


def slot_type_name(slot: Slot) -> str:
    rng_name = slot.range or "string"
    rng_lower = rng_name.lower()
    if rng_lower in PRIMITIVE_MODEL_TYPE:
        return PRIMITIVE_MODEL_TYPE[rng_lower]
    return rng_name


def slot_multiplicity(slot: Slot) -> str:
    if slot.required and slot.multivalued:
        return "1..*"
    if slot.multivalued:
        return "0..*"
    return "1" if slot.required else "0..1"


def slot_multiplicity_for_role(owner: SchemaClass, role_name: Optional[str]) -> str:
    if not role_name:
        return "0..1"
    for candidate in owner.attributes:
        if candidate.name == role_name:
            return slot_multiplicity(candidate)
    return "0..1"


def find_slot_by_name(owner: SchemaClass, role_name: Optional[str]) -> Optional[Slot]:
    if not role_name:
        return None
    for candidate in owner.attributes:
        if candidate.name == role_name:
            return candidate
    return None


def extension_ref_attrs(kind: str, element_id: str) -> Dict[str, str]:
    return {
        f"{{{XMI_NS}}}idref": element_id,
        "idref": element_id,
        f"{{{XMI_NS}}}type": f"uml:{kind}",
        "type": kind,
    }


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

    # Map prefixed package/class paths to ids and an additional class lookup based
    # on original (unprefixed) package paths from LinkML.
    package_id_map: Dict[Tuple[str, ...], str] = {}
    class_id_map: Dict[Tuple[str, ...], str] = {}
    class_id_lookup: Dict[Tuple[str, ...], str] = {}

    for pkg_path in sorted(packages.keys(), key=lambda p: (len(p), p)):
        package_id_map[pkg_path] = make_id("PKG", "/".join(pkg_path) or "FINT")
        for schema_class in packages[pkg_path]["classes"]:
            key = pkg_path + (schema_class.name,)
            class_id = make_id("CLS", "/".join(pkg_path), schema_class.name)
            class_id_map[key] = class_id
            class_id_lookup[schema_class.package_path + (schema_class.name,)] = class_id

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
    ext_connectors = ET.SubElement(xmi_ext, "connectors")

    package_elements: Dict[Tuple[str, ...], ET.Element] = {(): model}
    emitted_bidirectional_associations = set()

    def is_top_level_application_schema(path: Tuple[str, ...]) -> bool:
        return (
            len(path) == len(base_prefix) + 1
            and path[: len(base_prefix)] == base_prefix
            and path[-1].casefold() in top_level_application_schemas
        )

    for pkg_path in sorted(packages.keys(), key=lambda p: (len(p), p)):
        parent_path = pkg_path[:-1]
        parent_element = package_elements.get(parent_path, model)
        schema_name = display_package_name(pkg_path[-1]) if pkg_path else "FINT"
        apply_application_schema = is_top_level_application_schema(pkg_path)

        # Selve pakken i UML-delen
        pkg_element = ET.SubElement(parent_element, "packagedElement", {
            f"{{{XMI_NS}}}type": "uml:Package",
            f"{{{XMI_NS}}}id": package_id_map[pkg_path],
            "name": schema_name,
        })
        # Stereotype-kilde for TS-parseren: element-stubb i GLOBAL extension
        pkg_ext_attrs = extension_ref_attrs("Package", package_id_map[pkg_path])
        pkg_ext_attrs.update({
            "name": schema_name,
            "scope": "public",
        })
        pkg_ext = ET.SubElement(ext_elements, "element", pkg_ext_attrs)
        pkg_model_attrs = {
            "package2": package_id_map[pkg_path],
            "ea_eleType": "package",
        }
        parent_id = package_id_map.get(parent_path)
        if parent_id:
            pkg_model_attrs["package"] = parent_id
        ET.SubElement(pkg_ext, "model", pkg_model_attrs)
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
                stereotype = schema_class.stereotypes[0]
                if should_emit_class_stereotype(stereotype):
                    props_attrs["stereotype"] = stereotype
            if props_attrs:
                ET.SubElement(class_el, "properties", props_attrs)

            # Stereotype-kilde for TS-parseren: element-stubb i GLOBAL extension
            class_ext_attrs = extension_ref_attrs("Class", class_id_map[class_key])
            class_ext_attrs.update({
                "name": schema_class.name,
                "scope": "public",
            })
            class_ext = ET.SubElement(ext_elements, "element", class_ext_attrs)
            ET.SubElement(class_ext, "model", {
                "package": package_id_map[pkg_path],
                "ea_eleType": "element",
            })
            class_tags = ET.SubElement(class_ext, "tags")
            append_deprecated_tag(class_tags, schema_class.deprecated)
            class_props = {
                "isAbstract": "true" if schema_class.abstract else "false",
                "sType": "Class",
                "scope": "public",
            }
            if doc_text:
                class_props["documentation"] = doc_text
            if schema_class.stereotypes:
                stereotype = schema_class.stereotypes[0]
                if should_emit_class_stereotype(stereotype):
                    class_props["stereotype"] = stereotype
            ET.SubElement(class_ext, "properties", class_props)

            class_attributes_ext = ET.SubElement(class_ext, "attributes")

            if schema_class.description:
                add_comment(class_el, schema_class.description, make_id("CMT", "/".join(class_key)))

            if schema_class.is_a:
                superclass = resolve_class_reference(
                    schema_class.is_a,
                    schema_class.package_path,
                    name_index,
                    schema_class.import_paths,
                )
                if superclass:
                    super_key = superclass.package_path + (superclass.name,)
                    super_id = class_id_lookup.get(super_key)
                    if super_id:
                        gen_id = make_id("GEN", "/".join(class_key))
                        ET.SubElement(class_el, "generalization", {
                            f"{{{XMI_NS}}}type": "uml:Generalization",
                            f"{{{XMI_NS}}}id": gen_id,
                            "general": super_id,
                            "start": class_id_map[class_key],
                            "end": super_id,
                        })
                        gen_conn = ET.SubElement(ext_connectors, "connector", {
                            f"{{{XMI_NS}}}type": "uml:Generalization",
                            f"{{{XMI_NS}}}idref": gen_id,
                            "idref": gen_id,
                            "start": class_id_map[class_key],
                            "end": super_id,
                        })
                        gen_source = ET.SubElement(gen_conn, "source", {
                            f"{{{XMI_NS}}}idref": class_id_map[class_key],
                            "idref": class_id_map[class_key],
                        })
                        ET.SubElement(gen_source, "model", {"type": "Class", "name": schema_class.name})
                        ET.SubElement(gen_source, "role", {"visibility": "Public"})
                        ET.SubElement(gen_source, "type", {"multiplicity": "0..1"})
                        ET.SubElement(gen_source, "tags")
                        gen_target = ET.SubElement(gen_conn, "target", {
                            f"{{{XMI_NS}}}idref": super_id,
                            "idref": super_id,
                        })
                        ET.SubElement(gen_target, "model", {"type": "Class", "name": superclass.name})
                        ET.SubElement(gen_target, "role", {"visibility": "Public"})
                        ET.SubElement(gen_target, "type", {"multiplicity": "0..1"})
                        ET.SubElement(gen_target, "tags")
                        ET.SubElement(gen_conn, "properties", {
                            "ea_type": "Generalization",
                            "direction": "Source -> Destination",
                        })
                        ET.SubElement(gen_conn, "tags")

            # Attributter
            for slot in schema_class.attributes:
                target_cls = resolve_class_reference(
                    slot.range or "",
                    schema_class.package_path,
                    name_index,
                    schema_class.import_paths,
                )
                if target_cls is not None and not is_datatype_class(target_cls):
                    target_id = class_id_lookup.get(target_cls.package_path + (target_cls.name,))
                    if target_id:
                        inverse_slot = find_slot_by_name(target_cls, slot.inverse)
                        if slot.inverse and (not slot.primary_relation) and inverse_slot and inverse_slot.primary_relation:
                            continue

                        source_id = class_id_map[class_key]
                        source_name = schema_class.name
                        target_role_name = slot.name
                        source_role_name = slot.inverse
                        target_name = target_cls.name

                        owner_slot = slot
                        owner_multiplicity = slot_multiplicity(owner_slot)
                        inverse_multiplicity = slot_multiplicity(inverse_slot) if inverse_slot else "0..1"
                        source_multiplicity = "0..1"
                        target_multiplicity = owner_multiplicity

                        if slot.inverse and not slot.primary_relation:
                            source_id = target_id
                            source_name = target_cls.name
                            target_id = class_id_map[class_key]
                            target_role_name = slot.inverse
                            source_role_name = slot.name
                            target_name = schema_class.name
                            source_multiplicity = owner_multiplicity
                            target_multiplicity = inverse_multiplicity
                        elif slot.inverse:
                            source_multiplicity = inverse_multiplicity
                            target_multiplicity = owner_multiplicity

                        if slot.inverse:
                            endpoint_a = (source_id, source_role_name)
                            endpoint_b = (target_id, target_role_name)
                            canonical_key = tuple(sorted((endpoint_a, endpoint_b)))
                            if canonical_key in emitted_bidirectional_associations:
                                continue
                            emitted_bidirectional_associations.add(canonical_key)

                        assoc_id = make_id("ASC", "/".join(class_key), slot.name)
                        ET.SubElement(pkg_element, "packagedElement", {
                            f"{{{XMI_NS}}}type": "uml:Association",
                            f"{{{XMI_NS}}}id": assoc_id,
                            "visibility": "public",
                            "start": source_id,
                            "end": target_id,
                        })

                        source_doc = sanitize_attribute_text((slot.description or "").strip()) if slot.description else None
                        inverse_doc = sanitize_attribute_text((inverse_slot.description or "").strip()) if (inverse_slot and inverse_slot.description) else None
                        target_doc = inverse_doc if (slot.inverse and not slot.primary_relation) else source_doc
                        source_end_doc = source_doc if (slot.inverse and not slot.primary_relation) else inverse_doc

                        assoc_conn = ET.SubElement(ext_connectors, "connector", {
                            f"{{{XMI_NS}}}type": "uml:Association",
                            f"{{{XMI_NS}}}idref": assoc_id,
                            "idref": assoc_id,
                            "start": source_id,
                            "end": target_id,
                        })
                        assoc_source = ET.SubElement(assoc_conn, "source", {
                            f"{{{XMI_NS}}}idref": source_id,
                            "idref": source_id,
                        })
                        ET.SubElement(assoc_source, "model", {"type": "Class", "name": source_name})
                        source_role_attrs = {"visibility": "Public"}
                        if source_role_name:
                            source_role_attrs["name"] = source_role_name
                        ET.SubElement(assoc_source, "role", source_role_attrs)
                        ET.SubElement(assoc_source, "type", {"multiplicity": source_multiplicity})
                        if source_end_doc:
                            ET.SubElement(assoc_source, "documentation", {"value": source_end_doc})
                        ET.SubElement(assoc_source, "tags")

                        assoc_target = ET.SubElement(assoc_conn, "target", {
                            f"{{{XMI_NS}}}idref": target_id,
                            "idref": target_id,
                        })
                        ET.SubElement(assoc_target, "model", {"type": "Class", "name": target_name})
                        ET.SubElement(assoc_target, "role", {
                            "name": target_role_name,
                            "visibility": "Public",
                        })
                        ET.SubElement(assoc_target, "type", {"multiplicity": target_multiplicity})
                        if target_doc:
                            ET.SubElement(assoc_target, "documentation", {"value": target_doc})
                        ET.SubElement(assoc_target, "tags")

                        ET.SubElement(assoc_conn, "properties", {
                            "ea_type": "Association",
                            "direction": "Bi-Directional" if slot.inverse else "Source -> Destination",
                        })
                        ET.SubElement(assoc_conn, "tags")
                        continue

                attr_id = make_id("PRP", "/".join(class_key), slot.name)
                attr_el = ET.SubElement(class_el, "ownedAttribute", {
                    f"{{{XMI_NS}}}type": "uml:Property",
                    f"{{{XMI_NS}}}id": attr_id,
                    "name": slot.name,
                    "visibility": "public",
                })

                set_slot_type(attr_el, slot, schema_class, class_id_lookup, name_index)

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
                    "idref": attr_id,
                    "name": slot.name,
                })
                ET.SubElement(attr_ext, "properties", {
                    "type": slot_type_name(slot),
                })
                ET.SubElement(attr_ext, "bounds", {
                    "lower": lower_value,
                    "upper": "*" if slot.multivalued else "1",
                })
                ET.SubElement(attr_ext, "stereotype", {"stereotype": "writable" if slot.writeable else ""})
                if slot.description:
                    ET.SubElement(attr_ext, "documentation", {
                        "value": sanitize_attribute_text(slot.description),
                    })
                attr_tags = ET.SubElement(attr_ext, "tags")
                append_deprecated_tag(attr_tags, slot.deprecated)

    indent(root)
    return ET.ElementTree(root)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a UML XMI 2.1 model from LinkML YAML schemas.")
    parser.add_argument("--src", default="src", help="Directory containing LinkML YAML schemas (default: src)")
    parser.add_argument("--out", default="FINT-informasjonsmodell.xml", help="Output XMI file path")

    args = parser.parse_args()
    src_dir = Path(args.src)
    if not src_dir.exists():
        raise SystemExit(f"Source directory {src_dir} does not exist")

    classes, name_index = collect_classes(src_dir)
    if not classes:
        raise SystemExit("No classes found in provided LinkML sources")

    apply_default_stereotypes(classes, name_index)

    tree = build_xmi(classes, name_index)
    tree.write(args.out, encoding="windows-1252", xml_declaration=True)
    print(f"Wrote XMI to {args.out}")


if __name__ == "__main__":
    main()
