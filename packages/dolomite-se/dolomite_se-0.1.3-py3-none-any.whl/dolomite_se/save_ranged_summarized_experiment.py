import os

import dolomite_base as dl
from summarizedexperiment import RangedSummarizedExperiment, SummarizedExperiment


@dl.save_object.register
@dl.validate_saves
def save_ranged_summarized_experiment(
    x: RangedSummarizedExperiment,
    path: str,
    data_frame_args: dict = None,
    assay_args: dict = None,
    **kwargs,
):
    """Method for saving
    :py:class:`~summarizedexperiment.SummarizedExperiment.SummarizedExperiment`
    objects to their corresponding file representations, see
    :py:meth:`~dolomite_base.save_object.save_object` for details.

    Args:
        x:
            Object to be staged.

        path:
            Path to a directory in which to save ``x``.

        data_frame_args:
            Further arguments to pass to the ``save_object`` method for the
            row/column data.

        assay_args:
            Further arguments to pass to the ``save_object`` method for the
            assays.

        kwargs:
            Further arguments.

    Returns:
        ``x`` is saved to path.
    """

    if data_frame_args is None:
        data_frame_args = {}

    if assay_args is None:
        assay_args = {}

    # convert to SE
    _se = SummarizedExperiment(
        assays=x.get_assays(),
        row_data=x.get_row_data(),
        column_data=x.get_column_data(),
        row_names=x.get_row_names(),
        column_names=x.get_column_names(),
        metadata=x.get_metadata(),
    )
    dl.alt_save_object(
        _se, path, data_frame_args=data_frame_args, assay_args=assay_args, **kwargs
    )

    # save row_ranges
    _ranges = x.get_row_ranges()
    if _ranges is not None:
        dl.alt_save_object(_ranges, path=os.path.join(path, "row_ranges"), **kwargs)

    # Modify OBJECT
    _info = dl.read_object_file(path)
    _info["ranged_summarized_experiment"] = {"version": "1.0"}
    dl.save_object_file(path, "ranged_summarized_experiment", _info)

    return
