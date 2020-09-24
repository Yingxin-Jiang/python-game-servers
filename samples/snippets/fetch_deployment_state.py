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

"""Google Cloud Game Servers sample for getting a game server deployment.

Example usage:
    python fetch_deployment_state.py --project-id <project-id> --deployment-id <deployment-id>
"""

import argparse

from google.cloud import gaming
from google.cloud.gaming_v1.types import game_server_deployments


# [START cloud_game_servers_fetch_deployment_state]
def fetch_deployment_state(project_id, deployment_id):
    """Fetch the state of a game server deployment."""

    client = gaming.GameServerDeploymentsServiceClient()

    # Location is hard coded as global, as game server deployments can
    # only be created in global.  This is done for all operations on
    # game server deployments, as well as for its child resource types.
    request = game_server_deployments.FetchDeploymentStateRequest(
        name=f"projects/{project_id}/locations/global/gameServerDeployments/{deployment_id}",
    )

    response = client.fetch_deployment_state(request)
    print(f"Fet deployment state response:\n{response}")
    return response
# [END cloud_game_servers_fetch_deployment_state]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--project-id', help='Your cloud project ID.', required=True)
    parser.add_argument('--deployment-id', help='Your game server deployment ID.', required=True)

    args = parser.parse_args()

    fetch_deployment_state(args.project_id, args.deployment_id)
