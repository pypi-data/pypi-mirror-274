# PredictionStrength: Prediction Strength for Cluster Validation

## Overview

prediction-strength is a Python package designed to implement the concept of Prediction Strength, a score for cluster validation introduced by Robert Tibshirani and Guenther Walther in their seminal paper, "Cluster Validation by Prediction Strength". This package aims to provide a user-friendly and efficient way to apply this powerful score to your clustering solutions, improving your ability to discern the optimal number of clusters and evaluate the stability of your clustering results.

## Features

- Efficient computation of Prediction Strength score for various clustering algorithms.
- Flexibility to work with any distance or similarity metric.
- Compatibility with popular data manipulation and analysis libraries like NumPy, Pandas, and Scikit-learn.
- Supports parallel computation for handling large datasets.

## Installation

prediction-strength can be installed via pip:

```sh
pip install git+git://github.com/HKozubek/PredictionStrength.git#egg=predstr
```

## Quick Start

Here is a simple example of how to use prediction-strength with a k-means clustering algorithm.

```python
from sklearn.cluster import KMeans
from prediction_strength import prediction_strength

# Assume X is your data
kmeans_train = KMeans(n_clusters=3, random_state=0).fit(X_train)
kmeans_test = KMeans(n_clusters=3, random_state=0).fit(X_test)

score = prediction_strength(kmeans_train.predict(X_test), kmeans_test.labels_)

print("Prediction Strength Score: ", score)
```

## Documentation

For a more comprehensive guide on how to use PredStr, please refer to our [full documentation](http://link-to-your-documentation).

## Contributing

We appreciate all contributions. If you're interested in contributing, please read our [contributing guide](CONTRIBUTING.md).

## Citation

If you use PredStr in a scientific publication, we would appreciate citations to the following paper:

Tibshirani, R., Walther, G. (2005). Cluster Validation by Prediction Strength. Journal of Computational and Graphical Statistics, 14(3), 511-528.

## License

PredStr is distributed under the terms of the [MIT License](LICENSE.txt).

## Contact

For help and feedback, please feel free to contact the maintainer.

## Acknowledgments

The creation of this package would not have been possible without the groundbreaking work of Robert Tibshirani and Guenther Walther.
