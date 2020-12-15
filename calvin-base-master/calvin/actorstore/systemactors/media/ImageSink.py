# -*- coding: utf-8 -*-

# Copyright (c) 2016-17 Ericsson AB
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


from calvin.actor.actor import Actor, manage, condition, stateguard, calvinsys
from calvin.utilities.calvinlogger import get_actor_logger

_log = get_actor_logger(__name__)

class ImageSink(Actor):

    """
    Incoming tokens, as base64 endoded images, sent to renderer.

    Inputs:
      b64image: base64 encoded jpg
    """

    @manage(exclude=["_sink"])
    def init(self):
        self.setup()

    def setup(self):
        self._sink = calvinsys.open(self, "image.render")

    def did_migrate(self):
        self.setup()

    def will_end(self):
        calvinsys.close(self._sink)

    @stateguard(lambda self: calvinsys.can_write(self._sink))
    @condition(action_input=['b64image'])
    def render_image(self, image):
        calvinsys.write(self._sink, image)


    action_priority = (render_image, )
    requires = ['image.render']


    test_calvinsys = {'image.render': {'write': ["dummy_data"]}}
    test_set = [
        {
            'inports': {'b64image': ["dummy_data"]},
        }
    ]
