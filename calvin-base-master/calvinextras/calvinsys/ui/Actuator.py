# -*- coding: utf-8 -*-

# Copyright (c) 2017 Ericsson AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import calvin.runtime.south.calvinsys.ui.uicalvinsys as ui
from calvin.runtime.south.calvinsys import base_calvinsys_object


class Actuator(base_calvinsys_object.BaseCalvinsysObject):
    """
    Actuator - Virtual actuator device.
    """

    init_schema = {
        "type": "object",
        "properties": {
            "ui_def": {
                "description": "Visual appearance",
                "type": "object",
            }
        },
        "description": "Initialize virtual device"
    }

    can_write_schema = {
        "description": "Returns True if data can be written, otherwise False",
        "type": "boolean"
    }

    write_schema = {
        "description": "Set output state",
    }

    def init(self, ui_def=None, **kwargs):
        ui.register_actuator(self.actor, ui_def)

    def can_write(self):
        return True

    def write(self, value):
        ui.update_ui(self.actor, value)

    def close(self):
        # FIXME: Handle close
        pass
