import os
import re
import sys
import typer
import toml
import cProfile
from pstats import Stats
from typing import Annotated
from rich import print as console
from rich.console import Group
from rich.panel import Panel
from rich.text import Text
from termcolor import colored
from cerebrium import api
from cerebrium.core import cli
from cerebrium.config import (
    CerebriumConfig,
    ScalingConfig,
    HardwareConfig,
    DeploymentConfig,
    DependencyConfig,
)
from cerebrium.utils.logging import cerebrium_log
from cerebrium.utils.requirements import strip_delimiters
from cerebrium.utils.deploy import package_app


_EXAMPLE_MAIN = """
def run(param_1: str, param_2: str, run_id):  # run_id is optional, injected by Cerebrium at runtime
    my_results = {"1": param_1, "2": param_2}
    my_status_code = 200 # if you want to return a specific status code

    return {"my_result": my_results, "status_code": my_status_code} # return your results
"""


@cli.command("init")
def init(
    name: Annotated[str, typer.Option(help="Name of the Cortex deployment.")],
    init_dir: Annotated[
        str,
        typer.Argument(
            help="Directory where you would like to init a Cortex project.",
        ),
    ] = ".",
    overwrite: Annotated[
        bool,
        typer.Option(help="Flag to overwrite contents of the init_dir."),
    ] = False,
    pip: Annotated[
        str,
        typer.Option(
            help=(
                "Optional list of requirements. "
                "Example: \"['transformers', 'torch==1.31.1']\""
            ),
        ),
    ] = "['transformers', 'torch']",
    apt: Annotated[
        str,
        typer.Option(
            help=("Optional list of apt packages. For example: \"['git', 'ffmpeg' ]\""),
        ),
    ] = "[]",
    conda: Annotated[str, typer.Option(help="Optional list of conda packages.")] = "[]",
    cpu: Annotated[
        int,
        typer.Option(
            help=(
                "Number of vCPUs (cores) to use for the Cortex deployment. " "Defaults to 3."
            ),
        ),
    ] = 3,
    memory: Annotated[
        float,
        typer.Option(
            help=(
                "Amount of memory (in GB) to use for the Cortex deployment. "
                "Defaults to 14GB. "
            ),
        ),
    ] = 14,
    gpu: Annotated[
        str,
        typer.Option(
            help=("Type of GPU to use for the Cortex deployment. " "Defaults to 'AMPERE_A10'."),
        ),
    ] = "AMPERE_A10",
    gpu_count: Annotated[
        int,
        typer.Option(
            help=("Number of GPUs to use for the Cortex deployment. " "Defaults to 1."),
        ),
    ] = 1,
    include: Annotated[
        str,
        typer.Option(
            help=(
                "Comma delimited string list of relative paths to files/folder to include. "
                "Defaults to all visible files/folders in project root."
            ),
        ),
    ] = "[./*, main.py, cerebrium.toml]",
    exclude: Annotated[
        str,
        typer.Option(
            help=(
                "Comma delimited string list of relative paths to files/folder to exclude. "
                "Defaults to all hidden files/folders in project root."
            ),
        ),
    ] = "[.*]",
    cuda_version: Annotated[
        str,
        typer.Option(
            help=("CUDA version to use. " "Defaults to '12'"),
        ),
    ] = "12",
    min_replicas: Annotated[
        int,
        typer.Option(
            help=("Minimum number of replicas to keep running. " "Defaults to 0."),
        ),
    ] = 0,
    max_replicas: Annotated[
        int,
        typer.Option(
            help=("Maximum number of replicas to keep running. " "Defaults to 5."),
        ),
    ] = 5,
    cooldown: Annotated[
        int,
        typer.Option(
            help=("Cooldown period in seconds. " "Defaults to 60 seconds (5 minutes)."),
        ),
    ] = 60,
):
    """
    Initialize an empty Cerebrium Cortex project.
    """
    print(f"Initializing Cerebrium Cortex project in {init_dir}")
    if not name:
        name = os.path.basename(os.path.abspath(init_dir))
        name = name.replace("_", "-")
        # remove all non alpha-numerical digits that aren't '-'
        name = re.sub(r"[^a-zA-Z0-9-]", "", name)
        name = name.lower()

    if not os.path.exists(init_dir):
        os.makedirs(init_dir)
    elif os.listdir(init_dir) and not overwrite:
        cerebrium_log(
            level="WARNING",
            message="Directory is not empty. "
            "Use an empty directory or use the `--overwrite` flag.",
            prefix_seperator="\t",
        )
        raise typer.Exit()

    if not os.path.exists(os.path.join(init_dir, "main.py")):
        with open(os.path.join(init_dir, "main.py"), "w") as f:
            f.write(_EXAMPLE_MAIN)

    interpreter_version = sys.version_info
    python_version = f"{interpreter_version.major}.{interpreter_version.minor}"
    pip_dict = strip_delimiters(pip)
    apt_dict = strip_delimiters(apt)
    conda_dict = strip_delimiters(conda)

    scaling_config = ScalingConfig(
        min_replicas=min_replicas, max_replicas=max_replicas, cooldown=cooldown
    )
    hardware_config = HardwareConfig(
        cpu=cpu,
        memory=memory,
        gpu=gpu,
        gpu_count=gpu_count,
        provider="aws",
        region="us-east-1",
    )
    dependency_config = DependencyConfig(pip=pip_dict, apt=apt_dict, conda=conda_dict)
    deployment_config = DeploymentConfig(
        name=name,
        python_version=python_version,
        cuda_version=cuda_version,
        include=include,
        exclude=exclude,
        shell_commands=[],
    )
    config = CerebriumConfig(
        scaling=scaling_config,
        hardware=hardware_config,
        deployment=deployment_config,
        dependencies=dependency_config,
    )
    config.to_toml(f"{init_dir}/cerebrium.toml")
    print("🚀 Cerebrium Cortex project initialized successfully!")


@cli.command("deploy")
def deploy(
    disable_syntax_check: Annotated[
        bool, typer.Option(help="Flag to disable syntax check.")
    ] = False,
    force_rebuild: Annotated[
        bool,
        typer.Option(
            help="Force rebuild an app. Clears a deployment's environment and builds as if it is a clean deployment.",
        ),
    ] = False,
    init_debug: Annotated[
        bool,
        typer.Option(
            help="Pauses the container after initialization. You need to manually cancel the build to terminate.",
        ),
    ] = False,
    log_level: Annotated[
        str,
        typer.Option(
            help="Log level for the Cortex deployment. Can be one of 'DEBUG' or 'INFO'",
        ),
    ] = "INFO",
    config_file: Annotated[
        str,
        typer.Option(
            help="Path to the cerebrium config TOML file. You can generate a config using `cerebrium init`."
        ),
    ] = "./cerebrium.toml",
    disable_confirmation: Annotated[
        bool,
        typer.Option(
            "--disable-confirmation",
            "-y",
            help="Disable the confirmation prompt before deploying.",
        ),
    ] = False,
    disable_animation: Annotated[
        bool,
        typer.Option(
            "--disable-animation",
            help="Disable TQDM loading bars and yaspin animations.",
        ),
    ] = False,
    disable_build_logs: Annotated[
        bool,
        typer.Option("--disable-build-logs", help="Disable build logs during a deployment."),
    ] = False,
):
    """
    Deploy a Cortex deployment to Cerebrium
    """

    with cProfile.Profile() as pr:
        # load config toml file
        log_level = log_level.upper()
        assert log_level in [
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "INTERNAL",
        ], "Log level must be one of 'DEBUG' or 'INFO'"
        toml_config = toml.load(config_file)["cerebrium"]
        scaling_config: ScalingConfig = ScalingConfig(**toml_config["scaling"])
        hardware_config: HardwareConfig = HardwareConfig(**toml_config["hardware"])
        deployment_config: DeploymentConfig = DeploymentConfig(**toml_config["deployment"])
        dependency_config: DependencyConfig = DependencyConfig(**toml_config["dependencies"])
        config: CerebriumConfig = CerebriumConfig(
            scaling=scaling_config,
            hardware=hardware_config,
            deployment=deployment_config,
            dependencies=dependency_config,
        )

        # Check if the provider is Coreweave, if so print a V3 deprecation warning
        if config.hardware.provider == "coreweave":
            cerebrium_log(
                message="WARNING: Cortex V4 does not currently support Coreweave. Please considering updating your deployment to V4 and deploying to AWS.",
                level="WARNING",
            )
        build_status, setup_response = package_app(
            config,
            "deploy",
            force_rebuild,
            init_debug,
            disable_build_logs,
            log_level,  # type: ignore
            disable_syntax_check,
            disable_animation,
            disable_confirmation,
        )
        if setup_response is None:
            cerebrium_log(
                message="Error setting up your deployment and getting your logs. Please check your dashboard or contact support if the issue persists.",
                color="red",
            )
            sys.exit(1)
        if "success" == build_status:
            project_id = setup_response["projectId"]
            jwt = setup_response["jwt"]
            endpoint = setup_response["internalEndpoint"]

            dashboard_url = f"{api.dashboard_url}/projects/{project_id}/models/{project_id}-{config.deployment.name}"

            info_string = (
                f"🔗 [link={dashboard_url}]View your deployment dashboard here[/link]\n"
                f"🔗 [link={dashboard_url}?tab=builds]View builds here[/link]\n"
                f"🔗 [link={dashboard_url}?tab=runs]View runs here[/link]\n\n"
                f"🛜  Endpoint:\n{endpoint}"
            )

            dashboard_info = Panel(
                info_string,
                title=f"[bold green]🚀 {config.deployment.name} is now live! 🚀 ",
                border_style="green",
                width=100,
                padding=(1, 2),
            )

            console(Group(dashboard_info))

            curl_command = colored(
                f"curl -X POST {endpoint}/{{function}} \\\n"
                "     -H 'Content-Type: application/json'\\\n"
                f"     -H 'Authorization: Bearer {jwt}'\\\n"
                '     --data \'{"param": "Hello World!"}\'',
                "green",
            )
            print(
                "\n💡You can call the endpoint with the following curl command:\n"
                f"{curl_command}"
            )
        elif build_status in ["build_failure", "init_failure"]:
            console(
                Text(
                    "Unfortunately there was an issue with your deployment",
                    style="red",
                )
            )
    pr.disable()
    if log_level == "INTERNAL":
        stats = Stats(pr)
        stats.sort_stats("tottime").print_stats(10)
