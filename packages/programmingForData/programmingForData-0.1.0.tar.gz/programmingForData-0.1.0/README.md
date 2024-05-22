# Data Preprocessing Library

A comprehensive library for data preprocessing tasks, including data cleaning, transformation, and visualization.

## Installation

To install the library, use pip:


`pip install data_preprocessing_library`

### Usage
#### Outlier Handling
```
import pandas as pd
from data_preprocessing_library.outlier_handler import OutlierHandler

data = pd.DataFrame({'A': [1, 2, 3, 4, 100]})
outlier_handler = OutlierHandler()

# Remove outliers using IQR method
cleaned_data = outlier_handler.iqr_outliers(data, 'A')
print(cleaned_data)

# Replace outliers with median
data = outlier_handler.replace_outliers_with_median(data, 'A')
print(data)
```


#### Scaling
```
import pandas as pd
from data_preprocessing_library.scaler import Scaler

data = pd.DataFrame({'A': [1, 2, 3, 4, 5]})
scaler = Scaler()

# Min-Max scaling
scaled_data = scaler.min_max_scale(data)
print(scaled_data)

# Standard scaling
standard_scaled_data = scaler.standard_scale(data)
print(standard_scaled_data)
```
#### Handling Missing Values
```
import pandas as pd
from data_preprocessing_library.missing_value_handler import MissingValueHandler

data = pd.DataFrame({'A': [1, 2, None, 4, 5]})
missing_value_handler = MissingValueHandler()

# Fill missing values with mean
data = missing_value_handler.fill_mean(data, ['A'])
print(data)

# Drop rows with missing values
data = missing_value_handler.drop_missing(data)
print(data)
```
#### Visualization
```
import pandas as pd
from data_preprocessing_library.visualizer import Visualizer

data = pd.DataFrame({'A': [1, 2, 3, 4, 5], 'B': [5, 4, 3, 2, 1]})
visualizer = Visualizer()

# Plot histogram
visualizer.plot_histogram(data, 'A')

# Plot boxplot
visualizer.plot_boxplot(data, 'A')

# Plot scatter plot
visualizer.plot_scatter(data, 'A', 'B')

# Plot correlation matrix
visualizer.plot_correlation_matrix(data)
```
#### Filtering Data
```
import pandas as pd
from data_preprocessing_library.data_filter import DataFilter

data = pd.DataFrame({'A': [1, 2, 3, 4, 5], 'B': [5, 4, 3, 2, 1]})
data_filter = DataFilter()

# Filter data by condition
filtered_data = data_filter.filter_by_condition(data, 'A > 2')
print(filtered_data)

# Filter specific columns
filtered_columns = data_filter.filter_by_columns(data, ['A'])
print(filtered_columns)
```
#### Encoding Categorical Data
```
import pandas as pd
from data_preprocessing_library.categorical_encoder import CategoricalEncoder

data = pd.DataFrame({'Category': ['A', 'B', 'A', 'C']})
encoder = CategoricalEncoder()

# One-hot encoding
one_hot_encoded_data = encoder.one_hot_encode(data, 'Category')
print(one_hot_encoded_data)

# Label encoding
label_encoded_data = encoder.label_encode(data, 'Category')
print(label_encoded_data)
```
#### Budget Categorization
```
import pandas as pd
from data_preprocessing_library.budget_handler import BudgetHandler

data = pd.DataFrame({'Budget': [500000, 20000000, 300000000]})
budget_handler = BudgetHandler()

# Categorize budget
categorized_data = budget_handler.categorize_budget(data, 'Budget')
print(categorized_data)
```
#### Data Type Conversion
```
import pandas as pd
from data_preprocessing_library.data_type_converter import DataTypeConverter

data = pd.DataFrame({'A': ['1', '2', '3'], 'B': [1, 2, 3]})
converter = DataTypeConverter()

# Convert to numeric
numeric_data = converter.convert_to_numeric(data, ['A'])
print(numeric_data)

# Convert to categorical
categorical_data = converter.convert_to_categorical(data, ['B'])
print(categorical_data)
```
#### Date and Time Handling
```
import pandas as pd
from data_preprocessing_library.date_time_handler import DateTimeHandler

data = pd.DataFrame({'Date': ['01/01/2020', '02/01/2020', '03/01/2020']})
date_time_handler = DateTimeHandler()

# Convert to datetime
datetime_data = date_time_handler.convert_to_datetime(data, 'Date')
print(datetime_data)

# Extract date parts
date_parts = date_time_handler.extract_date_parts(datetime_data, 'Date')
print(date_parts)
```