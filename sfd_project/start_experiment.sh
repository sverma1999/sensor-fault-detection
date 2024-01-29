#!/bin/bash

# Define the arrays of parameters
learning_rates=(0.01 0.03 0.05 0.10 0.15 0.20 0.25 0.30)
n_estimators=(100 200 300 400 500)
max_depths=(1 3 5 6 8 10 12 15)

# Iterate over each combination of parameters
for lr in "${learning_rates[@]}"; do
    for ne in "${n_estimators[@]}"; do
        
        for md in "${max_depths[@]}"; do
            # Update params.yaml file
            sed -i '' "s/  learning_rate: .*/  learning_rate: $lr/" config/params.yaml
            sed -i '' "s/  n_estimators: .*/  n_estimators: $ne/" config/params.yaml
            sed -i '' "s/  max_depth: .*/  max_depth: $md/" config/params.yaml

            # Run the Python script
            python main.py

            # Optional: Add a log or print statement to keep track of progress
            echo "Completed: learning_rate=$lr, n_estimators=$ne, max_depth=$md"
        done
        echo "-------------------------------------------"
    done
    echo ";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;"
done
