import logging
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


logger = logging.getLogger(__name__)


def compcor_variance_plot(
    metadata_files,
    metadata_sources=None,
    output_file=None,
    varexp_thresh=(0.5, 0.7, 0.9),
    fig=None,
):
    """
    Parameters
    ----------
    metadata_files: list
        List of paths to files containing component metadata. If more than one
        decomposition has been performed (e.g., anatomical and temporal
        CompCor decompositions), then all metadata files can be provided in
        the list. However, each metadata file should have a corresponding
        entry in `metadata_sources`.
    metadata_sources: list or None
        List of source names (e.g., ['aCompCor']) for decompositions. This
        list should be of the same length as `metadata_files`.
    output_file: str or None
        Path where the output figure should be saved. If this is not defined,
        then the plotting axes will be returned instead of the saved figure
        path.
    varexp_thresh: tuple
        Set of variance thresholds to include in the plot (default 0.5, 0.7,
        0.9).
    fig: figure or None
        Existing figure on which to plot.

    Returns
    -------
    ax: axes
        Plotting axes. Returned only if the `output_file` parameter is None.
    output_file: str
        The file where the figure is saved.
    """
    metadata = {}
    if metadata_sources is None:
        if len(metadata_files) == 1:
            metadata_sources = ["CompCor"]
        else:
            metadata_sources = [
                f"Decomposition {i:d}" for i in range(len(metadata_files))
            ]
    for file, source in zip(metadata_files, metadata_sources):
        metadata[source] = pd.read_csv(str(file), sep=r"\s+")
        metadata[source]["source"] = source
    metadata = pd.concat(list(metadata.values()))
    bbox_txt = {
        "boxstyle": "round",
        "fc": "white",
        "ec": "none",
        "color": "none",
        "linewidth": 0,
        "alpha": 0.8,
    }
    decompositions = []
    data_sources = list(metadata.groupby(["source", "mask"]).groups.keys())
    for source, mask in data_sources:
        if not np.isnan(
            metadata.loc[(metadata["source"] == source) & (metadata["mask"] == mask)][
                "singular_value"
            ].values[0]
        ):
            decompositions.append((source, mask))
    if fig is not None:
        ax = [
            fig.add_subplot(1, len(decompositions), i + 1)
            for i in range(len(decompositions))
        ]
    elif len(decompositions) > 1:
        fig, ax = plt.subplots(
            1, len(decompositions), figsize=(5 * len(decompositions), 5)
        )
    else:
        ax = [plt.axes()]
    for m, (source, mask) in enumerate(decompositions):
        components = metadata[
            (metadata["mask"] == mask) & (metadata["source"] == source)
        ]
        if len([m for s, m in decompositions if s == source]) > 1:
            title_mask = f" ({mask} mask)"
        else:
            title_mask = ""
        fig_title = f"{source}{title_mask}"
        ax[m].plot(
            np.arange(components.shape[0] + 1),
            [0] + list(100 * components["cumulative_variance_explained"]),
            color="purple",
            linewidth=2.5,
        )
        ax[m].grid(False)
        ax[m].set_xlabel("number of components in model")
        ax[m].set_ylabel("cumulative variance explained (%)")
        ax[m].set_title(fig_title)
        varexp = {}
        for i, thr in enumerate(varexp_thresh):
            varexp[thr] = (
                np.atleast_1d(
                    np.searchsorted(components["cumulative_variance_explained"], thr)
                )
                + 1
            )
            ax[m].axhline(y=100 * thr, color="lightgrey", linewidth=0.25)
            ax[m].axvline(x=varexp[thr], color=f"C{i}", linewidth=2, linestyle=":")
            ax[m].text(
                0,
                100 * thr,
                "{:.0f}".format(100 * thr),
                fontsize="x-small",
                bbox=bbox_txt,
            )
            ax[m].text(
                varexp[thr][0],
                25,
                "{} components explain\n{:.0f}% of variance".format(
                    varexp[thr][0], 100 * thr
                ),
                rotation=90,
                horizontalalignment="center",
                fontsize="xx-small",
                bbox=bbox_txt,
            )
        ax[m].set_yticks([])
        ax[m].set_yticklabels([])
        for label in ax[m].xaxis.get_majorticklabels():
            label.set_fontsize("x-small")
            label.set_rotation("vertical")
        for side in ["top", "right", "left"]:
            ax[m].spines[side].set_color("none")
            ax[m].spines[side].set_visible(False)
    if output_file is not None:
        figure = plt.gcf()
        figure.savefig(output_file, bbox_inches="tight")
        plt.close(figure)
        figure = None
        return output_file
    return ax
