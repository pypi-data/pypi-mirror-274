import argparse
from . import __version__ as version
from .core import hello_world, run_ansible_playbook

def main():
    parser = argparse.ArgumentParser(description='rikibot Command Line Tool')

    # Add a version argument
    parser.add_argument('--version', action='version', version=f'%(prog)s {version}')

    subparsers = parser.add_subparsers(dest='command')

    # Deploy command
    parser_deploy = subparsers.add_parser('deploy', help='Deploy a specific playbook')
    parser_deploy.add_argument('playbook', help='Name of the playbook to deploy')

    args = parser.parse_args()

    if args.command == 'deploy':
        run_ansible_playbook(args.playbook)
    else:
        print(hello_world())

if __name__ == "__main__":
    main()
