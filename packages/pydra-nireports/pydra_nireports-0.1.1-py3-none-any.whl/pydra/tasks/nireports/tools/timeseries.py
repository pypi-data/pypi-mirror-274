import logging
import nibabel as nb
import numpy as np


logger = logging.getLogger(__name__)


def cifti_timeseries(dataset):
    """Extract timeseries from CIFTI2 dataset."""
    dataset = nb.load(dataset) if isinstance(dataset, str) else dataset
    if dataset.nifti_header.get_intent()[0] != "ConnDenseSeries":
        raise ValueError("Not a dense timeseries")
    matrix = dataset.header.matrix
    labels = {
        "CIFTI_STRUCTURE_CORTEX_LEFT": "CtxL",
        "CIFTI_STRUCTURE_CORTEX_RIGHT": "CtxR",
        "CIFTI_STRUCTURE_CEREBELLUM_LEFT": "CbL",
        "CIFTI_STRUCTURE_CEREBELLUM_RIGHT": "CbR",
    }
    seg = {label: [] for label in list(labels.values()) + ["Other"]}
    for bm in matrix.get_index_map(1).brain_models:
        label = (
            "Other" if bm.brain_structure not in labels else labels[bm.brain_structure]
        )
        seg[label] += list(range(bm.index_offset, bm.index_offset + bm.index_count))
    return dataset.get_fdata(dtype="float32").T, seg


def get_tr(img):
    """
    Attempt to extract repetition time from NIfTI/CIFTI header.

    Examples
    --------
    >>> get_tr(nb.load(
    ...     testdata_path
    ...     / 'sub-ds205s03_task-functionallocalizer_run-01_bold_volreg.nii.gz'
    ... ))
    2.2
    >>> get_tr(nb.load(
    ...     testdata_path
    ...     / 'sub-01_task-mixedgamblestask_run-02_space-fsLR_den-91k_bold.dtseries.nii'
    ... ))
    2.0

    """
    try:
        return img.header.matrix.get_index_map(0).series_step
    except AttributeError:
        return img.header.get_zooms()[-1]
    raise RuntimeError("Could not extract TR - unknown data structure type")


def nifti_timeseries(
    dataset,
    segmentation=None,
    labels=("Ctx GM", "dGM", "WM+CSF", "Cb", "Crown"),
    remap_rois=False,
    lut=None,
):
    """Extract timeseries from NIfTI1/2 datasets."""
    dataset = nb.load(dataset) if isinstance(dataset, str) else dataset
    data = dataset.get_fdata(dtype="float32").reshape((-1, dataset.shape[-1]))
    if segmentation is None:
        return data, None
    # Open NIfTI and extract numpy array
    segmentation = (
        nb.load(segmentation) if isinstance(segmentation, str) else segmentation
    )
    segmentation = np.asanyarray(segmentation.dataobj, dtype=int).reshape(-1)
    remap_rois = remap_rois or (
        len(np.unique(segmentation[segmentation > 0])) > len(labels)
    )
    # Map segmentation
    if remap_rois or lut is not None:
        if lut is None:
            lut = np.zeros((256,), dtype="uint8")
            lut[100:201] = 1  # Ctx GM
            lut[30:99] = 2  # dGM
            lut[1:11] = 3  # WM+CSF
            lut[255] = 4  # Cerebellum
        # Apply lookup table
        segmentation = lut[segmentation]
    fgmask = segmentation > 0
    segmentation = segmentation[fgmask]
    seg_dict = {}
    for i in np.unique(segmentation):
        seg_dict[labels[i - 1]] = np.argwhere(segmentation == i).squeeze()
    return data[fgmask], seg_dict
