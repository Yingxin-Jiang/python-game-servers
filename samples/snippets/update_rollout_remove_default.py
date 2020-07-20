#!/usr/bin/env python

# Copyright 2020 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Game Servers sample for updating the rollout of a Game Server
Deployment to remove the default config.

Example usage:
    python update_rollout_remove_default.py --project-id <project-id> --deployment-id <deployment-id>
"""

import argparse

from google.cloud import gaming
from google.cloud.gaming_v1.types import game_server_deployments
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore

import wait_for_operation

# [START gaming_update_rollout_remove_default]


def update_rollout_remove_default(project_id, deployment_id):
    """Creates a game server deployment."""

    client = gaming.GameServerDeploymentsServiceClient()

    # Location is hard coded as global, as Game Server Deployments can
    # only be created in global.  This is done for all operations on
    # Game Server Deployments, as well as for its child resource types.
    request = game_server_deployments.UpdateGameServerDeploymentRolloutRequest()
    request.rollout.name = f"projects/{project_id}/locations/global/gameServerDeployments/{deployment_id}"
    request.rollout.default_game_server_config = ""
    request.update_mask = field_mask.FieldMask(paths=["default_game_server_config"])

    response = client.update_game_server_deployment_rollout(request)
    print(f"Update deployment rollout operation: {response.operation.name}")
    wait_for_operation.wait_for_operation(client._transport.operations_client, response.operation.name)
# [END gaming_update_rollout_remove_default]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--project-id', help='Your cloud project ID.', required=True)
    parser.add_argument('--deployment-id', help='Your game server deployment ID.', required=True)

    args = parser.parse_args()

    update_rollout_remove_default(args.project_id, args.deployment_id)