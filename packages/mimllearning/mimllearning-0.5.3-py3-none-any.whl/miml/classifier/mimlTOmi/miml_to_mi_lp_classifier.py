import numpy as np

from .miml_to_mi_classifier import MIMLtoMIClassifier
from ...transformation import LabelPowersetTransformation
from ...data import MIMLDataset


class MIMLtoMILPClassifier(MIMLtoMIClassifier):
    """
    Class to represent a multi-instance classifier using a label powerset transformation
    """

    def __init__(self, classifier) -> None:
        """
        Constructor of the class MIMLtoMILPClassifier

        Parameters
        ----------
        classifier
            Specific classifier to be used
        """
        super().__init__(classifier)
        self.transformation = LabelPowersetTransformation()

    def fit_internal(self, dataset_train: MIMLDataset) -> None:
        """
        Training the classifier

        Parameters
        ----------
        dataset_train: MIMLDataset
            Dataset to train the classifier
        """
        dataset = self.transformation.transform_dataset(dataset_train)
        self.classifier.fit(dataset.get_features_by_bag(), dataset.get_labels_by_bag())
        self.trained = True

    def predict(self, x: np.ndarray) -> np.ndarray:
        """
        Predict labels of given data

        Parameters
        ----------
        x : ndarray of shape (n_instances, n_features)
            Data to predict their labels

        Returns
        -------
        results : ndarray of shape (n_labels)
            Predicted labels
        """
        if not self.trained:
            raise Exception("The classifier is not trained. You need to call fit before predict anything")

        lp_label = self.classifier.predict(x)

        return self.transformation.lp_to_ml_label(lp_label)

    def predict_proba(self, dataset_test: MIMLDataset):
        """
        Predict probabilities of given dataset of having a positive label

        Parameters
        ----------
        dataset_test : MIMLDataset
            Dataset to predict probabilities

        Returns
        -------
        results: np.ndarray of shape (n_instances, n_features)
            Predicted probabilities for given dataset
        """
        if not self.trained:
            raise Exception("The classifier is not trained. You need to call fit before predict anything")

        bags_prob = self.classifier.predict_proba(dataset_test.get_features_by_bag())
        results = np.zeros((dataset_test.get_number_bags(), dataset_test.get_number_labels()))
        for bag_prob_index, bag_prob in enumerate(bags_prob):
            ml_probs = np.zeros(self.transformation.number_labels)
            for lp_label_index, lp_label_prob in enumerate(bag_prob):
                if lp_label_prob != 0:
                    ml_labels = self.transformation.lp_to_ml_label(self.classifier.classes_[lp_label_index])
                    ml_probs += ml_labels*lp_label_prob
            results[bag_prob_index] = ml_probs

        return results

