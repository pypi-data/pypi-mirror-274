from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional

import yaml


class ClientException(Exception):
    def __init__(self, msg):
        self.msg = msg


class Cloud(Enum):
    AWS = "aws"
    LAMBDA_LABS = "lambda"


@dataclass(kw_only=True)
class MachineConfig:
    setup_script: str = ""
    env: Dict[str, str] = field(default_factory=lambda: {})
    resources: Dict[str, Any] = field(default_factory=lambda: {})
    storage: Dict[str, Any] = field(default_factory=lambda: {})
    workdir: Optional[str] = None
    cloud: Optional[Cloud] = None
    docker_image: Optional[str] = None
    notebook: bool = False

    @staticmethod
    def _from_dict(config: dict) -> "MachineConfig":
        final_config = {}
        if "setup" in config:
            setup_script = config["setup"]
            assert isinstance(setup_script, str)
            final_config["setup_script"] = setup_script
            del config["setup"]
        if "env" in config:
            env = config["env"]
            assert isinstance(env, dict)
            for k, v in env.items():
                assert isinstance(k, str) and isinstance(v, str)
            final_config["env"] = env
            del config["env"]
        if "resources" in config:
            resources = config["resources"]
            assert isinstance(resources, dict)
            for k, v in resources.items():
                assert k in {"cpus", "gpus", "memory", "ports"}
                # TODO: more validation of values
            if "ports" in resources:
                ports = resources["ports"]
                assert isinstance(ports, int) or isinstance(ports, list)
                if isinstance(ports, list):
                    assert [isinstance(p, int) for p in ports]
            final_config["resources"] = resources
            del config["resources"]
        if "storage" in config:
            storage = config["storage"]
            assert isinstance(storage, dict)
            # TODO: more validation
            final_config["storage"] = storage
            del config["storage"]
        if "workdir" in config:
            workdir = config["workdir"]
            assert isinstance(workdir, str)
            final_config["workdir"] = workdir
            del config["workdir"]
        if "cloud" in config:
            cloud = config["cloud"]
            cloud = Cloud(cloud)
            final_config["cloud"] = cloud
            del config["cloud"]
        if "docker_image" in config:
            docker_image = config["docker_image"]
            assert isinstance(docker_image, str)
            final_config["docker_image"] = docker_image
            del config["docker_image"]
        if "notebook" in config:
            notebook = config["notebook"]
            assert isinstance(notebook, bool)
            final_config["notebook"] = notebook
            del config["notebook"]

        if config:
            keys = list(config.keys())
            raise Exception(f'Unexpected entries found in config: {",".join(keys)}')

        return MachineConfig(**final_config)

    @staticmethod
    def from_yaml(config_file: str) -> "MachineConfig":
        with open(config_file, "r") as f:
            config = yaml.load(f, yaml.FullLoader)

        return MachineConfig._from_dict(config)


@dataclass(kw_only=True)
class JobConfig(MachineConfig):
    run_script: str
    num_nodes: int = 1

    @staticmethod
    def _from_dict(config: Dict) -> "JobConfig":
        final_config = {}
        assert "run" in config
        run_script = config["run"]
        assert isinstance(run_script, str)
        final_config["run_script"] = run_script
        del config["run"]

        if "num_nodes" in config:
            num_nodes = config["num_nodes"]
            assert isinstance(num_nodes, int)
            assert num_nodes >= 1
            final_config["num_nodes"] = num_nodes
            del config["num_nodes"]

        machine_config = MachineConfig._from_dict(config).__dict__
        final_config.update(machine_config)

        job_config = JobConfig(**final_config)
        return job_config

    @staticmethod
    def from_yaml(config_file: str) -> "JobConfig":
        with open(config_file, "r") as f:
            config = yaml.load(f, yaml.FullLoader)

        job_config = JobConfig._from_dict(config)
        return job_config


@dataclass(kw_only=True)
class ServiceInfo:
    min_replicas: int
    target_qps_per_replica: float
    readiness_probe_path: str
    max_replicas: Optional[int] = None
    upscale_delay_seconds: int = 300
    downscale_delay_seconds: int = 1200
    readiness_probe_post_data: Optional[str] = None
    readiness_probe_initial_delay_seconds: int = 600

    @staticmethod
    def _from_dict(config: dict) -> "ServiceInfo":
        final_config = {}

        assert "min_replicas" in config
        min_replicas = config["min_replicas"]
        assert isinstance(min_replicas, int)
        assert min_replicas >= 0
        final_config["min_replicas"] = min_replicas
        del config["min_replicas"]

        assert "target_qps_per_replica" in config
        target_qps_per_replica = config["target_qps_per_replica"]
        assert isinstance(target_qps_per_replica, float) or isinstance(
            target_qps_per_replica, int
        )
        assert target_qps_per_replica > 0
        final_config["target_qps_per_replica"] = target_qps_per_replica
        del config["target_qps_per_replica"]

        assert "readiness_probe" in config
        readiness_probe = config["readiness_probe"]
        if isinstance(readiness_probe, str):
            readiness_probe_path = readiness_probe
            assert isinstance(readiness_probe_path, str)
            final_config["readiness_probe_path"] = readiness_probe_path
        elif isinstance(readiness_probe, dict):
            assert "path" in readiness_probe
            readiness_probe_path = readiness_probe["path"]
            final_config["readiness_probe_path"] = readiness_probe_path
            assert isinstance(readiness_probe_path, str)
            if "post_data" in readiness_probe:
                readiness_probe_post_data = readiness_probe["post_data"]
                assert isinstance(readiness_probe_post_data, dict)
                final_config["readiness_probe_post_data"] = readiness_probe_post_data
            if "initial_delay_seconds" in readiness_probe:
                readiness_probe_initial_delay_seconds = readiness_probe[
                    "initial_delay_seconds"
                ]
                assert (
                    isinstance(readiness_probe_initial_delay_seconds, int)
                    and readiness_probe_initial_delay_seconds > 0
                )
                final_config["readiness_probe_initial_delay_seconds"] = (
                    readiness_probe_initial_delay_seconds
                )
        del config["readiness_probe"]

        if "max_replicas" in config:
            max_replicas = config["max_replicas"]
            assert isinstance(max_replicas, int)
            assert max_replicas >= min_replicas
            final_config["max_replicas"] = max_replicas
            del config["max_replicas"]

        if "upscale_delay_seconds" in config:
            upscale_delay_seconds = config["upscale_delay_seconds"]
            assert isinstance(upscale_delay_seconds, int)
            assert upscale_delay_seconds > 0
            final_config["upscale_delay_seconds"] = upscale_delay_seconds
            del config["upscale_delay_seconds"]

        if "downscale_delay_seconds" in config:
            downscale_delay_seconds = config["downscale_delay_seconds"]
            assert isinstance(downscale_delay_seconds, int)
            assert downscale_delay_seconds > 0
            final_config["downscale_delay_seconds"] = downscale_delay_seconds
            del config["downscale_delay_seconds"]

        if config:
            keys = list(config.keys())
            raise Exception(
                f'Unexpected entries found in service config: {",".join(keys)}'
            )

        service_info = ServiceInfo(**final_config)
        return service_info


@dataclass(kw_only=True)
class ServiceConfig(JobConfig):
    service: ServiceInfo

    @staticmethod
    def _from_dict(config: dict) -> "ServiceConfig":
        final_config = {}

        assert "service" in config
        service_section = config["service"]
        service_info = ServiceInfo._from_dict(service_section)
        final_config["service"] = service_info
        del config["service"]

        job_config = JobConfig._from_dict(config).__dict__
        final_config.update(job_config)
        service_config = ServiceConfig(**final_config)

        # Service must have a port
        assert service_config.resources.get("ports", None)

        return service_config

    @staticmethod
    def from_yaml(config_file: str) -> "ServiceConfig":
        with open(config_file, "r") as f:
            config = yaml.load(f, yaml.FullLoader)

        service_config = ServiceConfig._from_dict(config)
        return service_config


class JobStatus(Enum):
    PENDING = "pending"
    INITIALIZING = "initializing"
    RUNNING = "running"
    SHUTTING_DOWN = "shutting_down"
    FINISHED = "finished"
    CANCELLING = "cancelling"
    CANCELLED = "cancelled"
    ERROR = "error"
    UNKNOWN = "unknown"
    NOT_FOUND = "not found"
    UNAUTHORIZED = "unauthorized"
    UNREACHABLE = "unreachable"


class MachineStatus(Enum):
    PENDING = "pending"
    INITIALIZING = "initializing"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    TERMINATING = "terminating"
    TERINATED = "terminated"
    ERROR = "error"
    UNKNOWN = "unknown"
    NOT_FOUND = "not found"
    UNAUTHORIZED = "unauthorized"
    UNREACHABLE = "unreachable"


class ServiceStatus(Enum):
    CONTROLLER_INIT = "CONTROLLER_INIT"
    REPLICA_INIT = "REPLICA_INIT"
    CONTROLLER_FAILED = "CONTROLLER_FAILED"
    READY = "READY"
    SHUTTING_DOWN = "SHUTTING_DOWN"
    FAILED = "FAILED"
    FAILED_CLEANUP = "FAILED_CLEANUP"
    NO_REPLICA = "NO_REPLICA"
    DELETED = "DELETED"
    UNAUTHORIZED = "unauthorized"
    NOT_FOUND = "not found"
    UNKNOWN = "unknown"


class ReplicaStatus(Enum):
    PENDING = "PENDING"
    PROVISIONING = "PROVISIONING"
    STARTING = "STARTING"
    READY = "READY"
    NOT_READY = "NOT_READY"
    SHUTTING_DOWN = "SHUTTING_DOWN"
    FAILED = "FAILED"
    FAILED_INITIAL_DELAY = "FAILED_INITIAL_DELAY"
    FAILED_PROBING = "FAILED_PROBING"
    FAILED_PROVISION = "FAILED_PROVISION"
    FAILED_CLEANUP = "FAILED_CLEANUP"
    PREEMPTED = "PREEMPTED"
    UNKNOWN = "UNKNOWN"


@dataclass
class Job:
    id: str
    name: str
    status: JobStatus
    status_message: str
    setup_script: str
    run_script: str
    num_nodes: int
    env: dict
    resources: dict
    storage: dict
    cloud: Optional[Cloud]
    docker_image: Optional[str]
    created_timestamp: int
    updated_timestamp: int

    @classmethod
    def from_dict(cls, d):
        d["status"] = JobStatus(d["status"])
        if d.get("cloud", None):
            d["cloud"] = Cloud(d["cloud"])

        job = Job(**d)
        return job


@dataclass
class Machine:
    id: str
    name: str
    status: MachineStatus
    status_message: str
    setup_script: str
    env: dict
    resources: dict
    storage: dict
    cloud: Optional[Cloud]
    docker_image: Optional[str]
    notebook_token: Optional[str]
    notebook_url: Optional[str]

    @classmethod
    def from_dict(cls, d):
        d["status"] = MachineStatus(d["status"])
        if d.get("cloud", None):
            d["cloud"] = Cloud(d["cloud"])

        machine = Machine(**d)
        return machine


@dataclass
class Service:
    id: str
    name: str
    status: ServiceStatus
    status_message: str
    setup_script: str
    run_script: str
    env: dict
    resources: dict
    storage: dict
    cloud: Cloud
    docker_image: Optional[str]

    readiness_path: str
    initial_delay_seconds: Optional[int]
    post_data: Optional[Dict[str, Any]]

    min_replicas: int
    max_replicas: Optional[int]
    target_qps_per_replica: Optional[float]
    upscale_delay_seconds: Optional[int]
    downscale_delay_seconds: Optional[int]

    uptime: int
    current_version: Optional[int]
    active_versions: Optional[str]

    created_timestamp: int
    updated_timestamp: int

    @classmethod
    def from_dict(cls, d):
        d["status"] = ServiceStatus(d["status"])
        d["cloud"] = Cloud(d["cloud"])

        service = Service(**d)
        return service


@dataclass
class ServiceReplica:
    service_id: str
    replica_id: int
    replica_info: Optional[Dict[str, Any]]
    status: Optional[ReplicaStatus]
    created_timestamp: int
    updated_timestamp: int

    @classmethod
    def from_dict(cls, d):
        if d.get("status", None):
            d["status"] = ReplicaStatus(d["status"])
        else:
            d["status"] = None

        replica = ServiceReplica(**d)
        return replica
