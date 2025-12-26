from datetime import datetime
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from airflow.models import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
from joblib import load, dump
import os
from sklearn.ensemble import RandomForestClassifier

DATA_DIR = "/opt/airflow/data"

def preprocess_data():
    cleveland = pd.read_csv(f"{DATA_DIR}/cleveland.csv")
    X = cleveland.drop(columns=['label'])
    y = cleveland['label']
    dump(X, f"{DATA_DIR}/X.pkl")
    dump(y, f"{DATA_DIR}/y.pkl")

def split_data():
    X = load(f"{DATA_DIR}/X.pkl")
    y = load(f"{DATA_DIR}/y.pkl")
    X_train, X_test, y_train, y_test =  train_test_split(X, y, test_size=0.2, random_state=42)
    dump(X_train, "data/X_train.pkl")
    dump(X_test, "data/X_test.pkl")
    dump(y_train, "data/y_train.pkl")
    dump(y_test, "data/y_test.pkl")
 
def train():
    X_train = load("data/X_train.pkl")
    y_train = load("data/y_train.pkl")
    model  = RandomForestClassifier(n_estimators=100, max_depth=7,random_state=42)
    model.fit(X_train, y_train)
    dump(model, "data/model.pkl")

def evaluate(): 
    X_test = load("data/X_test.pkl")
    y_test = load("data/y_test.pkl")
    model = load("data/model.pkl")
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    accuracy = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_proba)
    print({"accuracy": accuracy, "roc_auc": roc_auc})

with DAG(
    dag_id='heart_risk_pred_pipeline',
    schedule='@daily',
    start_date=datetime(2025, 12, 26),
    catchup=False) as dag:
    task_preprocess_data = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_data
    )
    task_split_data = PythonOperator(
        task_id='split_data',
        python_callable=split_data
    )
    task_train = PythonOperator(
        task_id='train',
        python_callable=train
    )
    task_evaluate = PythonOperator(
        task_id='evaluate',
        python_callable=evaluate
    )

    task_preprocess_data >> task_split_data >> task_train >> task_evaluate
