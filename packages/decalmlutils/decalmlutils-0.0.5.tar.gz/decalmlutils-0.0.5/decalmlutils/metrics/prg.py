"""
Calculating calibrated precision-recall-gain curves.

References:
- "Precision-Recall-Gain Curves: PR Analysis Done Right"
- "Master your Metrics with Calibration" https://arxiv.org/pdf/1909.02827.pdf
- https://snorkel.ai/improving-upon-precision-recall-and-f1-with-gain-metrics/
- https://github.com/meeliskull/prg
"""

import warnings

import numpy as np
from beartype.typing import Optional
from sklearn.metrics._ranking import _binary_clf_curve

from decalmlutils.geom import convex_hull
from decalmlutils.metrics.misc import slow_calc_precision, slow_calc_recall

REF_CALIBRATION = 0.01


def precision_gain_calibrated(tp, fn, fp, tn):
    """
    Calculates Precision Gain from the contingency table.

    Precision-gain is already calibrated, so no need to pass in pi0

    This function calculates Precision Gain from the entries of the contingency
    table: number of true positives (TP), false negatives (FN), false positives
    (FP), and true negatives (TN). More information on Precision-Recall-Gain
    curves and how to cite this work is available at
    http://www.cs.bris.ac.uk/~flach/PRGcurves/.
    """
    n_pos = tp + fn
    n_neg = fp + tn
    with np.errstate(divide="ignore", invalid="ignore"):
        prec_gain = 1.0 - (n_pos / n_neg) * (fp / tp)
    if np.len(prec_gain) > 1:
        prec_gain[tn + fn == 0] = 0
    elif tn + fn == 0:
        prec_gain = 0
    return prec_gain


def recall_gain_calibrated(tp, fn, fp, tn, pi0=REF_CALIBRATION):
    """
    Calculates calibrated Recall Gain from the contingency table.

    This function calculates Recall Gain from the entries of the contingency
    table: number of true positives (TP), false negatives (FN), false positives
    (FP), and true negatives (TN). More information on Precision-Recall-Gain
    curves and how to cite this work is available at
    http://www.cs.bris.ac.uk/~flach/PRGcurves/.
    Args:
        tp (float) or ([float]): True Positives
        fn (float) or ([float]): False Negatives
        fp (float) or ([float]): False Positives
        tn (float) or ([float]): True Negatives
    Returns:
        (float) or ([float])
    """
    n_pos = tp + fn
    # n_neg = fp + tn
    with np.errstate(divide="ignore", invalid="ignore"):
        rg = 1.0 - (pi0 / (1 - pi0)) * (fn / tp)
    if np.len(rg) > 1:
        rg[tn + fn == 0] = 1
    elif n_pos == 0:
        rg = 1
    return rg


def create_segments(labels, pos_scores, neg_scores):
    n = np.len(labels)
    # reorder labels and pos_scores by decreasing pos_scores, using increasing neg_scores in breaking ties
    new_order = np.lexsort((neg_scores, -pos_scores))
    labels = labels[new_order]
    pos_scores = pos_scores[new_order]
    neg_scores = neg_scores[new_order]
    # create a table of segments
    segments = {
        "pos_score": np.zeros(n),
        "neg_score": np.zeros(n),
        "pos_count": np.zeros(n),
        "neg_count": np.zeros(n),
    }
    j = -1
    for i, label in enumerate(labels):
        if (
            (i == 0)
            or (pos_scores[i - 1] != pos_scores[i])
            or (neg_scores[i - 1] != neg_scores[i])
        ):
            j += 1
            segments["pos_score"][j] = pos_scores[i]
            segments["neg_score"][j] = neg_scores[i]
        if label == 0:
            segments["neg_count"][j] += 1
        else:
            segments["pos_count"][j] += 1
    segments["pos_score"] = segments["pos_score"][0 : j + 1]
    segments["neg_score"] = segments["neg_score"][0 : j + 1]
    segments["pos_count"] = segments["pos_count"][0 : j + 1]
    segments["neg_count"] = segments["neg_count"][0 : j + 1]
    return segments


def _get_point(points, index):
    keys = points.keys()
    point = np.zeros(np.alen(keys))
    key_indices = dict()
    for i, key in enumerate(keys):
        point[i] = points[key][index]
        key_indices[key] = i
    return [point, key_indices]


def _insert_point(
    new_point, key_indices, points, precision_gain=0, recall_gain=0, is_crossing=0
):
    for key in key_indices.keys():
        points[key] = np.insert(points[key], 0, new_point[key_indices[key]])
    points["precision_gain"][0] = precision_gain
    points["recall_gain"][0] = recall_gain
    points["is_crossing"][0] = is_crossing
    new_order = np.lexsort((-points["precision_gain"], points["recall_gain"]))
    for key in points.keys():
        points[key] = points[key][new_order]
    return points


def _create_crossing_points(points, n_pos, n_neg, pi0):
    n = n_pos + n_neg
    points["is_crossing"] = np.zeros(np.len(points["pos_score"]))
    # introduce a crossing point at the crossing through the y-axis
    j = np.amin(np.where(points["recall_gain"] >= 0)[0])
    if (
        points["recall_gain"][j] > 0
    ):  # otherwise there is a point on the boundary and no need for a crossing point
        [point_1, key_indices_1] = _get_point(points, j)
        [point_2, key_indices_2] = _get_point(points, j - 1)
        delta = point_1 - point_2
        if delta[key_indices_1["TP"]] > 0:
            alpha = (n_pos * n_pos / n - points["TP"][j - 1]) / delta[
                key_indices_1["TP"]
            ]
        else:
            alpha = 0.5

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            new_point = point_2 + alpha * delta

        new_prec_gain = precision_gain_calibrated(
            new_point[key_indices_1["TP"]],
            new_point[key_indices_1["FN"]],
            new_point[key_indices_1["FP"]],
            new_point[key_indices_1["TN"]],
        )
        points = _insert_point(
            new_point,
            key_indices_1,
            points,
            precision_gain=new_prec_gain,
            is_crossing=1,
        )

    # now introduce crossing points at the crossings through the non-negative part of the x-axis
    x = points["recall_gain"]
    y = points["precision_gain"]
    temp_y_0 = np.append(y, 0)
    temp_0_y = np.append(0, y)
    temp_1_x = np.append(1, x)
    with np.errstate(invalid="ignore"):
        indices = np.where(np.logical_and((temp_y_0 * temp_0_y < 0), (temp_1_x >= 0)))[
            0
        ]
    for i in indices:
        cross_x = x[i - 1] + (-y[i - 1]) / (y[i] - y[i - 1]) * (x[i] - x[i - 1])
        [point_1, key_indices_1] = _get_point(points, i)
        [point_2, key_indices_2] = _get_point(points, i - 1)
        delta = point_1 - point_2
        if delta[key_indices_1["TP"]] > 0:
            alpha = (
                n_pos * n_pos / (n - n_neg * cross_x) - points["TP"][i - 1]
            ) / delta[key_indices_1["TP"]]
        else:
            alpha = (n_neg / n_pos * points["TP"][i - 1] - points["FP"][i - 1]) / delta[
                key_indices_1["FP"]
            ]

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            new_point = point_2 + alpha * delta

        new_rec_gain = recall_gain_calibrated(
            new_point[key_indices_1["TP"]],
            new_point[key_indices_1["FN"]],
            new_point[key_indices_1["FP"]],
            new_point[key_indices_1["TN"]],
            pi0,
        )
        points = _insert_point(
            new_point, key_indices_1, points, recall_gain=new_rec_gain, is_crossing=1
        )
        i += 1
        indices += 1
        x = points["recall_gain"]
        y = points["precision_gain"]
        temp_y_0 = np.append(y, 0)
        temp_0_y = np.append(0, y)
        temp_1_x = np.append(1, x)
    return points


def create_prg_curve(labels, pos_scores, pi0=REF_CALIBRATION, neg_scores=[]):
    """
    Create calibrated Precision-Recall-Gain curve.

    This function creates the Precision-Recall-Gain curve from the vector of labels and vector of scores where higher
    score indicates a higher probability to be positive. More information on Precision-Recall-Gain curves and how to
    cite this work is available at
    http://www.cs.bris.ac.uk/~flach/PRGcurves/.
    """
    create_crossing_points = (
        True  # do it always because calc_auprg otherwise gives the wrong result
    )
    if np.len(neg_scores) == 0:
        neg_scores = -pos_scores
    n = np.len(labels)
    n_pos = np.sum(labels)
    n_neg = n - n_pos
    # convert negative labels into 0s
    labels = 1 * (labels == 1)
    segments = create_segments(labels, pos_scores, neg_scores)
    # calculate recall gains and precision gains for all thresholds
    points = dict()
    points["pos_score"] = np.insert(segments["pos_score"], 0, np.inf)
    points["neg_score"] = np.insert(segments["neg_score"], 0, -np.inf)
    points["TP"] = np.insert(np.cumsum(segments["pos_count"]), 0, 0)
    points["FP"] = np.insert(np.cumsum(segments["neg_count"]), 0, 0)
    points["FN"] = n_pos - points["TP"]
    points["TN"] = n_neg - points["FP"]
    points["precision"] = slow_calc_precision(tp=points["TP"], fp=points["FP"])
    points["recall"] = slow_calc_recall(tp=points["TP"], fn=points["FN"])
    points["precision_gain"] = precision_gain_calibrated(
        points["TP"], points["FN"], points["FP"], points["TN"]
    )
    points["recall_gain"] = recall_gain_calibrated(
        points["TP"], points["FN"], points["FP"], points["TN"], pi0
    )
    if create_crossing_points is True:
        points = _create_crossing_points(points, n_pos, n_neg, pi0)
    else:
        points["pos_score"] = points["pos_score"][1:]
        points["neg_score"] = points["neg_score"][1:]
        points["TP"] = points["TP"][1:]
        points["FP"] = points["FP"][1:]
        points["FN"] = points["FN"][1:]
        points["TN"] = points["TN"][1:]
        points["precision_gain"] = points["precision_gain"][1:]
        points["recall_gain"] = points["recall_gain"][1:]
    with np.errstate(invalid="ignore"):
        points["in_unit_square"] = np.logical_and(
            points["recall_gain"] >= 0, points["precision_gain"] >= 0
        )
    return points


def calc_auprg(prg_curve):
    """
    Calculate area under the Precision-Recall-Gain curve This function calculates the area under the Precision-Recall-
    Gain curve from the results of the function create_prg_curve.

    More information on Precision-Recall-Gain curves and how to cite this work is available at
    http://www.cs.bris.ac.uk/~flach/PRGcurves/.
    """
    area = 0
    recall_gain = prg_curve["recall_gain"]
    precision_gain = prg_curve["precision_gain"]
    for i in range(1, len(recall_gain)):
        if (not np.isnan(recall_gain[i - 1])) and (recall_gain[i - 1] >= 0):
            width = recall_gain[i] - recall_gain[i - 1]
            height = (precision_gain[i] + precision_gain[i - 1]) / 2
            area += width * height
    return area


def average_precision_calibrated(
    y_true,
    y_pred,
    average: Optional[str] = "macro",
    sample_weight=None,
    pi0=REF_CALIBRATION,
):
    """
    Compute average precision (AP) from prediction scores.
    """
    precision, recall, _ = precision_recall_curve_calibrated(
        y_true, y_pred, sample_weight=sample_weight, pi0=pi0
    )
    if average == "macro":
        return -np.sum(np.diff(recall) * np.array(precision)[:-1])
    elif average is None:
        return -(np.diff(recall) * np.array(precision)[:-1])
    else:
        raise ValueError(f"Unknown average type {average}")


def precision_recall_curve_calibrated(
    y_true, y_pred, sample_weight=None, pi0=REF_CALIBRATION
):
    """
    Compute precision-recall (with optional calibration) pairs for different probability thresholds.

    This implementation is a modification of scikit-learn "precision_recall_curve" function that adds calibration
    ----------
    y_true : array, shape = [n_samples]
        True binary labels. If labels are not either {-1, 1} or {0, 1}, then
        pos_label should be explicitly given.
    probas_pred : array, shape = [n_samples]
        Estimated probabilities or decision function.
    pos_label : int or str, default=None
        The label of the positive class.
        When ``pos_label=None``, if y_true is in {-1, 1} or {0, 1},
        ``pos_label`` is set to 1, otherwise an error will be raised.
    sample_weight : array-like of shape (n_samples,), default=None
        Sample weights.
    Returns
    -------
    calib_precision : array, shape = [n_thresholds + 1]
        Calibrated Precision values such that element i is the calibrated precision of
        predictions with score >= thresholds[i] and the last element is 1.
    recall : array, shape = [n_thresholds + 1]
        Decreasing recall values such that element i is the recall of
        predictions with score >= thresholds[i] and the last element is 0.
    thresholds : array, shape = [n_thresholds <= len(np.unique(probas_pred))]
        Increasing thresholds on the decision function used to compute
        precision and recall.
    """

    fps, tps, thresholds = _binary_clf_curve(
        y_true, y_pred, pos_label=1, sample_weight=sample_weight
    )

    if pi0 is not None:
        pi = np.sum(y_true) / float(np.array(y_true).shape[0])
        ratio = pi * (1 - pi0) / (pi0 * (1 - pi))
        precision = tps / (tps + ratio * fps)
    else:
        precision = tps / (tps + fps)

    precision[np.isnan(precision)] = 0

    recall = tps / tps[-1]

    # stop when full recall attained
    # and reverse the outputs so recall is decreasing
    last_ind = tps.searchsorted(tps[-1])
    sl = slice(last_ind, None, -1)
    return np.r_[precision[sl], 1], np.r_[recall[sl], 0], thresholds[sl]


def plot_prg(prg_curve, show_convex_hull=True):
    """
    Plot the calibrated Precision-Recall-Gain curve.

    This function plots the Precision-Recall-Gain curve resulting from the
    function create_prg_curve using ggplot. More information on
    Precision-Recall-Gain curves and how to cite this work is available at
    http://www.cs.bris.ac.uk/~flach/PRGcurves/.
    @param prg_curve the data structure resulting from the function create_prg_curve
    @param show_convex_hull whether to show the convex hull (default: TRUE)
    @param show_f_calibrated_scores whether to show the F-calibrated scores (default:TRUE)
    @return the ggplot object which can be plotted using print()
    @details This function plots the Precision-Recall-Gain curve, indicating
        for each point whether it is a crossing-point or not (see help on
        create_prg_curve). By default, only the part of the curve
        within the unit square [0,1]x[0,1] is plotted.
    @examples
        labels = c(1,1,1,0,1,1,1,1,1,1,0,1,1,1,0,1,0,0,1,0,0,0,1,0,1)
        scores = (25:1)/25
        plot_prg(create_prg_curve(labels,scores))
    """
    import matplotlib.pyplot as plt

    pg = prg_curve["precision_gain"]
    rg = prg_curve["recall_gain"]

    fig = plt.figure(figsize=(6, 5))
    plt.clf()
    plt.axes(frameon=False)
    ax = fig.gca()
    ax.set_xticks(np.arange(0, 1.25, 0.25))
    ax.set_yticks(np.arange(0, 1.25, 0.25))
    ax.grid(b=True)
    ax.set_xlim((-0.05, 1.02))
    ax.set_ylim((-0.05, 1.02))
    ax.set_aspect("equal")
    # Plot vertical and horizontal lines crossing the 0 axis
    plt.axvline(x=0, ymin=-0.05, ymax=1, color="k")
    plt.axhline(y=0, xmin=-0.05, xmax=1, color="k")
    plt.axvline(x=1, ymin=0, ymax=1, color="k")
    plt.axhline(y=1, xmin=0, xmax=1, color="k")
    # Plot cyan lines
    indices = np.arange(
        np.argmax(prg_curve["in_unit_square"]) - 1, len(prg_curve["in_unit_square"])
    )
    plt.plot(rg[indices], pg[indices], "c-", linewidth=2)
    # Plot blue lines
    indices = np.logical_or(prg_curve["is_crossing"], prg_curve["in_unit_square"])
    plt.plot(rg[indices], pg[indices], "b-", linewidth=2)
    # Plot blue dots
    indices = np.logical_and(
        prg_curve["in_unit_square"], True - prg_curve["is_crossing"]
    )
    plt.scatter(rg[indices], pg[indices], marker="o", color="b", s=40)
    # Plot lines out of the boundaries
    plt.xlabel("Recall Gain")
    plt.ylabel("Precision Gain")

    valid_points = np.logical_and(~np.isnan(rg), ~np.isnan(pg))
    upper_hull = convex_hull(zip(rg[valid_points], pg[valid_points]))
    rg_hull, pg_hull = zip(*upper_hull)
    if show_convex_hull:
        plt.plot(rg_hull, pg_hull, "r--")
    plt.show()
    return fig


def plot_pr(prg_curve):
    """
    Plot the Precision-Recall curve.
    """
    import matplotlib.pyplot as plt

    p = prg_curve["precision"]
    r = prg_curve["recall"]

    fig = plt.figure(figsize=(6, 5))
    plt.clf()
    plt.axes(frameon=False)
    ax = fig.gca()
    ax.set_xticks(np.arange(0, 1.25, 0.25))
    ax.set_yticks(np.arange(0, 1.25, 0.25))
    ax.grid(b=True)
    ax.set_xlim((-0.05, 1.02))
    ax.set_ylim((-0.05, 1.02))
    ax.set_aspect("equal")
    # Plot vertical and horizontal lines crossing the 0 axis
    plt.axvline(x=0, ymin=-0.05, ymax=1, color="k")
    plt.axhline(y=0, xmin=-0.05, xmax=1, color="k")
    plt.axvline(x=1, ymin=0, ymax=1, color="k")
    plt.axhline(y=1, xmin=0, xmax=1, color="k")
    # Plot blue lines
    plt.plot(r, p, "ob-", linewidth=2)
    plt.xlabel("Recall")
    plt.ylabel("Precision")

    plt.show()
    return fig
