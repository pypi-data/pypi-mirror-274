"""TODO: Access Behaverse datasets via Behaverse Registry."""


import logging
from .utils import extract_dataset
from pathlib import Path
logger = logging.getLogger(__name__)


def download_dataset(name: str, **kwargs) -> Path:
    """Download a dataset from the dvc-managed Behaverse registry.

    Args:
        name: the name of the dataset to download.
        kwargs (dict): additional arguments. For example you can specify the destination
                        path (`dest`) to save the dataset file. Defaults to
                        `~/.behaverse/datasets/{name}/`. Or `chunk_size` to specify the chunk size for downloading.

    Returns:
        Path: Path to the downloaded dataset file.

    Raises:
        ImportError: if DVC is not installed.
        FileNotFoundError: if the dataset is not found.
        AssertionError: if the dataset name is not provided.
    """
    from dvc.api import DVCFileSystem

    assert name is not None, 'Dataset name is required.'

    # FIXME: query DVC registry for the url of the dataset

    repo = 'git@github.com:behaverse/behaverse.git'
    fs = DVCFileSystem(repo, rev='Registry', remote='ulhpc')

    dest = Path(kwargs.get('dest',
                           Path.home() / '.behaverse' / 'datasets' / f'{name.replace("/", "-")}.tar.gz'))

    if dest.exists():
        return extract_dataset(name)

    dest.parent.mkdir(parents=True, exist_ok=True)

    # download the dataset using DVC
    fs.get(f'datasets/{name}.tar.gz', dest.as_posix())

    logger.info(f'Downloaded DVC dataset to {dest}, now extracting...')

    return extract_dataset(name)
