from azure.ai.ml import command, PyTorchDistribution
from azure.ai.ml.entities import JupyterLabJobService, SshJobService, TensorBoardJobService, VsCodeJobService
from azure.ai.ml import MLClient
from azure.ai.ml.entities._assets.environment import Environment
from azure.identity import DefaultAzureCredential
from azureml.core import Workspace, Dataset
from azureml.core import ScriptRunConfig, Environment, Experiment, Workspace, Dataset, Model
from azureml.core.runconfig import PyTorchConfiguration
from azureml.core.conda_dependencies import CondaDependencies
from azureml.data import OutputFileDatasetConfig
from azureml.core.container_registry import ContainerRegistry
import json
import os
import shutil
from tqdm import tqdm
from multiprocessing import Pool
import re
import pandas as pd
from azure.ai.ml.entities._assets.environment import Environment

### resource definitions
subscription_id = os.getenv("SUBSCRIPTION_ID", default="a5025edd-be02-4cd9-b4e7-522a741254d0")
resource_group = os.getenv("RESOURCEGROUP_NAME", default="Orca-DNO")
workspace_name = os.getenv("WORKSPACE_NAME", default="Orca-SelfImprovingWS")
ws = Workspace(subscription_id = subscription_id, resource_group = resource_group, workspace_name = workspace_name)
vc = "baltic08" # please replace with your preferred VC
node_count = 1

### setup virtual cluster
vc_config = {
    "instance_type": "Singularity.ND96_H100_v5",
    "instance_count": node_count,
    "properties" : {
        "AISuperComputer" : {
        "interactive" : True,
        "slaTier": "Premium",
        "tensorboardLogDirectory": "/scratch/tensorboard_logs",
        }
    }
}

class vc_info:
    def __init__(self, subscription_id= "156138e5-a3b1-48af-9e2e-883f4df3f457", resource_group="gcr-singularity-lab", vc="baltic08"):
        self.subscription_id = subscription_id
        self.resource_group = resource_group
        self.vc = vc
        self.compute_config= "/subscriptions/"+ subscription_id +"/resourceGroups/"+ resource_group +"/providers/Microsoft.MachineLearningServices/virtualclusters/" + vc

if vc in ["dell1", "kings01", "kings02", "kings03", "kings04", "kings05", "kings06", "kings07", "kings08", "kings09", "kings10", "kings11", "kings12", "mckinley01", "mckinley02", "mckinley03", "mckinley04", "mckinley05", "mckinley06", "mckinley07", "mckinley08", "barlow01", "barlow02", "barlow03", "barlow04", "barlow05", "barlow06", "barlow07", "barlow08", "barlow09", "msrresrchlab"]:
    vc_info= vc_info(subscription_id= "156138e5-a3b1-48af-9e2e-883f4df3f457", resource_group="gcr-singularity-lab", vc=vc)
elif vc in ["baltic01", "baltic02", "baltic03", "baltic04", "baltic05", "baltic06", "baltic07", "baltic08", "baltic09", "baltic10", "baltic11", "baltic12", "huashanvc1", "huashanvc2", "huashanvc3", "huashanvc4"]:
    vc_info= vc_info(subscription_id= " 22da88f6-1210-4de2-a5a3-da4c7c2a1213", resource_group="gcr-singularity", vc=vc)   
elif vc in ["msrresrchvc"]:
    vc_info= vc_info(subscription_id= " 22da88f6-1210-4de2-a5a3-da4c7c2a1213", resource_group="gcr-singularity-resrch", vc=vc)
elif vc in ["msroctovc"]:
    vc_info= vc_info(subscription_id= " d4404794-ab5b-48de-b7c7-ec1fefb0a04e", resource_group="gcr-singularity-octo", vc=vc)

### setup workspace
ml_client = MLClient(
    DefaultAzureCredential(), subscription_id, resource_group, workspace_name
)
print(f"ml_client.workspace_name: {ml_client.workspace_name}")

environment = env = ml_client.environments.get(name='stable-ubuntu2004-cu121-py310-torch222', version='1.0')
distr_config = PyTorchConfiguration(
        node_count=node_count
    )

### setup launch command
launch_cmd = "sleep infinity"

job_name = "test-job12"
job = command(
    name=job_name,
    description="description",
    environment=environment,
    environment_variables={
        'JOB_EXECUTION_MODE': "basic",
        'AZUREML_COMPUTE_USE_COMMON_RUNTIME': 'true'
    },
    command=launch_cmd,
    compute=vc_info.compute_config,
    resources=vc_config,
    services={ # see https://learn.microsoft.com/en-us/azure/machine-learning/how-to-interactive-jobs?view=azureml-api-2&tabs=python
        "vscode": VsCodeJobService(nodes="all"),
    },
)

print(launch_cmd)
# submit the command
returned_job = ml_client.jobs.create_or_update(job)
# get a URL for the status of the job
returned_job.studio_url