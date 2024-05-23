"""Test for dvc_storage.py module."""


def test_download_dataset_functional():
    """Test functional download method."""
    from behaverse.dvc_storage import download_dataset
    path = download_dataset('P500_9subjects/L1m')

    assert path.exists()
    assert path.is_dir()
    assert path.stem == 'L1m'


def test_download_dataset_oop():
    """Test object-oriented download method."""
    from behaverse import Dataset
    dataset = Dataset.open('P500_9subjects/L1m', download=True, storage='dvc')
    assert dataset.validate()
