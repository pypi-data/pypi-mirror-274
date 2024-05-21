import logging


logger = logging.getLogger(__name__)


def pop_file(in_files):
    """
    Select the first file from a list of filenames.

    Used to grab the first echo's file when processing
    multi-echo data through workflows that only accept
    a single file.

    Examples
    --------
    >>> pop_file('some/file.nii.gz')
    'some/file.nii.gz'
    >>> pop_file(['some/file1.nii.gz', 'some/file2.nii.gz'])
    'some/file1.nii.gz'

    """
    if isinstance(in_files, (list, tuple)):
        return in_files[0]
    return in_files
