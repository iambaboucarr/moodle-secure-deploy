DOCUMENTATION = """
name: php_version
author: Geoffrey Bernardo van Wyk, Baboucarr Ceesay
version_added: 1.1.0
short_description: Latest PHP version compatible with given Moodle version
description:
  - Retrieves the latest PHP version compatible with the given Moodle version.
options:
  moodle_version:
    description:
      - The Moodle version for which to retrieve the PHP version.
    type: str
    required: true
    choices: ['3.9', '3.10', '3.11', '4.0', '4.1', '4.2', '4.3', '4.4', '5.1']
"""

RETURN = """
  _raw:
    description:
      - A single-element list containing a PHP version.
    type: list
    elements: str
"""

from ansible.errors import AnsibleLookupError
from ansible.plugins.lookup import LookupBase


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        php_per_moodle = {
            "3.9": ["7.4"],
            "3.10": ["7.4"],
            "3.11": ["8.0"],
            "4.0": ["8.0"],
            "4.1": ["8.1"],
            "4.2": ["8.2"],
            "4.3": ["8.2"],
            "4.4": ["8.3"],
            "5.1": ["8.4"],
        }

        self.set_options(var_options=variables, direct=kwargs)
        moodle_version = self.get_option("moodle_version")

        if moodle_version not in php_per_moodle.keys():
            raise AnsibleLookupError("Unknown Moodle version")

        return php_per_moodle[moodle_version]


