#!/usr/bin/env python3
# Copyright (C) 2017  Ghent University
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from charmhelpers.core.hookenv import status_set, log
from charms.reactive import when, when_not, set_state, remove_state
from charms.layer.externalservicehelpers import configure_headless_service


@when_not('mongodb.connected')
def no_mongodb_connected():
    status_set('blocked', 'Please connect the application to Mongodb.')


@when('mongodb.connected')
@when_not('k8s-external-mongodb.requested')
def mongodb_connected(mongodb):
    status_set('maintenance', 'Mongodb connection found.')
    connection_info = mongodb.connection_string()
    if connection_info:
        hostname, port = connection_info.split(':')
        configure_headless_service([hostname], port)
        set_state('k8s-external-mongodb.requested')


@when('mongodb-service.available', 'kubernetes-deployer.available')
def service_requested(service, deployer):
    service.send_service_name(unitdata.kv().get('service_name', ''))


@when('mongodb-service.available')
@when_not('kubernetes-deployer.available')
def service_requested(service):
    service.send_service_name('')
