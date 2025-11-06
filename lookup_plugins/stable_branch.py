DOCUMENTATION = """
name: stable_branch
author: Geoffrey Bernardo van Wyk, Baboucarr Ceesay
version_added: 1.1.0
short_description: Stable branch for Moodle version
description:
  - Retrieves the name of the stable Git branch corresponding to the given Moodle version.
options:
  moodle_version:
    description:
      - Moodle version in the format x.y
    type: str
    required: true
"""

RETURN = """
  _raw:
    description:
      - A single-element list containing the name of a stable Git branch, e.g. ['MOODLE_403_STABLE'].
    type: list
    elements: str
"""

from ansible.errors import AnsibleLookupError
from ansible.plugins.lookup import LookupBase


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        moodle_version = str(self.get_option("moodle_version"))
        try:
            major_version, minor_version = moodle_version.split(".", maxsplit=1)
        except ValueError:
            raise AnsibleLookupError("Invalid moodle_version")

        if len(major_version) != 1:
            raise AnsibleLookupError("Invalid moodle_version")

        if len(minor_version) not in [1, 2]:
            raise AnsibleLookupError("Invalid moodle_version")

        branch_number = major_version + (
            minor_version if len(minor_version) == 2 else "0" + minor_version
        )

        return ["MOODLE_" + branch_number + "_STABLE"]


