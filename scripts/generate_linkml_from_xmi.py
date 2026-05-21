#!/usr/bin/env python3
import argparse
import os
import sys
import unicodedata
import xml.etree.ElementTree as ET
from collections import defaultdict, OrderedDict
import re

UML_NS = 'http://schema.omg.org/spec/UML/2.1'
XMI_NS = 'http://schema.omg.org/spec/XMI/2.1'
NS = {'uml': UML_NS, 'xmi': XMI_NS}

PRIMITIVE_MAP = {
    'Boolean': 'boolean',
    'String': 'string',
    'Integer': 'integer',
    'UnlimitedNatural': 'integer',
    'Real': 'float',
    'Double': 'float',
    'Float': 'float',
    'Date': 'date',
    'Time': 'time',
    'DateTime': 'datetime',
}

EA_JAVA_PRIMITIVE_MAP = {
    'EAJava_string': 'string',
    'EAJava_int': 'integer',
    'EAJava_long': 'integer',
    'EAJava_float': 'float',
    'EAJava_boolean': 'boolean',
    'EAJava_date': 'date',
    'EAJava_datetime': 'datetime',
    'EAJava_dateTime': 'datetime',
    'EAnone_date': 'date',
    'EAnone_datetime': 'datetime',
    'EAnone_dateTime': 'datetime',
}

MODEL_PRIMITIVE_RANGE_MAP = {
    'string': 'string',
    'int': 'integer',
    'integer': 'integer',
    'long': 'integer',
    'float': 'float',
    'double': 'float',
    'boolean': 'boolean',
    'date': 'date',
    'datetime': 'datetime',
    'dateTime': 'datetime',
    'unlimitednatural': 'integer',
}

HEADER = "# yaml-language-server: $schema=https://w3id.org/linkml/meta.schema.json\n\n"


def slugify(s: str) -> str:
    trans = str.maketrans({
        'æ': 'a', 'Æ': 'A',
        'ø': 'o',  'Ø': 'O',
        'å': 'a',  'Å': 'A',
    })
    s = s.translate(trans)
    s = unicodedata.normalize('NFKD', s)
    s = s.encode('ascii', 'ignore').decode('ascii')
    s = s.lower().strip()
    s = s.replace('/', ' ').replace('\\', ' ')
    s = s.replace(' ', '-')
    s = s.replace('_', '-')
    while '--' in s:
        s = s.replace('--', '-')
    return s


def dotted_name(segments):
    return '.'.join(slugify(p) for p in segments)


def id_url(segments):
    return 'https://w3id.org/novari/fint/' + '/'.join(slugify(p) for p in segments)


def detect_declared_encoding(raw: bytes) -> str | None:
    # Look for <?xml ... encoding="..."?>
    head = raw[:256]
    m = re.search(br'encoding\s*=\s*"([A-Za-z0-9_\-]+)"', head)
    if m:
        try:
            return m.group(1).decode('ascii').lower()
        except Exception:
            return None
    return None


def read_xml(path: str) -> ET.Element:
    with open(path, 'rb') as f:
        raw = f.read()
    enc = detect_declared_encoding(raw)
    tried = []
    for codec in ([enc] if enc else []) + ['utf-8', 'cp1252', 'latin-1']:
        if not codec:
            continue
        if codec in tried:
            continue
        tried.append(codec)
        try:
            data = raw.decode(codec)
            return ET.fromstring(data)
        except Exception:
            continue
    # last resort
    data = raw.decode('latin-1', errors='ignore')
    return ET.fromstring(data)


def sanitize_text(text: str) -> str:
    if text is None:
        return text
    # Normalize newlines
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    # Replace Cc control chars (except tab/newline) with space
    cleaned = []
    for ch in text:
        if ch in ('\n', '\t'):
            cleaned.append(ch)
        elif unicodedata.category(ch).startswith('C'):
            cleaned.append(' ')
        else:
            cleaned.append(ch)
    return ''.join(cleaned)


def build_doc_indexes(root: ET.Element):
    """Build maps for documentation and deprecation texts using EA extension blocks and connectors."""
    class_docs = {}
    class_stereotypes = {}
    attr_docs = {}
    assoc_docs = {}
    class_deprecated = {}
    attr_deprecated = {}
    assoc_deprecated = {}
    assoc_role_deprecated = {}
    assoc_inverse = {}
    assoc_source_class = {}
    attr_writeable = {}
    attr_model_type = {}
    # EA stores extra info in non-namespaced blocks <element>, <attributes>/<attribute>
    for el in root.findall('.//element'):
        xmi_type = el.get(f'{{{XMI_NS}}}type')
        xmi_idref = el.get(f'{{{XMI_NS}}}idref')
        if xmi_type == 'uml:Class' and xmi_idref:
            props = el.find('properties')
            if props is not None:
                doc = props.get('documentation')
                if doc:
                    class_docs[xmi_idref] = sanitize_text(doc.strip())
                stereotype = (props.get('stereotype') or '').strip().lower()
                if stereotype:
                    class_stereotypes[xmi_idref] = stereotype
        tag_block = el.find('tags')
        if tag_block is not None and xmi_idref:
            for tag in tag_block.findall('tag'):
                if (tag.get('name') or '').upper() == 'DEPRECATED':
                    text = extract_tag_text(tag)
                    if text:
                        class_deprecated[xmi_idref] = text
                        break
        # attributes for this element
        atts_block = el.find('attributes')
        if atts_block is not None:
            for att in atts_block.findall('attribute'):
                attr_ids = [att.get(f'{{{XMI_NS}}}id'), att.get(f'{{{XMI_NS}}}idref')]
                attr_ids = [aid for aid in attr_ids if aid]
                if not attr_ids:
                    continue
                adoc_el = att.find('documentation')
                if adoc_el is not None:
                    val = adoc_el.get('value')
                    if val:
                        cleaned = sanitize_text(val.strip())
                        for aid in attr_ids:
                            attr_docs[aid] = cleaned
                tag_block = att.find('tags')
                if tag_block is not None:
                    for tag in tag_block.findall('tag'):
                        if (tag.get('name') or '').upper() == 'DEPRECATED':
                            text = extract_tag_text(tag)
                            if text:
                                for aid in attr_ids:
                                    attr_deprecated[aid] = text
                                break
                stereotype = att.find('stereotype')
                if stereotype is not None and (stereotype.get('stereotype') or '').lower() == 'writable':
                    for aid in attr_ids:
                        attr_writeable[aid] = True
                props = att.find('properties')
                if props is not None:
                    model_type = props.get('type')
                    if model_type:
                        for aid in attr_ids:
                            attr_model_type[aid] = model_type
    # EA connector blocks frequently contain documentation for association ends (slots)
    for conn in root.findall('.//connector'):
        assoc_id = conn.get(f'{{{XMI_NS}}}idref') or conn.get('xmi:idref')
        if not assoc_id:
            continue
        props = conn.find('properties')
        direction = props.get('direction') if props is not None else None
        source_role_name = None
        target_role_name = None
        source_node = conn.find('source')
        if source_node is not None:
            source_id = source_node.get(f'{{{XMI_NS}}}idref') or source_node.get('idref')
            if source_id:
                assoc_source_class[assoc_id] = source_id
        tag_block = conn.find('tags')
        if tag_block is not None:
            for tag in tag_block.findall('tag'):
                if (tag.get('name') or '').upper() == 'DEPRECATED':
                    text = extract_tag_text(tag)
                    if text:
                        assoc_deprecated[assoc_id] = text
                        break
        for node_name in ('source', 'target'):
            node = conn.find(node_name)
            if node is None:
                continue
            role_el = node.find('role')
            if role_el is None:
                continue
            role_name = role_el.get('name')
            if not role_name:
                continue
            if node_name == 'source':
                source_role_name = role_name
            else:
                target_role_name = role_name
            doc_el = node.find('documentation')
            if doc_el is not None:
                val = doc_el.get('value')
                if val:
                    assoc_docs[(assoc_id, role_name)] = sanitize_text(val.strip())
            tag_block = node.find('tags')
            if tag_block is not None:
                for tag in tag_block.findall('tag'):
                    if (tag.get('name') or '').upper() == 'DEPRECATED':
                        text = extract_tag_text(tag)
                        if text:
                            assoc_role_deprecated[(assoc_id, role_name)] = text
                            break
        if direction == 'Bi-Directional' and source_role_name and target_role_name:
            assoc_inverse[(assoc_id, source_role_name)] = target_role_name
            assoc_inverse[(assoc_id, target_role_name)] = source_role_name
    return (
        class_docs,
        class_stereotypes,
        attr_docs,
        assoc_docs,
        class_deprecated,
        attr_deprecated,
        assoc_deprecated,
        assoc_role_deprecated,
        assoc_inverse,
        assoc_source_class,
        attr_writeable,
        attr_model_type,
    )


def get_class_doc(cls_el: ET.Element, class_docs: dict):
    cid = cls_el.get(f'{{{XMI_NS}}}id')
    if cid and cid in class_docs:
        return class_docs[cid]
    # fallback to ownedComment on UML class
    bodies = [oc.get('body') for oc in cls_el.findall('ownedComment') if oc.get('body')]
    if bodies:
        return sanitize_text('\n\n'.join(bodies).strip())
    return None


def append_description(lines: list, indent_spaces: int, text: str):
    """Append a YAML block scalar description at a given indentation."""
    if not text:
        return
    indent = ' ' * indent_spaces
    lines.append(f'{indent}description: |')
    for ln in text.splitlines():
        lines.append(f'{indent}  {ln}')


def append_deprecated(lines: list, indent_spaces: int, text: str):
    if not text:
        return
    indent = ' ' * indent_spaces
    stripped = text.strip()
    if '\n' in stripped:
        lines.append(f'{indent}deprecated: |')
        for ln in stripped.splitlines():
            lines.append(f'{indent}  {ln}')
    else:
        escaped = stripped.replace('\\', '\\\\').replace('"', '\\"')
        lines.append(f'{indent}deprecated: "{escaped}"')


def extract_tag_text(tag_el: ET.Element):
    if tag_el is None:
        return None
    for key in ('value', 'notes', 'memo'):
        val = tag_el.get(key)
        if val:
            cleaned = sanitize_text(val.strip())
            if cleaned:
                return cleaned
    return None


def find_fint_package(model_root: ET.Element) -> ET.Element:
    # In EA XMI the UML elements are encoded as <packagedElement xmi:type="uml:Package" ...>
    for pe in model_root.findall('packagedElement'):
        if pe.get(f'{{{XMI_NS}}}type') == 'uml:Package' and pe.get('name') == 'FINT':
            return pe
    # fallback: deep search
    for pe in model_root.findall('.//packagedElement'):
        if pe.get(f'{{{XMI_NS}}}type') == 'uml:Package' and pe.get('name') == 'FINT':
            return pe
    return None


def collect_packages(pkg_el: ET.Element, path_segments, class_index, package_classes):
    # Record all classes immediately inside this package
    for pe in pkg_el.findall('packagedElement'):
        xmi_type = pe.get(f'{{{XMI_NS}}}type')
        if xmi_type == 'uml:Class':
            cid = pe.get(f'{{{XMI_NS}}}id')
            if cid:
                class_index[cid] = {'el': pe, 'package': tuple(path_segments)}
                package_classes[tuple(path_segments)].append(cid)
        elif xmi_type == 'uml:Package':
            name = pe.get('name') or 'unnamed'
            collect_packages(pe, path_segments + [name], class_index, package_classes)
    return class_index, package_classes


def get_text(node: ET.Element, attr: str, default=None):
    v = node.get(attr)
    return v if v is not None else default


def map_primitive(href: str) -> str:
    # href usually like http://schema.omg.org/spec/UML/2.1/uml.xml#String
    if not href:
        return 'string'
    t = href.split('#')[-1]
    return PRIMITIVE_MAP.get(t, 'string')


def parse_attributes(
    cls_el: ET.Element,
    class_index,
    attr_docs=None,
    assoc_docs=None,
    attr_deprecated=None,
    assoc_deprecated=None,
    assoc_role_deprecated=None,
    assoc_inverse=None,
    assoc_source_class=None,
    attr_writeable=None,
    attr_model_type=None,
):
    attrs = []
    # owned attributes
    for a in cls_el.findall('ownedAttribute'):
        name = a.get('name')
        if not name:
            continue
        rng = 'string'
        # multiplicity
        required = False
        multivalued = False
        range_package = None
        lower = None
        upper = None
        lv = a.find('lowerValue')
        if lv is not None:
            lower = lv.get('value')
        uv = a.find('upperValue')
        if uv is not None:
            upper = uv.get('value')
            uv_type = uv.get(f'{{{XMI_NS}}}type')
        else:
            uv_type = None
        if lower is not None:
            try:
                required = int(lower) >= 1
            except Exception:
                required = False
        # multivalued if upper is '*' or > 1 or UnlimitedNatural
        if upper is not None:
            if upper in ('*', '-1'):
                multivalued = True
            else:
                try:
                    multivalued = int(upper) != 1
                except Exception:
                    multivalued = False
        if uv_type and uv_type.endswith('LiteralUnlimitedNatural'):
            multivalued = True
        # detect type
        t = a.find('type')
        if t is not None:
            href = t.get('href')
            xmi_idref = t.get(f'{{{XMI_NS}}}idref')
            xmi_type = t.get(f'{{{XMI_NS}}}type')
            if href:
                rng = map_primitive(href)
            elif xmi_idref:
                if xmi_idref in EA_JAVA_PRIMITIVE_MAP:
                    rng = EA_JAVA_PRIMITIVE_MAP[xmi_idref]
                elif xmi_idref.startswith('EAnone_'):
                    none_primitive = xmi_idref[len('EAnone_'):]
                    rng = MODEL_PRIMITIVE_RANGE_MAP.get(none_primitive, 'string')
                else:
                    ref = class_index.get(xmi_idref)
                    # reference to a class
                    if ref:
                        rng = ref['el'].get('name') or 'string'
                        range_package = ref['package']
                    else:
                        rng = 'string'
            elif xmi_type:
                # sometimes primitive has xmi:type only
                prim = xmi_type.split(':')[-1]
                rng = PRIMITIVE_MAP.get(prim, 'string')
        else:
            # some EA variants place type as attribute directly
            xmi_idref = a.get(f'{{{XMI_NS}}}idref')
            if xmi_idref and xmi_idref in class_index:
                rng = class_index[xmi_idref]['el'].get('name') or 'string'
                range_package = class_index[xmi_idref]['package']

        attr_ids = []
        for key in (f'{{{XMI_NS}}}id', f'{{{XMI_NS}}}idref'):
            val = a.get(key)
            if val:
                attr_ids.append(val)

        desc = None
        if attr_docs:
            for aid in attr_ids:
                if aid in attr_docs:
                    desc = attr_docs[aid]
                    break
        if not desc and assoc_docs is not None:
            assoc_id = a.get('association')
            if assoc_id:
                doc = assoc_docs.get((assoc_id, name))
                if doc:
                    desc = doc

        deprecated = None
        if attr_deprecated:
            for aid in attr_ids:
                if aid in attr_deprecated:
                    deprecated = attr_deprecated[aid]
                    break
        assoc_id = a.get('association')
        if not deprecated and assoc_id:
            if assoc_role_deprecated and (assoc_id, name) in assoc_role_deprecated:
                deprecated = assoc_role_deprecated[(assoc_id, name)]
            elif assoc_deprecated and assoc_id in assoc_deprecated:
                deprecated = assoc_deprecated[assoc_id]

        inverse = None
        if assoc_inverse is not None and assoc_id:
            inverse = assoc_inverse.get((assoc_id, name))

        writeable = False
        if attr_writeable:
            for aid in attr_ids:
                if attr_writeable.get(aid):
                    writeable = True
                    break

        model_primitive_type = None
        if attr_model_type:
            for aid in attr_ids:
                mt = attr_model_type.get(aid)
                if mt:
                    if mt in MODEL_PRIMITIVE_RANGE_MAP:
                        model_primitive_type = mt
                    break
        if model_primitive_type:
            mapped_range = MODEL_PRIMITIVE_RANGE_MAP.get(model_primitive_type)
            if mapped_range:
                rng = mapped_range

        primary_relation = False
        class_id = cls_el.get(f'{{{XMI_NS}}}id')
        if inverse and assoc_source_class is not None and assoc_id and class_id:
            primary_relation = assoc_source_class.get(assoc_id) == class_id

        attrs.append({
            'name': name,
            'range': rng,
            'range_package': range_package,
            'required': required,
            'multivalued': multivalued,
            'description': desc,
            'deprecated': deprecated,
            'inverse': inverse,
            'primary_relation': primary_relation,
            'writeable': writeable,
        })
    return attrs


def parse_is_a(cls_el: ET.Element, class_index):
    gen = cls_el.find('generalization')
    if gen is not None:
        sup = gen.get('general')
        if sup and sup in class_index:
            return class_index[sup]['el'].get('name')
    return None


def collect_dependencies(attrs, class_index, self_package):
    deps = set()
    for a in attrs:
        if a.get('range_package'):
            pkg = a['range_package']
            if pkg != self_package:
                deps.add(pkg)
            continue
        rng = a['range']
        # if range is another class, try to find its package
        for cid, info in class_index.items():
            if info['el'].get('name') == rng:
                pkg = info['package']
                if pkg != self_package:
                    deps.add(pkg)
                break
    return deps


def emit_yaml_for_package(
    pkg_path,
    classes_for_pkg,
    class_index,
    outdir,
    overwrite=False,
    class_docs=None,
    attr_docs=None,
    assoc_docs=None,
    class_deprecated=None,
    attr_deprecated=None,
    assoc_deprecated=None,
    assoc_role_deprecated=None,
    assoc_inverse=None,
    assoc_source_class=None,
    attr_writeable=None,
    attr_model_type=None,
    class_stereotypes=None,
):
    if not classes_for_pkg:
        return None
    name = dotted_name(pkg_path)
    file_name = name + '.yaml'
    target = os.path.join(outdir, file_name)
    if (not overwrite) and os.path.exists(target):
        return target  # skip

    lines = []
    lines.append(HEADER.rstrip('\n'))
    lines.append(f'id: {id_url(pkg_path)}')
    lines.append(f'name: {name}')
    base_imports = ['linkml:types']
    if pkg_path[0].lower() != 'felles':
        base_imports.extend(['felles.basisklasser', 'felles.komplekse-datatyper'])
    # Determine cross-package dependencies to include as imports
    cls_elements = [class_index[cid]['el'] for cid in classes_for_pkg]
    deps = set()
    self_pkg_full = ('FINT',) + tuple(pkg_path)
    for cls_el in cls_elements:
        ainfo = parse_attributes(
            cls_el,
            class_index,
            attr_docs=attr_docs,
            assoc_docs=assoc_docs,
            attr_deprecated=attr_deprecated,
            assoc_deprecated=assoc_deprecated,
            assoc_role_deprecated=assoc_role_deprecated,
            assoc_inverse=assoc_inverse,
            assoc_source_class=assoc_source_class,
            attr_writeable=attr_writeable,
            attr_model_type=attr_model_type,
        )
        deps |= collect_dependencies(ainfo, class_index, self_pkg_full)
        # also include superclass package deps
        gen = cls_el.find('generalization')
        if gen is not None:
            sup = gen.get('general')
            if sup and sup in class_index:
                dep_pkg = class_index[sup]['package']
                if dep_pkg != self_pkg_full:
                    deps.add(dep_pkg)
    imports = []
    seen_imports = set()
    for imp in base_imports:
        if imp not in seen_imports:
            imports.append(imp)
            seen_imports.add(imp)

    extra_imports = set()
    for dep in sorted(deps):
        if len(dep) < 2:
            continue
        top = (dep[1] or '').lower()
        if not top:
            continue
        if top.startswith('diagram') or top in {'model', 'diagram'}:
            continue
        dotted = dotted_name(dep[1:])
        if dotted == name:
            continue
        extra_imports.add(dotted)

    for imp in sorted(extra_imports):
        if imp not in seen_imports:
            imports.append(imp)
            seen_imports.add(imp)

    lines.append('imports:')
    for imp in imports:
        lines.append(f'  - {imp}')

    lines.append('')
    lines.append('classes:')
    lines.append('')

    for cls_el in cls_elements:
        cls_name = cls_el.get('name') or 'UnnamedClass'
        lines.append(f'  {cls_name}:')
        # description from EA docs/comments
        if class_docs is not None:
            cdesc = get_class_doc(cls_el, class_docs)
            if cdesc:
                append_description(lines, 4, cdesc)
        if class_deprecated:
            cid = cls_el.get(f'{{{XMI_NS}}}id')
            if cid and cid in class_deprecated:
                append_deprecated(lines, 4, class_deprecated[cid])
        cid = cls_el.get(f'{{{XMI_NS}}}id')
        class_stereotype = (class_stereotypes or {}).get(cid, '') if cid else ''
        if class_stereotype in {'referanse', 'datatype'}:
            linkml_stereotype = 'kompleks-datatype' if class_stereotype == 'datatype' else class_stereotype
            lines.append('    annotations:')
            lines.append(f'      stereotype: {linkml_stereotype}')
        if (cls_el.get('isAbstract') or '').lower() == 'true':
            lines.append('    abstract: true')
        isa = parse_is_a(cls_el, class_index)
        if isa:
            lines.append(f'    is_a: {isa}')
        attrs = parse_attributes(
            cls_el,
            class_index,
            attr_docs=attr_docs,
            assoc_docs=assoc_docs,
            attr_deprecated=attr_deprecated,
            assoc_deprecated=assoc_deprecated,
            assoc_role_deprecated=assoc_role_deprecated,
            assoc_inverse=assoc_inverse,
            assoc_source_class=assoc_source_class,
            attr_writeable=attr_writeable,
            attr_model_type=attr_model_type,
        )
        if attrs:
            lines.append('    attributes:')
            for a in attrs:
                lines.append(f'      {a["name"]}:')
                lines.append(f'        range: {a["range"]}')
                if a.get('inverse'):
                    lines.append(f'        inverse: {a["inverse"]}')
                if a.get('primary_relation') or a.get('writeable'):
                    lines.append('        annotations:')
                    if a.get('primary_relation'):
                        lines.append('          primaryRelation: true')
                    if a.get('writeable'):
                        lines.append('          writeable: true')
                if a.get('description'):
                    append_description(lines, 8, a['description'])
                if a.get('deprecated'):
                    append_deprecated(lines, 8, a['deprecated'])
                if a['multivalued']:
                    lines.append('        multivalued: true')
                if a['required']:
                    lines.append('        required: true')
        lines.append('')

    content = '\n'.join(lines).rstrip() + '\n'
    os.makedirs(outdir, exist_ok=True)
    with open(target, 'w', encoding='utf-8') as f:
        f.write(content)
    return target


def main():
    ap = argparse.ArgumentParser(description='Generate LinkML YAML files from FINT XMI 2.1 (EA export).')
    ap.add_argument('--xmi', default='FINT-informasjonsmodell-eap.xml', help='Path to XMI file')
    ap.add_argument('--out', default='src', help='Output directory for YAML files')
    ap.add_argument('--overwrite', action='store_true', help='Overwrite existing YAML files')
    args = ap.parse_args()

    root = read_xml(args.xmi)
    (
        class_docs,
        class_stereotypes,
        attr_docs,
        assoc_docs,
        class_deprecated,
        attr_deprecated,
        assoc_deprecated,
        assoc_role_deprecated,
        assoc_inverse,
        assoc_source_class,
        attr_writeable,
        attr_model_type,
    ) = build_doc_indexes(root)
    model = root.find('.//uml:Model', NS)
    if model is None:
        print('ERROR: Could not find uml:Model in XMI', file=sys.stderr)
        sys.exit(2)

    fint = find_fint_package(model)
    if fint is None:
        print('ERROR: Could not find FINT root package in XMI', file=sys.stderr)
        sys.exit(2)

    class_index = {}
    package_classes = defaultdict(list)  # pkg_path(tuple) -> [class_ids]

    collect_packages(fint, ['FINT'], class_index, package_classes)

    # Build list of all packages under FINT (excluding FINT itself)
    pkg_paths = sorted([p for p in package_classes.keys() if len(p) >= 2])

    # filter out meta/diagram packages
    def is_meta(path_tuple):
        parts = [x.lower() for x in path_tuple]
        return any(x.startswith('diagram') for x in parts) or parts[1] in {'model', 'diagram'}

    generated = []
    for pkg_path in pkg_paths:
        if is_meta(pkg_path):
            continue
        # file name and write
        out = emit_yaml_for_package(
            pkg_path[1:],
            package_classes[pkg_path],
            class_index,
            args.out,
            overwrite=args.overwrite,
            class_docs=class_docs,
            attr_docs=attr_docs,
            assoc_docs=assoc_docs,
            class_deprecated=class_deprecated,
            attr_deprecated=attr_deprecated,
            assoc_deprecated=assoc_deprecated,
            assoc_role_deprecated=assoc_role_deprecated,
            assoc_inverse=assoc_inverse,
            assoc_source_class=assoc_source_class,
            attr_writeable=attr_writeable,
            attr_model_type=attr_model_type,
            class_stereotypes=class_stereotypes,
        )
        if out:
            generated.append(out)

    if generated:
        print('Generated:')
        for g in generated:
            print(' -', g)
    else:
        print('No files generated (maybe all exist, or no classes found).')


if __name__ == '__main__':
    main()
