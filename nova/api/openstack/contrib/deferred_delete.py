# Copyright 2011 Openstack, LLC
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""The deferred instance delete extension."""

import webob

from nova import compute
from nova import log as logging
from nova.api.openstack import extensions
from nova.api.openstack import servers


LOG = logging.getLogger("nova.api.contrib.deferred-delete")


class Deferred_delete(extensions.ExtensionDescriptor):
    """Instance deferred delete"""

    name = "DeferredDelete"
    alias = "os-deferred-delete"
    namespace = "http://docs.openstack.org/ext/deferred-delete/api/v1.1"
    updated = "2011-09-01T00:00:00+00:00"

    def __init__(self, ext_mgr):
        super(Deferred_delete, self).__init__(ext_mgr)
        self.compute_api = compute.API()

    def _restore(self, input_dict, req, instance_id):
        """Restore a previously deleted instance."""

        context = req.environ["nova.context"]
        self.compute_api.restore(context, instance_id)
        return webob.Response(status_int=202)

    def _force_delete(self, input_dict, req, instance_id):
        """Force delete of instance before deferred cleanup."""

        context = req.environ["nova.context"]
        instance = self.compute_api.get(context, instance_id)
        self.compute_api.force_delete(context, instance)
        return webob.Response(status_int=202)

    def get_actions(self):
        """Return the actions the extension adds, as required by contract."""
        actions = [
            extensions.ActionExtension("servers", "restore",
                                       self._restore),
            extensions.ActionExtension("servers", "forceDelete",
                                       self._force_delete),
        ]

        return actions
