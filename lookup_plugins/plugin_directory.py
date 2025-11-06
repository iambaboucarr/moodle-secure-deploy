DOCUMENTATION = """
name: plugin_directory
author: Geoffrey Bernardo van Wyk, Baboucarr Ceesay
version_added: 1.1.0
short_description: Path to plugin installation directory
description:
  - Computes the path to a Moodle plugin's installation directory from its frankenstyle name.
options:
  frankenstyle_name:
    description:
      - The plugin frankenstyle name, e.g. 'block_xp'.
    type: str
    required: true
"""

RETURN = """
  _raw:
    description:
      - A single-element list containing the relative path to the plugin's installation directory.
    type: list
    elements: str
"""

from ansible.errors import AnsibleLookupError
from ansible.plugins.lookup import LookupBase


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        directory_per_plugin_type = {
            "antivirus": "lib/antivirus",
            "assignfeedback": "mod/assign/feedback",
            "assignsubmission": "mod/assign/submission",
            "atto": "lib/editor/atto/plugins",
            "availability": "availability/condition",
            "block": "blocks",
            "booktool": "mod/book/tool",
            "customfield": "customfield/field",
            "datafield": "mod/data/field",
            "enrol": "enrol",
            "fileconverter": "files/converter",
            "filter": "filter",
            "format": "course/format",
            "local": "local",
            "logstore": "admin/tool/log/store",
            "mlbackend": "lib/mlbackend",
            "mod": "mod",
            "profilefield": "user/profile/field",
            "qbank": "question/bank",
            "qbehaviour": "question/behaviour",
            "qformat": "question/format",
            "qtype": "question/type",
            "repository": "repository",
            "theme": "theme",
            "tiny": "lib/editor/tiny/plugins",
            "tool": "admin/tool",
        }

        self.set_options(var_options=variables, direct=kwargs)
        frankenstyle_name = str(self.get_option("frankenstyle_name"))
        try:
            plugin_type, plugin_name = frankenstyle_name.split("_", maxsplit=1)
        except ValueError:
            raise AnsibleLookupError("Invalid frankenstyle name")

        plugin_type = plugin_type.strip()
        if plugin_type not in directory_per_plugin_type.keys():
            raise AnsibleLookupError("Invalid plugin type")

        plugin_name = plugin_name.strip()
        if len(plugin_name) == 0:
            raise AnsibleLookupError("Invalid plugin name")

        return [directory_per_plugin_type[plugin_type] + "/" + plugin_name]


