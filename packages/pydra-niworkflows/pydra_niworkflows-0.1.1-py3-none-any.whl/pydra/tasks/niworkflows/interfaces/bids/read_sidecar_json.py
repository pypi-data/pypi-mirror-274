import attrs
from fileformats.generic import Directory, File
import logging
from pydra.tasks.niworkflows.utils.bids import _init_layout
import pydra.mark
import typing as ty


logger = logging.getLogger(__name__)





@pydra.mark.task
@pydra.mark.annotate(
    {
        "return": {
            "out_dict": dict,
            "subject": str,
            "session": str,
            "task": str,
            "acquisition": str,
            "reconstruction": str,
            "run": int,
            "suffix": str,
        }
    }
)
def ReadSidecarJSON(
    in_file: File, bids_dir: ty.Any, bids_validate: bool, index_db: Directory, fields: ty.List[str]
) -> ty.Tuple[dict, str, str, str, str, str, int, str]:
    """
    Examples
    -------

    >>> from fileformats.generic import Directory, File
    >>> from pydra.tasks.niworkflows.interfaces.bids.read_sidecar_json import ReadSidecarJSON

    """
    layout = bids_dir 
    layout = _init_layout(
        in_file,
        layout,
        bids_validate,
        database_path=(index_db if (index_db is not attrs.NOTHING) else None),
    )

    # Fill in BIDS entities of the output ("*_id")
    output_keys = ['subject', 'session', 'task', 'acquisition', 'reconstruction', 'run', 'suffix']
    params = layout.parse_file_entities(in_file)
    _results = {
        key: params.get(key.split("_")[0], type(attrs.NOTHING)) for key in output_keys
    }

    # Fill in metadata
    metadata = layout.get_metadata(in_file)
    out_dict = metadata

    # Set dynamic outputs if fields input is present
    for fname in fields:
        if fname not in metadata:
            raise KeyError(
                'Metadata field "%s" not found for file %s' % (fname, in_file)
            )
        _results[fname] = metadata.get(fname, type(attrs.NOTHING))

    return out_dict, _results['subject'], _results['session'], _results['task'], _results['acquisition'], _results['reconstruction'], _results['run'], _results['suffix']


# Nipype methods converted into functions
