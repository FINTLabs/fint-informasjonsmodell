#!/usr/bin/env python3
"""Lag et nytt LinkML-repo med én commit per ordinære release.

Kjør: .venv/bin/python scripts/migrate_to_linkml_repo.py --source .
Krever git, autentisert gh og PyYAML. Kilderepoet brukes bare til lesing.
Skriptet spør før det sletter det lokale målrepoet og før det publiserer.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

GITHUB_REPO = 'FINTLabs/fint-informasjonsmodell-linkml'
GITHUB_URL = f'https://github.com/{GITHUB_REPO}.git'


def run(*args, cwd=None, env=None):
    return subprocess.check_output(args, cwd=cwd, env=env)


def confirm(question):
    try:
        return input(f'{question} [y/N]: ').strip().lower() == 'y'
    except (EOFError, KeyboardInterrupt):
        return False


def prepare_target(target):
    if target.is_symlink():
        raise SystemExit('Target must not be a symlink.')
    if not target.exists():
        return True
    if not target.is_dir() or target.is_mount():
        raise SystemExit('Target must be a regular directory, not a mount point.')
    print(f'\nMappen finnes allerede: {target}')
    print('Hele mappen, inkludert lokal Git-historikk og ulagrede endringer, blir slettet.')
    if not confirm('Slette mappen og bygge på nytt?'):
        print('\nAvbrutt. Eksisterende repo er beholdt.')
        return False
    shutil.rmtree(target)
    print(f'Slettet {target}. Lokale endringer kan ikke gjenopprettes av skriptet.')
    return True


def publish(target, releases):
    # Repoet er nyopprettet og har ingen remote fra før.
    run('git', 'remote', 'add', 'origin', GITHUB_URL, cwd=target)
    run('git', 'fetch', 'origin', cwd=target)

    remote_main = run('git', 'ls-remote', GITHUB_URL, 'refs/heads/main', cwd=target)
    remote_commit = remote_main.decode().split()[0] if remote_main else ''
    local_commit = run('git', 'rev-parse', 'main', cwd=target).decode().strip()
    remote_tags = {}
    for line in run('git', 'ls-remote', '--tags', '--refs', GITHUB_URL, cwd=target).decode().splitlines():
        commit, ref = line.split()
        remote_tags[ref] = commit

    print(f'\nPublisering til {GITHUB_URL}')
    print(f'Erstatter main ({remote_commit or "finnes ikke"}) med {local_commit}.')
    print(f'Oppretter eller oppdaterer også {len(releases)} versjonstagger og GitHub-releaser.')
    if not confirm('Publisere main, tagger og releasenotater på GitHub?'):
        print('Publisering avbrutt. Det lokale repoet er beholdt.')
        return

    # Stopp hvis noen har endret GitHub sin main mens vi ventet på bekreftelse.
    leases = [f'--force-with-lease=refs/heads/main:{remote_commit}']
    refspecs = [f'{local_commit}:refs/heads/main']
    for release in releases:
        ref = f"refs/tags/{release['tag_name']}"
        leases.append(f'--force-with-lease={ref}:{remote_tags.get(ref, "")}')
        refspecs.append(f"{release['commit']}:{ref}")
    # Main og de migrerte taggene oppdateres samlet, eller ikke i det hele tatt.
    subprocess.run(['git', 'push', '--atomic', *leases, GITHUB_URL, *refspecs],
                   cwd=target, check=True)
    publish_releases(target, releases)


def prepare_release_notes(target, releases):
    notes_dir = target / '.git' / 'release-notes'
    notes_dir.mkdir(exist_ok=True)
    previous_commit = '-'
    for index, release in enumerate(releases):
        notes_file = notes_dir / f'{index}.md'
        run(sys.executable, 'scripts/generate_release_notes.py',
            previous_commit, release['commit'], '--repo', str(target),
            '--output', str(notes_file), cwd=target)
        original_url = release['html_url']
        original_link = f"Migrert fra [original release {release['tag_name']}]({original_url}) i fint-informasjonsmodell.\n\n"
        notes_file.write_text(original_link + notes_file.read_text())
        release['notes_file'] = str(notes_file)
        previous_commit = release['commit']


def publish_releases(target, releases):
    pages = json.loads(run('gh', 'api', '--paginate', '--slurp',
                          f'repos/{GITHUB_REPO}/releases'))
    existing_tags = {release['tag_name'] for page in pages for release in page}
    for release in releases:
        tag = release['tag_name']
        action = 'edit' if tag in existing_tags else 'create'
        print(f'Publiserer release {tag}', flush=True)
        command = ['gh', 'release', action, tag, '--repo', GITHUB_REPO,
                   '--title', tag, '--notes-file', release['notes_file']]
        if action == 'create':
            command.append('--verify-tag')
        else:
            command.extend(['--draft=false', '--prerelease=false'])
        run(*command, cwd=target)


def show_plan(source, target):
    print(f'Kilde: {source}\nLokalt mål: {target}')
    print('Dette skal skje:')
    print('1. Slett eksisterende fint-linkml etter bekreftelse, og opprett repoet på nytt.')
    print('2. Ordinære releaser konverteres fra EA til LinkML og tilbake til XMI (uten pre-releases).')
    print('3. Det opprettes én lokal commit per release, med README-LinkML.md som README.md.')
    print('4. Etterpå vil du få spørsmål om å publisere til https://github.com/FINTLabs/fint-informasjonsmodell-linkml.')
    print('   Bekreftelsen omfatter main, versjonstagger og releaser med genererte notater og lenke til originalreleasen.')
    print('Bekreft med y og Enter. Enter, andre svar eller Ctrl+C avbryter.\n')


def initialize_repo(source, target):
    run('git', 'init', '-b', 'main', str(target))
    (target / 'scripts').mkdir(exist_ok=True)
    for name in ('generate_linkml_from_xmi.py', 'generate_xmi_from_linkml.py', 'generate_release_notes.py'):
        shutil.copyfile(source / 'scripts' / name, target / 'scripts' / name)
    (target / '.gitattributes').write_text('FINT-informasjonsmodell-ea.xml -text\n')
    (target / '.gitignore').write_text('release.json\n')
    shutil.copyfile(source / 'README-LinkML.md', target / 'README.md')
    shutil.copyfile(source / '.linkmllint.yaml', target / '.linkmllint.yaml')


def fetch_releases():
    response = run('gh', 'api', '--paginate', '--slurp',
                   'repos/FINTLabs/fint-informasjonsmodell/releases')
    releases = []
    for page in json.loads(response):
        for release in page:
            if not release['draft'] and not release['prerelease']:
                releases.append(release)
    return sorted(releases, key=lambda release: (release['published_at'], release['id']))


def convert_release(source, target, release):
    tag = release['tag_name']
    # Hent filinnholdet direkte fra release-taggen, uten å bytte branch i kilderepoet.
    original = run('git', 'show', f'refs/tags/{tag}:FINT-informasjonsmodell.xml', cwd=source)
    (target / 'FINT-informasjonsmodell-ea.xml').write_bytes(original)

    # Pakker som ble slettet mellom releaser må også forsvinne fra LinkML.
    if (target / 'src').exists():
        shutil.rmtree(target / 'src')
    run(sys.executable, 'scripts/generate_linkml_from_xmi.py',
        '--xmi', 'FINT-informasjonsmodell-ea.xml', '--out', 'src', cwd=target)
    run(sys.executable, 'scripts/generate_xmi_from_linkml.py',
        '--src', 'src', '--out', 'FINT-informasjonsmodell.xml', cwd=target)
    verify_conversion(target)


def verify_conversion(target):
    import yaml

    linkml_classes = 0
    for schema_file in (target / 'src').glob('*.yaml'):
        schema = yaml.safe_load(schema_file.read_text())
        linkml_classes += len(schema.get('classes', {}))

    xmi_classes = 0
    xml = ET.parse(target / 'FINT-informasjonsmodell.xml')
    for element in xml.iter('packagedElement'):
        if element.get('{http://schema.omg.org/spec/XMI/2.1}type') == 'uml:Class':
            xmi_classes += 1

    if not linkml_classes or linkml_classes != xmi_classes:
        raise SystemExit(f'Ulikt antall klasser i LinkML og XMI: {linkml_classes}/{xmi_classes}')


def commit_release(target, release):
    run('git', 'add', '--', '.', cwd=target)
    # Bruk publiseringstidspunktet som dato for den nye commiten.
    env = os.environ.copy()
    env['GIT_AUTHOR_DATE'] = release['published_at']
    env['GIT_COMMITTER_DATE'] = release['published_at']
    # Behold én commit per release, også når modellinnholdet er identisk.
    run('git', 'commit', '--allow-empty',
        '-m', f"Import release {release['tag_name']}", cwd=target, env=env)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    source = parser.parse_args().source.resolve()
    target = source / 'fint-linkml'
    show_plan(source, target)
    releases = fetch_releases()
    if not prepare_target(target):
        return
    initialize_repo(source, target)
    for index, release in enumerate(releases, 1):
        print(f"[{index}/{len(releases)}] {release['tag_name']}", flush=True)
        convert_release(source, target, release)
        commit_release(target, release)
        release['commit'] = run('git', 'rev-parse', 'HEAD', cwd=target).decode().strip()
    print(f'Complete: {len(releases)} releases in {target}', flush=True)
    prepare_release_notes(target, releases)
    publish(target, releases)


if __name__ == '__main__':
    main()
