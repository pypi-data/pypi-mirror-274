"""Dataset class."""

import re
from pathlib import Path
import pandas as pd
from tqdm.auto import tqdm
from typing import Any
from .dataset_description import DatasetDescription
import logging
logger = logging.getLogger(__name__)


class Dataset():
    """Dataset provides methods to load and describe datasets.

    :::{.callout-note}

    Notes:
        You cannot manually instantiate this class. Use the class methods instead, e.g.
        `Dataset.load()`. You can also pass additional
        `allow_instantiation=True` to bypass this restriction.
    :::

    Args:
        name (str): the name to the dataset file. Use
                    [](`~behaverse.list_datasets`) to see available datasets.
        kwargs (dict): additional arguments.

    Raises:
        NotImplementedError: you cannot instantiate this class. Use the class methods instead.
    """

    def __init__(self, name: str, **kwargs) -> None:
        """Initialize the Dataset class."""
        if not kwargs.get('allow_instantiation', False):
            raise NotImplementedError('You cannot instantiate this class. Use the class methods instead.')

        self.name = name

        self.db_path = Path.home() / '.behaverse' / 'datasets' / self.name

        if not self.db_path.exists():
            raise FileNotFoundError(f'Dataset not found: {self.db_path}')

        # TODO add dataset-level attributes
        # TODO move time-consuming operations to methods and/or lazy load
        self.description = DatasetDescription()

        # SECTION subjects table
        self.subjects = pd.read_csv(self.db_path / 'subjects.csv',
                                    dtype={'subject_id': str})
        # !SECTION subjects table

        # SECTION study flow table
        study_flow_files = list(self.db_path.glob('**/study_flow.csv'))

        self.study_flow = pd.concat(
            [pd.read_csv(f, dtype={'subject_id': str, 'session_id': str})
             for f in study_flow_files], axis=0, ignore_index=True)
        # !SECTION study flow table

    def select(self, **selector_kwargs: Any) -> 'Dataset':
        """Filter the dataset given some selectors.

        Examples:
            To select subjects by their IDs:
            ```python
            dataset = dataset.select(subject_id=['001', '002'])
            ```

            To select subjects by a regex pattern:
            ```python
            dataset = dataset.select(regex=True, subject='^00[1-2]$')
            ```

            To select activities by their names:
            ```python
            dataset = dataset.select(activity=['NB', 'SOS'])
            ```

        Args:
            selector_kwargs: list of study flow values to select, or a regex pattern.
                             For example, `subject_id=['001', '002']` or `subject_id=r'00[1-2]'`.

        """
        if not hasattr(self, 'study_flow'):
            raise AttributeError('Dataset is not initiated yet. Use `open()` method.')

        for k, v in selector_kwargs.items():

            # TODO automatically detect regex patterns
            # try:
            #     assert isinstance(v, str), 'Regex should be a string.'
            #     re.compile(v)
            #     is_regex = True
            # except Exception:
            #     is_regex = False

            if k not in self.study_flow.columns:
                raise ValueError(f'Invalid selector: {k}')

            if isinstance(v, str):
                # FIXME this also considers regex patterns
                self.study_flow = self.study_flow[self.study_flow[k].str.contains(v)]
                if k == 'subject_id':
                    self.subjects = self.subjects[self.subjects[k].str.contains(v)]
            elif isinstance(v, list):
                self.study_flow = self.study_flow[self.study_flow[k].isin(v)]
                if k == 'subject_id':
                    self.subjects = self.subjects[self.subjects[k].isin(v)]
            else:
                raise ValueError(f'Invalid type for selector {k}: {type(v)}')

        return self

    def load(self) -> 'Dataset':
        """Load the dataset with the given name.

        Returns:
            Dataset: The newly loaded dataset.

        """
        # SECTION response table
        response_files = self.study_flow.apply(lambda s:
            (self.db_path /
            f'subject_{s["subject_id"]}' /
            f'session_{s["session_id"]}' /
            f'{s["activity"]}' /
            f'response_{s["attempt"]}.csv').absolute().as_posix(), axis=1).to_list()

        response_dfs = []
        for f in tqdm(response_files):
            if Path(f).exists():
                try:
                    df = pd.read_csv(f)
                    if not df.empty and len(df.columns) > 1:
                        response_dfs.append(df)
                except pd.errors.EmptyDataError:
                    logger.warning(f'Empty response file: {f}')

        self.response = pd.concat(response_dfs, axis=0, ignore_index=True)
        # !SECTION response table

        # TODO SECTION stimulus table
        self.stimulus = ...
        # !SECTION stimulus table

        # TODO SECTION option table
        self.option = ...
        # !SECTION option table

        return self

    @classmethod
    def open(cls, name: str, download: bool = True, storage='http') -> 'Dataset':
        """Open the dataset with the given name, and optionally download it if it does not exist.

        Args:
            name: Name of the dataset to open.
            download: whether to download the dataset if it does not exist.
            storage: storage backend to use (`http` or `dvc`). Defaults to 'http'.

        """
        path = Path.home() / '.behaverse' / 'datasets' / name

        match storage:
            case 'dvc':
                from .dvc_storage import download_dataset
            case _:
                from .http_storage import download_dataset

        if not path.exists():
            if not download:
                raise FileNotFoundError(f'Dataset not found: {path}. '
                                        'Use `download=True` to download it.')
            download_dataset(name)

        return cls(name, allow_instantiation=True)

    def describe(self) -> DatasetDescription:
        """Provides metadata and information card for the dataset."""
        return self.description

    def validate(self) -> bool:
        """Simple validations to check if the dataset is valid and consistent.

        :::{.callout-note}

        Notes:
            Violations will be logged as errors. Validation rules include:

                1. The dataset path should exist.
                2. TODO add more rules here.
        :::

        Returns:
            bool: True if the dataset is valid, False otherwise.

        """
        try:
            path = Path.home() / '.behaverse' / 'datasets' / self.name
            assert path.exists(), f'Path not found: {path.as_posix()}'
            assert path.is_dir(), f'Path is not a directory: {path.as_posix()}'
            # TODO add more rules here
            return True
        except AssertionError as e:
            logger.error(e)
            return False
