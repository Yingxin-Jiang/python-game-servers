# Copyright 2020, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.api_core import exceptions

import pytest

import create_cluster
import create_realm
import delete_cluster
import delete_realm
import get_cluster
import get_realm
import list_clusters
import list_realms
import update_cluster
import update_realm

PROJECT_ID = "gcgs-client-lib-samples-python"
LOCATION_1 = "us-central1"
LOCATION_2 = "global"
REALM_ID_1 = "my-realm-1"
REALM_ID_2 = "my-realm-2"
CLUSTER_ID = "my-cluster"

GKE_CLUSTER_NAME = "projects/gcgs-client-lib-samples/locations/us-central1/clusters/gke-shared-default"


@pytest.fixture(scope="function", autouse=True)
def teardown():
    clean_up_realms_and_clusters(LOCATION_1)
    clean_up_realms_and_clusters(LOCATION_2)

    yield

    print("Cleaning up resources in teardown")
    clean_up_realms_and_clusters(LOCATION_1)
    clean_up_realms_and_clusters(LOCATION_2)


def clean_up_realms_and_clusters(location):
    # Delete any realms and game server clusters in the location.
    for realm in list_realms.list_realms(PROJECT_ID, location):
        realm_id = realm.name.rsplit('/', 1)[-1]
        delete_clusters_in_realm(location, realm_id)
        try:
            print(f"Deleting realm {realm_id}")
            delete_realm.delete_realm(PROJECT_ID, location, realm_id)
        except exceptions.NotFound:  # May have been in process
            pass


def delete_clusters_in_realm(location, realm_id):
    for cluster in list_clusters.list_clusters(PROJECT_ID, location, realm_id):
        cluster_id = cluster.name.rsplit('/', 1)[-1]
        print(f"Deleting game server cluster {cluster_id} in realm {realm_id}")
        try:
            delete_cluster.delete_cluster(PROJECT_ID, location, realm_id, cluster_id)
        except exceptions.NotFound:  # May have been in process
            pass


def test_realms():
    create_realm.create_realm(PROJECT_ID, LOCATION_1, REALM_ID_1)
    realm = get_realm.get_realm(PROJECT_ID, LOCATION_1, REALM_ID_1)
    assert realm.name == f"projects/{PROJECT_ID}/locations/{LOCATION_1}/realms/{REALM_ID_1}"

    realms = list_realms.list_realms(PROJECT_ID, LOCATION_1)
    assert len(realms) == 1

    update_realm.update_realm(PROJECT_ID, LOCATION_1, REALM_ID_1)
    realm = get_realm.get_realm(PROJECT_ID, LOCATION_1, REALM_ID_1)
    assert realm.labels == {"label-key-1": "label-value-1", "label-key-2": "label-value-2"}

    delete_realm.delete_realm(PROJECT_ID, LOCATION_1, REALM_ID_1)

    realms = list_realms.list_realms(PROJECT_ID, LOCATION_1)
    assert len(realms) == 0


def test_game_server_clusters():
    create_realm.create_realm(PROJECT_ID, LOCATION_2, REALM_ID_2)
    realm = get_realm.get_realm(PROJECT_ID, LOCATION_2, REALM_ID_2)
    assert realm.name == f"projects/{PROJECT_ID}/locations/{LOCATION_2}/realms/{REALM_ID_2}"

    create_cluster.create_cluster(PROJECT_ID, LOCATION_2, REALM_ID_2, CLUSTER_ID, GKE_CLUSTER_NAME)
    cluster = get_cluster.get_cluster(PROJECT_ID, LOCATION_2, REALM_ID_2, CLUSTER_ID)
    assert cluster.name == f"projects/{PROJECT_ID}/locations/{LOCATION_2}/realms/{REALM_ID_2}/gameServerClusters/{CLUSTER_ID}"

    clusters = list_clusters.list_clusters(PROJECT_ID, LOCATION_2, REALM_ID_2)
    assert len(clusters) == 1

    update_cluster.update_cluster(PROJECT_ID, LOCATION_2, REALM_ID_2, CLUSTER_ID)
    cluster = get_cluster.get_cluster(PROJECT_ID, LOCATION_2, REALM_ID_2, CLUSTER_ID)
    assert cluster.labels == {"label-key-1": "label-value-1", "label-key-2": "label-value-2"}

    delete_cluster.delete_cluster(PROJECT_ID, LOCATION_2, REALM_ID_2, CLUSTER_ID)
    clusters = list_clusters.list_clusters(PROJECT_ID, LOCATION_2, REALM_ID_2)
    assert len(clusters) == 0

    delete_realm.delete_realm(PROJECT_ID, LOCATION_2, REALM_ID_2)
    realms = list_realms.list_realms(PROJECT_ID, LOCATION_2)
    assert len(realms) == 0
