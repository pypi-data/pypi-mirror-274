from dataclasses import dataclass, fields, replace
from pathlib import Path
import click

dpi = 96


@dataclass
class TurnoverConfig:
    MIN_RT: int = 2
    ABUNDANCE_CUTOFF: float = 0.01
    # split jobs into this many spectra
    # set to zero to not split
    NSPECTRA: int = 10000
    # quadrature limit for estimating area under curve (unused now)
    QUAD_LIMIT: int = 500
    # https://docs.python.org/3/library/logging.html#logrecord-attributes
    LOG_FORMAT: str = "%(levelname)s|[%(asctime)s]|%(process)d| %(message)s"

    # XCMS_STEP = 0.0
    PEPXML_CHUNKS: int = 1000

    # also group on retention_time_sec
    GROUP_RT: bool = False

    FIGSIZE: tuple[float, float] = (1056.0 / dpi, 768.0 / dpi)

    MAIL_SUBJECT: str = "turnover pipeline"
    # default "from" sender
    MAIL_TURNOVER: str = "turnover-pipeline@uwa.edu.au"
    # set to None or 'none' to stop any emailing
    MAIL_SERVER: str = "antivirus.uwa.edu.au"

    # e.g. "https://protein-turnover.plantenergy.org/inspect/{jobid}"
    INSPECT_URL: str | None = None
    # email template with {job:TurnoverJob, url:str}
    MAIL_TEXT: str = (
        """Protein Turnover Job "{job.job_name}" has <b>finished</b>!{url}."""
    )
    # set to True for production version (hides debug click commands)

    INTERPOLATE_INTENSITY: bool = True

    # Dinosaur
    JAVA_PATH: str | None = None  # "java"
    DINOSAUR_JAR: str | None = None


FIELDS = [f.name for f in fields(TurnoverConfig)]

config = TurnoverConfig()


def _update_config(config: TurnoverConfig, filename: str | Path) -> TurnoverConfig:

    import tomli as tomllib

    updates = {}
    try:
        with open(filename, "rb") as fp:
            d = tomllib.load(fp)
    except Exception as e:
        raise click.BadParameter(
            f"can't read configuration file: {e}",
            param_hint="config",
        )

    for k, v in d.items():
        if k == "website":
            continue
        k = k.upper()

        if k in FIELDS:
            v2 = getattr(config, k)
            if v != v2:
                updates[k] = v

        else:
            click.secho(f"unknown configuration attribute {k}", fg="red")

    if updates:
        return replace(config, **updates)
    return config


def get_config() -> TurnoverConfig:
    return config

def update_config(filename: str | Path) -> TurnoverConfig:
    global config
    config = _update_config(config, filename)
    return config
