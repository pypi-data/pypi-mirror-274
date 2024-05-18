import numpy as np

__version__ = "1.0"


def calculate_D_matrix(train_labels, test_labels):
    size = train_labels.size

    train_labels = train_labels.reshape(-1, 1)
    train_similarity_matrix = np.tile(train_labels, size) == train_labels.T
    np.fill_diagonal(train_similarity_matrix, False)

    test_labels = test_labels.reshape(-1, 1)
    test_similarity_matrix = np.tile(test_labels, size) == test_labels.T

    D_matrix = train_similarity_matrix == test_similarity_matrix
    return D_matrix


def prediction_strength(train_labels, test_labels):
    """Computes the prediction strength of a clustering.

    Args:
        train_labels: A list of test labels predicted on training clusters.
        test_labels: A list of test labels predicted on test clusters.

    Returns:
        A float representing the prediction strength of the clustering.
    """

    # TODO: check if train_labels and test_labels are the same size
    number_of_clusters = np.unique(train_labels).size

    D_matrix = calculate_D_matrix(train_labels, test_labels)

    prediction_strength = [0] * number_of_clusters
    for i in range(number_of_clusters):
        mask = (test_labels == i).reshape(-1)
        n = np.sum(mask)
        if n == 1:
            return 0
        prediction_sum = np.sum(D_matrix[mask, :][:, mask])
        prediction_strength[i] = prediction_sum / (n * (n - 1))

    return np.min(prediction_strength)


def prediction_strength_samples(train_labels, test_labels, samples=None):
    """Computes the prediction strength of a clustering for samples.

    Args:
        train_labels: A list of test labels predicted on training clusters.
        test_labels: A list of test labels predicted on test clusters.
        samples: A list of indicies to compute the prediction strength for.

    Returns:
        An array of floats representing the prediction strength of the clustering for each sample.
    """
    # raise NotImplementedError("Not implemented, use prediction_strength instead")

    number_of_clusters = np.unique(train_labels).size
    size = train_labels.size

    if samples is not None:
        assert isinstance(samples, list) or isinstance(samples, np.ndarray) or isinstance(samples, tuple)
        samples = np.array(samples)
    else:
        samples = np.arange(size)

    # TODO: check if samples are unique
    # TODO: check if samples are in range
    # TODO: check if samples are integers
    # TODO: crate matrix which rows are only samples and columns are all points

    D_matrix = calculate_D_matrix(train_labels, test_labels)

    prediction_strength = [0] * len(samples)
    for index, s in enumerate(samples):
        mask = (test_labels == test_labels[s]).reshape(-1)
        n = np.sum(mask)
        prediction_sum = np.sum(D_matrix[mask, :][:, s])
        prediction_strength[index] = prediction_sum/(n-1)

    return prediction_strength
