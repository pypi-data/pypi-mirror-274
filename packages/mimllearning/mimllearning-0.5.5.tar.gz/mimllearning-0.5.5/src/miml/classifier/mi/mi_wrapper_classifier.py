import numpy as np
from sklearn.tree import DecisionTreeClassifier


class MIWrapperClassifier:

    """
    MIWrapper Classifier.

    A simple Wrapper method for applying standard propositional learners to multi-instance data.

    Attributes
    ----------
    base_classifier
        Classifier to be used

    References
    ----------
    E. T. Frank, X. Xu (2003). Applying propositional learning algorithms to multi-instance data. Department of Computer
    Science, University of Waikato, Hamilton, NZ.
    """
    def __init__(self, base_classifier=DecisionTreeClassifier()):
        self.base_classifier = base_classifier
        self.classes_ = None

    def fit(self, x_train: np.ndarray, y_train: np.ndarray, weight: int = 2):
        """
        Fit the classifier to the training data.

        Parameters
        ----------
        x_train : ndarray of shape (n_bags, n_instances, n_features)
            Features values of bags in the training set.
        y_train : ndarray (n_bags, n_instances, n_labels)
            Labels of bags in the training set.
        weight : int, default = 2
            The type of weight setting for each single-instance:
                0: weight = 1.0
                1: weight = 1.0/Total number of single-instance in the corresponding bag
                2: weight = Total number of single-instance / (Total number of bags * Total number of single-instance in
                the corresponding bag).
        """
        # Flatten the bags into instances
        x_instances = np.vstack(x_train)
        y_instances = np.zeros((x_instances.shape[0]))
        count = 0
        for bag, label in zip(x_train, y_train):
            for _ in bag:
                y_instances[count] = label
                count += 1
        instance_weights = None
        if weight == 0:
            instance_weights = np.hstack([np.ones(len(bag)) for bag in x_train])
        if weight == 1:
            instance_weights = np.hstack([np.ones(len(bag)) / len(bag) for bag in x_train])
        elif weight == 2:
            instance_weights = np.hstack([np.full(len(bag), x_instances.shape[0]) / x_train.shape[0]*len(bag) for bag
                                          in x_train])

        self.base_classifier.fit(x_instances, y_instances, sample_weight=instance_weights)
        self.classes_ = self.base_classifier.classes_

    def predict(self, bag: np.ndarray):
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
        x_test = np.expand_dims(bag, axis=0)
        bag_probs = self.predict_proba(x_test)[0]
        label = self.classes_[np.argmax(bag_probs)]
        return label

    def predict_proba(self, x_test: np.ndarray):
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
        bag_probs = []
        for bag in x_test:
            instance_probs = self.base_classifier.predict_proba(bag)
            avg_probs = np.mean(instance_probs, axis=0)
            bag_probs.append(avg_probs)
        return np.array(bag_probs)
