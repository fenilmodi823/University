import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import sys

def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        data.columns = data.columns.str.strip()
        print("Columns in the dataset:", list(data.columns))
        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print("Error: File is empty.")
        sys.exit(1)
    except pd.errors.ParserError:
        print("Error: File could not be parsed. Check for formatting issues.")
        sys.exit(1)

def preprocess_data(data):
    if 'target' not in data.columns:
        print("Error: The column 'target' is not found. Please check the column names.")
        sys.exit(1)
    
    if data.isnull().sum().sum() > 0:
        print("Warning: Missing values detected. Filling with column means.")
        data.fillna(data.mean(), inplace=True)
    
    label_encoder = LabelEncoder()
    data['target'] = label_encoder.fit_transform(data['target'])
    
    for col in data.select_dtypes(include=['object']).columns:
        if col != 'target':
            data[col] = label_encoder.fit_transform(data[col])
    
    features = data.drop(columns=['target'])
    target = data['target']
    return features, target

def train_naive_bayes(features, target):
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=42)
    
    model = GaussianNB()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, predictions)
    print(f'Accuracy: {accuracy * 100:.2f}%')
    print("Classification Report:\n", classification_report(y_test, predictions))
    print("Confusion Matrix:\n", confusion_matrix(y_test, predictions))
    
    return model, X_test, y_test, predictions

def main():
    file_path = sys.argv[1] if len(sys.argv) > 1 else 'data_prac-6.csv'
    data = load_data(file_path)
    
    features, target = preprocess_data(data)
    
    model, X_test, y_test, predictions = train_naive_bayes(features, target)
    
    results = pd.DataFrame({'Actual': y_test, 'Predicted': predictions})
    print(results.head())

if __name__ == "__main__":
    main()
