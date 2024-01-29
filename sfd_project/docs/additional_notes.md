## Training pipeline

    You may need to modifiy data_transformation and model_trainer components to suit your needs. For example, if you want to add different transformation steps or use a different model, then you can try them on Jupiter notebook first and then add them to the pipeline components (data_transformation and model_trainer).

### MLflow

    To achive best F1 score, params can be tuned as following:

    ```bash
        learning_rate: 0.1
        n_estimators: 400
        max_depth: 5
    ```
    The best F1 score is 0.87
