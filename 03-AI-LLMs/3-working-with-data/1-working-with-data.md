# Working with Data

## Introduction

In this lecture, we will focus on preparing data for a learning model. We'll discuss the importance of data preprocessing, explore common preprocessing techniques, and apply these concepts to a practical example using a dataset on water potability. By the end of this lecture, you'll have a solid understanding of how to clean, transform, and prepare your data to feed into a machine learning model.

## Lecture Content

### Importance of Data Preprocessing

Data preprocessing is a critical step in the machine learning pipeline. It involves cleaning and transforming raw data to improve the quality and performance of a model. Proper preprocessing ensures that the data is consistent, relevant, and ready for analysis.

#### Why Preprocess Data?

- **Consistency**: Handle missing values and outliers to ensure the dataset is uniform.
- **Relevance**: Select and engineer features that are most relevant to the problem.
- **Efficiency**: Normalize or scale data to improve model convergence and performance.

### Common Data Preprocessing Techniques

#### Handling Missing Values

Missing data can lead to incorrect model predictions. Common strategies include:

- **Removal**: Discard rows or columns with missing values.
- **Imputation**: Replace missing values with mean, median, mode, or other values.
- **Interpolation**: Estimate missing values based on other data points.

#### Scaling and Normalization

Different features may have different scales, which can affect model performance. Common techniques include:

- **Min-Max Scaling**: Scales data to a fixed range, typically [0, 1].
- **Standardization**: Centers data around the mean with a unit standard deviation.

#### Splitting Data

Split the dataset into training and testing sets to evaluate model performance. Common splits are:

- **Training Set**: Used to train the model.
- **Testing Set**: Used to evaluate the model's performance.

> If you train your model on all of the data you have available it will memorize your data but not make accurate predictions. Try to follow the 80%(training) 20%(testing) rule.

### Practical Example: Water Potability Dataset

### Dataset Description

We will work with the [water_potability.csv](./resources/water_potability.csv) dataset. The dataset includes various water quality metrics, such as pH, Hardness, Solids, Chloramines, Sulfate, Conductivity, Organic Carbon, Trihalomethanes, Turbidity, and a target variable `Potability` indicating whether the water is potable (0 or 1).

#### Loading the Data

Our typical approach to CSV files up to this point has been strictly oriented to `python csv` and it works well, but when we are working with data there is definitely a more efficient way to communicate with these files and extract each row as a tensor.

##### Utilizing Pandas to read csv files

Let's make sure we have Pandas installed within our Python Virtual Environment.

```bash
  pip install pandas
```

Now that we have Pandas available within our Python venv, we can utilize it within Jupyter Notebook to work with our csv data.

```python
import pandas as pd
# Load the dataset
data = pd.read_csv('./resources/water_potability.csv')
print(data) 
```

You can see how our data is being analyzed and printed onto our JupyterNotebook file almost as if it were the return statement of an SQL query. Well, just like in SQL we can select specific columns utilizing the header of the column we want to grab.

```python
data['<header'] # grabs a column
data.iloc[<num_row>] #grabs the row matching said num
data.iloc[<from_row>:<to_row>] # returns a slice of rows
```

We will see a couple of other methods Pandas has to offer when handling data.

##### Handle Missing Values

First lets determine how many values are null and this could help us decide how to handle our null values.

```python
# Check for missing values
print(data.isnull().sum())
```

Because our Sulfate data is missing a considerable amount of data, we may want to utilize `imputation` by replacing the null values by the mean of the column.

```python
# Impute missing values with the mean of each column
data.fillna(data.mean(), inplace=True)
```

##### Scale/Normalize our Data

Unfortunately, Pandas doesn't have this capability easily built in. Instead we will utilize a tool from `scikit-learn` to standardize and scale our data.

```python
from sklearn.preprocessing import StandardScaler

# Select features and target
features = data.drop('Potability', axis=1)
target = data['Potability']

# Standardize the features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)
```

##### Splitting Data and Placing it within Tensors

Split the dataset into training and testing sets.

```python
from sklearn.model_selection import train_test_split

# Split the data
X_train, X_test, y_train, y_test = train_test_split(scaled_features, target, test_size=0.2, random_state=42)
```

Lets take some time and break down the command above:

- **scaled_features**: This is typically a 2D array or DataFrame containing the features (independent variables) that you want to use for training your model.
target: This is usually a 1D array or Series containing the labels or targets (dependent variables) corresponding to the features.
- **test_size=0.2**: This specifies the proportion of the dataset to include in the test split. In this case, 20% of the data will be used for testing, while 80% will be used for training.
- **random_state=42**: This sets a seed for the random number generator. By specifying a random_state, you ensure that the split is reproducible; you'll get the same split every time you run the code.

```python
# Convert to PyTorch tensors
X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train.values, dtype=torch.float32).view(-1, 1)
y_test_tensor = torch.tensor(y_test.values, dtype=torch.float32).view(-1, 1)
```

### Testing our Model

Now lets adjust our model and feed 2 separate tensors into it to see what predictions it's able to make.

```python
class BinaryModel(nn.Module):
    def __init__(self):
        super(BinaryModel, self).__init__()
        self.linear1 = nn.Linear(9, 7)
        self.linear2 = nn.Linear(7, 4)
        self.linear3 = nn.Linear(4, 1)
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        x = self.linear1(x)
        x = self.linear2(x)
        x = self.linear3(x)
        x = self.sigmoid(x)
        return x

# Create an instance of the model
model = BinaryModel()
print(model(X_train_tensor[0])) #label: 0
print(model(X_train_tensor[406])) #label: 1
```

## Exercises

1. **Handling Missing Data**: Experiment with different strategies for handling missing data and observe the impact on model performance.
2. **Feature Scaling**: Try different scaling techniques (Min-Max Scaling, Standardization) and compare their effects.
3. **Data Splitting**: Use different data splitting ratios and analyze how they affect the model's performance.

## Conclusion

In this lecture, we covered the essential steps of data preprocessing, including handling missing values, scaling data, and preparing data for a PyTorch learning model. These steps are crucial for building effective and accurate machine learning models.
