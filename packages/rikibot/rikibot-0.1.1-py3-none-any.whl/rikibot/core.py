import configparser
import os
import subprocess

def load_config():
    config = configparser.ConfigParser()
    config.read(os.path.expanduser('~/.rikibot.rc'))
    return config

def run_ansible_playbook(playbook_name):
    config = load_config()
    playbook_dir = config['ansible']['playbook_dir']
    playbook_path = os.path.join(playbook_dir, f'{playbook_name}.yml')

    command = ['ansible-playbook', playbook_path, '--ask-vault-pass']
    subprocess.run(command)

def hello_world():
    return "Hello, world from rikibot!"
