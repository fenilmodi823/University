import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

iris = datasets.load_iris()
data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
data['target'] = iris.target

X = data.iloc[:, :-1]
y = data['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy of the Random Forest classifier: {accuracy * 100:.2f}%\n")

correct_preds = []
incorrect_preds = []

for i in range(len(y_test)):
    if y_test.iloc[i] == y_pred[i]:
        correct_preds.append((X_test.iloc[i].values, y_test.iloc[i]))
    else:
        incorrect_preds.append((X_test.iloc[i].values, y_test.iloc[i], y_pred[i]))

print("Correct Predictions:")
for features, label in correct_preds:
    print(f"Features: {features}, Predicted: {label}, Actual: {label}")

print("\nIncorrect Predictions:")
for features, actual, predicted in incorrect_preds:
    print(f"Features: {features}, Predicted: {predicted}, Actual: {actual}")

print("\nClassification Report:\n", classification_report(y_test, y_pred))

plt.figure(figsize=(6, 4))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, cmap="Blues", fmt="d", xticklabels=iris.target_names, yticklabels=iris.target_names)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()
