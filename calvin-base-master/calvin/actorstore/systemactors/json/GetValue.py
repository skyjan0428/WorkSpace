# -*- coding: utf-8 -*-

# Copyright (c) 2015 Ericsson AB
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

# encoding: utf-8

from calvin.actor.actor import Actor, manage, condition, stateguard
from calvin.runtime.north.calvin_token import EOSToken, ExceptionToken


class GetValue(Actor):

    """
    Extract a value from a container using key/index

    If container is a list then the key must be an integer index (zero-based), or a list of indices if for nested lists.
    If container is a dictionary the key must be a string or list of (string) keys for nested dictionaries.
    It is OK to make a key list of mixed strings and integers if the container comprises nested dictionaries and lists.
    Produce an ExceptionToken if mapping between key and (sub-)container is incorrect, or if a  integer index is out of range, or key is not present in dictionary.

    Inputs:
      container: a dictionary, list or a nested mix of them
      key:  index (integer), key (string), or a (possibly mixed) list for nested containers
    Outputs:
      value: value for the key/index/list
    """

    def exception_handler(self, action, args):
        return (ExceptionToken(),)

    @manage()
    def init(self):
        pass

    def _check_type_mismatch(self, container, key):
        t_cont = type(container)
        t_key = type(key)
        mismatch = (t_cont is list and t_key is not int) or (t_cont is dict and not isinstance(key, basestring))
        if mismatch:
            raise Exception()

    def _get_value(self, data, key):
        keylist = key if type(key) is list else [key]
        try:
            res = data
            for key in keylist:
                self._check_type_mismatch(res, key)
                res = res[key]
        except Exception as e:
            res = ExceptionToken()
        return res

    @condition(['container', 'key'], ['value'])
    def get_value(self, data, key):
        res = self._get_value(data, key)
        return (res, )

    action_priority = (get_value, )


    test_set = [
        {
            'inports': {'container': [{"a":1}], 'key':["a"]},
            'outports': {'value': [1]},
        },
        {
            'inports': {'container': [{"a":{"b":2}}]*3, 'key':["a", ["a"], ["a", "b"]]},
            'outports': {'value': [{"b":2}, {"b":2}, 2]},
        },
        {
            'inports': {'container': [[1,2,3]], 'key':[1]},
            'outports': {'value': [2]},
        },
        {
            'inports': {'container': [[{"a":{"b":2}}, 0]]*3, 'key':[1, [1], [0, "a", "b"]]},
            'outports': {'value': [0, 0, 2]},
        },
        # Error conditions
        {
            'inports': {'container': [1], 'key':["a"]},
            'outports': {'value': ['Exception']},
        },
        {
            'inports': {'container': [{"b":2}], 'key':["a"]},
            'outports': {'value': ['Exception']},
        },
    ]
