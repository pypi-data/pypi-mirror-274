import numpy as np
from sklearn.tree import DecisionTreeClassifier


class MIWrapperClassifier:
    def __init__(self, base_classifier=DecisionTreeClassifier()):
        self.base_classifier = base_classifier
        self.classes_ = None

    def fit(self, x_train, y_train):
        # Flatten the bags into instances
        x_instances = np.vstack(x_train)
        y_instances = np.zeros((x_instances.shape[0]))
        count = 0
        for bag, label in zip(x_train, y_train):
            for instance in bag:
                y_instances[count] = label
                count += 1
        instance_weights = np.hstack([np.ones(len(bag)) / len(bag) for bag in x_train])

        self.base_classifier.fit(x_instances, y_instances, sample_weight=instance_weights)
        self.classes_ = self.base_classifier.classes_

    def predict_proba(self, x_test):
        bag_probs = []
        for bag in x_test:
            instance_probs = self.base_classifier.predict_proba(bag)
            avg_probs = np.mean(instance_probs, axis=0)
            bag_probs.append(avg_probs)
        return np.array(bag_probs)

    def predict(self, x_test):
        x_test = np.expand_dims(x_test, axis=0)
        bag_probs = self.predict_proba(x_test)[0]
        label = self.classes_[np.argmax(bag_probs)]
        return label
