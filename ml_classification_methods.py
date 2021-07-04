from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.datasets import fetch_openml
from sklearn.base import clone
from sklearn.linear_model import SGDClassifier
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

class MlClassificationMethods:

    kmclassifier = None

    def __init__(self, train_x=[], train_y = []):
        self.train_x = train_x
        self.train_y = train_y
        #print(train_x[0])
        #print(train_x)
        #for i in range(len(train_x)):
            #train_x[i] = list(train_x)

        self.train_x = np.array(train_x, dtype=float)
        self.train_y = np.array(train_y, dtype=int)
        #print(self.train_y.shape)


    def k_means_train(self):
        # Create a knn Classifier
        knn1 = KNeighborsClassifier(n_neighbors=1, weights='distance')
        knn3 = KNeighborsClassifier(n_neighbors=3, weights='distance')
        knn5 = KNeighborsClassifier(n_neighbors=5, weights='distance')
        knn7 = KNeighborsClassifier(n_neighbors=7, weights='distance')
        svclassifier_lin = SVC(kernel='linear')
        svclassifier_rbf = SVC(kernel='rbf')
        #clf = DecisionTreeClassifier()

        """# Train the model using the training sets
        knn1.fit(self.train_x, self.train_y)
        knn3.fit(self.train_x, self.train_y)
        knn5.fit(self.train_x, self.train_y)
        knn7.fit(self.train_x, self.train_y)

        # Predict the response for test dataset
        y_pred1 = knn1.predict(self.train_x)
        y_pred3 = knn3.predict(self.train_x)
        y_pred5 = knn5.predict(self.train_x)
        y_pred7 = knn7.predict(self.train_x)"""
        i = 0
        skfolds = StratifiedKFold(n_splits=2, shuffle=True, random_state=42)
        for train_index, test_index in skfolds.split(self.train_x, self.train_y):
            #i +=1
            #if i>1 :
            #    continue
            clone_clf = clone(knn7)
            X_train_folds = self.train_x[train_index]
            y_train_folds = self.train_y[train_index]
            X_test_fold = self.train_x[test_index]
            y_test_fold = self.train_y[test_index]
            self.kmclassifier = clone_clf.fit(X_train_folds, y_train_folds)
            y_pred = clone_clf.predict(X_test_fold)
            n_correct = sum(y_pred == y_test_fold)
            #print(n_correct / len(y_pred))

        #self.kmclassifier = knn5

        """print("test size: ", len(self.train_y))
        print("train size: ", len(self.train_y))

        err_count1 = 0
        err_count3 = 0
        err_count5 = 0
        err_count7 = 0

        for i in range(len(self.train_y)):
            if self.train_y[i] != y_pred1[i]:
                err_count1 += 1
            if self.train_y[i] != y_pred3[i]:
                err_count3 += 1
            if self.train_y[i] != y_pred5[i]:
                err_count5 += 1
            if self.train_y[i] != y_pred7[i]:
                err_count7 += 1

        print("~~~Errors Comparison: ~~~")
        print("Number of neighbor= ", 1, " ,number of errors: ", err_count1, ", accuracy: ",
              metrics.accuracy_score(self.train_y, y_pred1))
        print("Number of neighbor= ", 3, " ,number of errors: ", err_count3, ", accuracy: ",
              metrics.accuracy_score(self.train_y, y_pred3))
        print("Number of neighbor= ", 5, " ,number of errors: ", err_count5, ", accuracy: ",
              metrics.accuracy_score(self.train_y, y_pred5))
        print("Number of neighbor= ", 7, " ,number of errors: ", err_count7, ", accuracy: ",
              metrics.accuracy_score(self.train_y, y_pred7))"""