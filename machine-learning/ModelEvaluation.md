# Key Modeling Terms

## Train-Test Split
The train-test split is a technique for evaluating the performance of a machine learning model. The dataset is divided into two parts:
- **Training Set**: Used to train the model.
- **Test Set**: Used to evaluate the model's performance on unseen data to ensure it generalizes well.

EDA and model fit should always be contained to the training data. Data leakage occurs when then test data is used in the modeling. This results in inaccurate estimates of model performance and generalizability.

### Example:
```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

Sure! Here is a short description of data leakage and its concerns in developing models:

## Data Leakage
Data leakage occurs when information from outside the training dataset is used to create the model, giving it an unintended advantage. This typically happens when the training data includes information that will not be available when the model is making predictions in a real-world scenario.

### Concerns with Data Leakage
- **Overestimated Performance**: Data leakage can cause the model to show unrealistically high performance during training and validation, as it has access to information it shouldn't have.
- **Poor Generalization**: Models affected by data leakage often fail to generalize to new, unseen data because they rely on spurious patterns present only in the training data.
- **Misleading Results**: Data leakage can lead to misleading conclusions about the model's effectiveness, which can be costly and time-consuming to correct.

### Example:
Including future information in the training data, such as using data from future time points in a time series forecast, or including a feature that directly leaks the target variable (e.g., including a feature that is derived from the target variable).

### Preventing Data Leakage:
- **Careful Data Splitting**: Ensure that data used for training, validation, and testing are properly separated.
- **Feature Engineering**: Be cautious during feature engineering to avoid incorporating future information or information derived from the target variable.
- **Cross-Validation**: Use appropriate cross-validation techniques that respect the data's temporal or hierarchical structure to prevent leakage.

By understanding and preventing data leakage, you can develop more robust models that perform reliably in real-world scenarios.

## Cross-Validation
Cross-validation is a technique for assessing how the results of a statistical analysis will generalize to an independent dataset. It involves partitioning the data into subsets, training the model on some subsets and validating it on the remaining subsets. The most common form is k-fold cross-validation.

### Example:
```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(model, X, y, cv=5)
```

## Metrics for Classification
Metrics used to evaluate the performance of classification models include:

- **Accuracy**: The ratio of correctly predicted instances to the total instances.
- **Precision**: The ratio of correctly predicted positive observations to the total predicted positives.
- **Recall (Sensitivity)**: The ratio of correctly predicted positive observations to all observations in the actual class.
- **F1 Score**: The harmonic mean of precision and recall.

### Example:
```python
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)
```

## Metrics for Regression
Metrics used to evaluate the performance of regression models include:

- **Mean Absolute Error (MAE)**: The average of the absolute errors between the predicted and actual values.
- **Mean Squared Error (MSE)**: The average of the squared errors between the predicted and actual values.
- **Root Mean Squared Error (RMSE)**: The square root of the mean squared error.
- **R-squared (R²)**: The proportion of the variance in the dependent variable that is predictable from the independent variables.

### Example:
```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

mae = mean_absolute_error(y_true, y_pred)
mse = mean_squared_error(y_true, y_pred)
rmse = mean_squared_error(y_true, y_pred, squared=False)
r2 = r2_score(y_true, y_pred)
```

## Confusion Matrix
A confusion matrix is a table used to describe the performance of a classification model. It shows the true positive, false positive, true negative, and false negative counts.

### Example:
```python
from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_true, y_pred)
```

## Overfitting
Overfitting occurs when a model learns the training data too well, capturing noise and details that do not generalize to new data. An overfitted model performs well on training data but poorly on test data.

### Signs of Overfitting:
- High accuracy on training data.
- Low accuracy on test data.

## Underfitting
Underfitting occurs when a model is too simple to capture the underlying patterns in the data. An underfitted model performs poorly on both training and test data.

### Signs of Underfitting:
- Low accuracy on training data.
- Low accuracy on test data.

---