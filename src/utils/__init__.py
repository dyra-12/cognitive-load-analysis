"""
utils package

Provides shared utilities for:
 - File I/O (io_utils)
 - Plotting helpers (plot_utils)
 - ML metrics (metrics)

Import examples:
    from utils.io_utils import read_json
    from utils.plot_utils import save_fig
    from utils.metrics import compute_fold_metrics
"""

from .io_utils import (
    ensure_dir,
    list_json_files,
    load_all_json,
    load_modeling_csv,
    read_json,
    save_df,
    write_json,
)
from .metrics import aggregate_metrics, collect_misclassifications, compute_fold_metrics
from .plot_utils import plot_bar, plot_confusion_matrix, plot_scatter, save_fig

__all__ = [
    # io_utils
    "ensure_dir",
    "read_json",
    "write_json",
    "save_df",
    "load_modeling_csv",
    "list_json_files",
    "load_all_json",
    # plot_utils
    "save_fig",
    "plot_bar",
    "plot_scatter",
    "plot_confusion_matrix",
    # metrics
    "compute_fold_metrics",
    "aggregate_metrics",
    "collect_misclassifications",
]
