import numpy as np
from copy import deepcopy
from ...data import Bag
from ...data import MIMLDataset


class LabelPowersetTransformation:
    """
    Class that performs a label powerset transformation.
    """

    def __init__(self):
        self.dataset = None
        self.number_labels = 0

    def transform_dataset(self, dataset: MIMLDataset) -> MIMLDataset:
        """
        Transform the dataset to multi-instance dataset converting the labels to one label using binary to decimal
        codification

        Returns
        -------

        datasets: MIMLDataset
            Multi instance dataset

        """
        self.dataset = deepcopy(dataset)
        self.number_labels = self.dataset.get_number_labels()
        labels = self.dataset.get_labels_by_bag()
        labels_transformed = []

        for label in labels:
            labels_transformed.append(self.ml_to_lp_label(label))

        for i in range(self.number_labels-1, 0, -1):
            self.dataset.delete_attribute(self.dataset.get_number_features()+i)

        for i in range(self.dataset.get_number_bags()):
            bag = self.dataset.get_bag(i)
            for j in range(bag.get_number_instances()):
                self.dataset.set_attribute(i, j, self.dataset.get_number_attributes()-1, labels_transformed[i])

        self.dataset.set_labels_name(["lp label"])

        return self.dataset

    def transform_bag(self, bag: Bag) -> Bag:
        """
        Transform miml bag to multi instance bags

        Parameters
        ----------
        bag :
            Bag to be transformed to multi-instance bag

        Returns
        -------
        transformed_bag : Bag
            Transformed bag
        """
        if bag.dataset is None:
            raise Exception("Can't transform a bag without an assigned dataset, because we wouldn't have info about "
                            "the features and labels")

        transformed_bag = deepcopy(bag)

        lp_label = self.ml_to_lp_label(bag.get_labels())

        for i in range(bag.get_number_labels(), 0, -1):
            transformed_bag.dataset.attributes.pop(list(transformed_bag.dataset.attributes)[-1])
            transformed_bag.data = np.delete(transformed_bag.data, bag.get_number_features()+i, axis=1)

        for j in range(bag.get_number_instances()):
            transformed_bag.set_attribute(j, self.dataset.get_number_attributes() - 1, lp_label)

        transformed_bag.dataset.set_labels_name(["lp label"])

        return transformed_bag

    def lp_to_ml_label(self, label) -> np.ndarray:
        """
        Transform lp label to multilabel

        Parameters
        ----------
        label
            Lp label to be transformed

        Returns
        -------
        labels : np.ndarray
            Multilabel labels
        """
        binary_str = np.binary_repr(label.astype(int), width=self.number_labels)
        return np.array([int(bit) for bit in binary_str])

    def ml_to_lp_label(self, labels: np.ndarray) -> float:
        """
        Transform multilabel to lp label

        Parameters
        ----------
        labels : np.ndarray
            Multilabel labels to be transformed

        Returns
        -------
        label
            Lp label to be transformed
        """
        return np.dot(labels, np.flip(2 ** np.arange(self.number_labels)))
