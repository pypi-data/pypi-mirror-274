import numpy as np


class APRClassifier:

    """
    Classifier for All-Positive Bags using Axis-Aligned Positive Region.

    This classifier assigns a positive label to bags that contain instances within a predefined
    axis-parallel rectangle (APR) defined by the minimum and maximum feature values of positive
    instances in the training set.

    Attributes
    ----------
    apr : list
        List containing the minimum and maximum feature values defining the APR.

    References
    ----------
    Dietterich, Thomas G., Richard H. Lathrop, and Tomás Lozano-Pérez.
    "Solving the multiple instance problem with axis-parallel rectangles."
    Artificial intelligence 89.1 (1997): 31-71.
    """

    def __init__(self) -> None:
        """
        Constructor of the class AllPositiveAPRClassifier
        """
        self.apr = []

    def fit(self, x_train: np.ndarray, y_train: np.ndarray) -> None:
        """
        Fit the classifier to the training data.

        Parameters
        ----------
        x_train : ndarray of shape (n_bags, n_instances, n_features)
            Features values of bags in the training set.
        y_train : ndarray (n_bags, n_instances, n_labels)
            Labels of bags in the training set.
        """

        positive_bag_indices = np.where(y_train == 1)[0]

        # Select a random instance as starting apr
        initial_bag_index = np.random.choice(positive_bag_indices)
        initial_index_instance = np.random.choice(x_train[initial_bag_index].shape[0])
        apr_min = apr_max = x_train[initial_bag_index][initial_index_instance]

        # We check all positive instances and expand apr to minimum and maximum attribute values
        for bag_index in positive_bag_indices:
            for instance in x_train[bag_index]:
                apr_min = np.minimum(apr_min, instance)
                apr_max = np.maximum(apr_max, instance)

        self.apr = [apr_min, apr_max]

    def predict(self, bag: np.ndarray) -> int:
        """
        Predict the label of the bag

        Parameters
        ----------
        bag: np.ndarray of shape(n_instances, n_features)
            Features values of a bag

        Returns
        -------
        label: int
            Predicted label of the bag

        """
        # If all instances of the bag and all feature values in apr, it is a positive bag
        if np.all(bag >= self.apr[0]):
            if np.all(bag <= self.apr[1]):
                return 1
        return 0

    def predict_proba(self, x_test: np.ndarray) -> np.ndarray:
        """
        Predict probabilities of given data of having a positive label

        Parameters
        ----------
        x_test : np.ndarray of shape (n_bags, n_instances, n_features)
            Data to predict probabilities

        Returns
        -------
        results: np.ndarray of shape (n_instances, n_features)
            Predicted probabilities for given data
        """
        result = np.zeros(x_test.shape[0])
        for i in range(x_test.shape[0]):
            result[i] = self.predict(x_test[i])
        return result

