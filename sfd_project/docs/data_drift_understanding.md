# Data Drift Understanding

Data drift is the change in the feature distribution between training and serving data. It is a common problem in machine learning systems and can cause models to degrade in performance over time. Data drift can be caused by many factors, including changes in user behavior, changes in the underlying population, or changes in the relationships between features.

## Data drift during training pipeline

- Train and test dataset must have same distribution.
- Base dataset: Train
- To compare with: Test
- If same distribution: No data drift
- If different distribution: Data drift
  - Solution: Do the train-test split correctly

## Data drift during prediction pipeline

### Instance prediction

Not possible to detect data drift immediately.

Why?

- It is not possible to summarize one record.

Solution:

- Save each request in database, then fetch all request by hour or by day and then compare the distribution.
  - The collected dataset can be compared with the training dataset to detect data drift.
  - Create the data drift report, if huge data drift is detected, then retrain the model.
  - Else, keep collecting data and check for data drift periodically (like every day).

### Batch prediction

Possible to detect data drift immediately.

- Base dataset: Train
- To compare with: Batch dataset
- If same distribution: No data drift
- If different distribution: Data drift
  - Solution: Send alert that data drift is detected, then retrain the model including the existing training dataset and as well as batch dataset.

## Some other type of data drifts

### Concept drift

It related to the model, where the relation between input feature and target feature is changed.
Solution: Retrain the model.

### Target drift

If the distribution of target feature is changed, then we have the target drift.
Example: If the target feature includes 3 classes, but during prediction, we get new class (4th class).

Solution: Retrain the model.
