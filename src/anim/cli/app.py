import sys
from datetime import datetime
from pathlib import Path
from typing import Annotated

import typer
import yaml
from pydantic import BaseModel

from anim.cli import anim

# from calib.cli import calibrate

app = typer.Typer(no_args_is_help=True)


class Waves_conventions(BaseModel):
    file: Path
    key_hs: str
    key_dir: str
    key_per: str
    key_t: str
    angle_min_landward: int
    angle_max_landward: int
    convert_direction_0_360_to_m180_180: bool
    threshold_aberrant_hs: float
    threshold_aberrant_period: float
    wave_height_notable_percentile_min_threshold: float
    storms_resume_file: Path


class AppConfig(BaseModel):
    app_name: str
    waves: Waves_conventions
    water_level: Path
    transects: list
    transects_to_plot: list
    input_directory_a: Path
    profile_mvt_files: list[Path]
    output_dir: Path
    start: datetime
    end: datetime
    variables_to_plot: dict[str, bool]
    height_ratios: dict[str, float]


def load_config(path: str) -> AppConfig:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return AppConfig(**data)  # validation automatique


@app.command()
def main(
    input_yaml: Annotated[
        Path,
        typer.Argument(
            exists=True,
            dir_okay=True,
            help="Input yaml file containing parameters",
        ),
    ],
):
    # load configuration file
    conf = load_config(input_yaml)

    if not conf.waves.file.exists():
        raise typer.Exit("waves file does not exist")

    if not conf.input_directory_a.exists():
        raise typer.Exit("Average images dir does not exist")

    if not conf.output_dir.exists():
        conf.output_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Run animation creation
        anim.main(conf)

    except Exception as e:  # noqa: BLE001
        typer.secho(f"An error occurred: {e}", fg=typer.colors.RED)
        sys.exit(1)


if __name__ == "__main__":
    app()
