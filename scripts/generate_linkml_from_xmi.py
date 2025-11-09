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

HEADER = "# yaml-language-server: $schema=https://w3id.org/linkml/meta.schema.json\n\n"


def slugify(s: str) -> str:
    # Preserve Scandinavian letters in a predictable way
    # æ -> a, ø -> o, å -> a (and uppercase variants)
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
    """Build maps for documentation texts using EA extension blocks and connectors.
    Returns (class_docs, attribute_docs, assoc_docs) mapping identifiers to doc strings.
    """
    class_docs = {}
    attr_docs = {}
    assoc_docs = {}
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
        # attributes for this element
        atts_block = el.find('attributes')
        if atts_block is not None:
            for att in atts_block.findall('attribute'):
                aid = att.get(f'{{{XMI_NS}}}idref')
                if not aid:
                    continue
                adoc_el = att.find('documentation')
                if adoc_el is not None:
                    val = adoc_el.get('value')
                    if val:
                        attr_docs[aid] = sanitize_text(val.strip())
    # EA connector blocks frequently contain documentation for association ends (slots)
    for conn in root.findall('.//connector'):
        assoc_id = conn.get(f'{{{XMI_NS}}}idref') or conn.get('xmi:idref')
        if not assoc_id:
            continue
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
            doc_el = node.find('documentation')
            if doc_el is None:
                continue
            val = doc_el.get('value')
            if val:
                assoc_docs[(assoc_id, role_name)] = sanitize_text(val.strip())
    return class_docs, attr_docs, assoc_docs


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


def parse_attributes(cls_el: ET.Element, class_index, attr_docs=None, assoc_docs=None):
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
                # reference to a class
                ref = class_index.get(xmi_idref)
                if ref:
                    rng = ref['el'].get('name') or 'string'
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

        desc = None
        if attr_docs is not None:
            aid = a.get(f'{{{XMI_NS}}}id') or a.get(f'{{{XMI_NS}}}idref')
            if aid and aid in attr_docs:
                desc = attr_docs[aid]
        if not desc and assoc_docs is not None:
            assoc_id = a.get('association')
            if assoc_id:
                doc = assoc_docs.get((assoc_id, name))
                if doc:
                    desc = doc

        attrs.append({'name': name, 'range': rng, 'required': required, 'multivalued': multivalued, 'description': desc})
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
        rng = a['range']
        # if range is another class, try to find its package
        for cid, info in class_index.items():
            if info['el'].get('name') == rng:
                pkg = info['package']
                if pkg != self_package:
                    deps.add(pkg)
                break
    return deps


def emit_yaml_for_package(pkg_path, classes_for_pkg, class_index, outdir, overwrite=False, class_docs=None, attr_docs=None, assoc_docs=None):
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
    cls_elements.sort(key=lambda e: (e.get('name') or '').lower())
    deps = set()
    self_pkg_full = ('FINT',) + tuple(pkg_path)
    for cls_el in cls_elements:
        ainfo = parse_attributes(cls_el, class_index, attr_docs=attr_docs, assoc_docs=assoc_docs)
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
        if (cls_el.get('isAbstract') or '').lower() == 'true':
            lines.append('    abstract: true')
        isa = parse_is_a(cls_el, class_index)
        if isa:
            lines.append(f'    is_a: {isa}')
        attrs = parse_attributes(cls_el, class_index, attr_docs=attr_docs, assoc_docs=assoc_docs)
        if attrs:
            lines.append('    attributes:')
            for a in attrs:
                lines.append(f'      {a["name"]}:')
                lines.append(f'        range: {a["range"]}')
                if a.get('description'):
                    append_description(lines, 8, a['description'])
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
    ap.add_argument('--xmi', default='FINT-informasjonsmodell.xml', help='Path to XMI file')
    ap.add_argument('--out', default='src', help='Output directory for YAML files')
    ap.add_argument('--overwrite', action='store_true', help='Overwrite existing YAML files')
    args = ap.parse_args()

    root = read_xml(args.xmi)
    class_docs, attr_docs, assoc_docs = build_doc_indexes(root)
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
