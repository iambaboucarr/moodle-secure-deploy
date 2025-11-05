# Ansible Role for Secure Moodle Deployment

Based on the original [Ansible Role for Moodle](https://github.com/geoffreyvanwyk/ansible-role-moodle) by [Geoffrey van Wyk](https://github.com/geoffreyvanwyk).

Extended to for security and support for Moodle 5.1+
Deploys, installs, and upgrades [Moodle](https://moodle.org) on [Ubuntu](https://ubuntu.com) servers.

Additionally, extends Moodle by installing plugins from Git.

## How to use

```bash
ansible-galaxy install -r requirements.yml
ansible-playbook -i inventory.ini playbook.yml -K
```
