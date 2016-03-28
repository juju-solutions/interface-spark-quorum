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

from charms.reactive import RelationBase, hook, scopes


class SparkPeers(RelationBase):
    scope = scopes.UNIT

    @hook('{peers:spark-quorum}-relation-joined')
    def joined(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.departed')
        conv.set_state('{relation_name}.joined')

    @hook('{peers:spark-quorum}-relation-departed')
    def departed(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.joined')
        conv.set_state('{relation_name}.departed')

    def get_nodes(self):
        nodes = []
        for conv in self.conversations():
            nodes.append((conv.scope, conv.get_remote('private-address')))

        return nodes
