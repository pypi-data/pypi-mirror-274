# Cleaner Panda
 Programming For Data Engineering course final project
 https://chat.openai.com/share/87c82e00-50af-446b-ac63-e82d9d35021a

### Missing Value Handler
- `strategy enum {MEAN, MEDIAN, CONSTANT, REMOVE_ROW, REMOVE_COLUMN, FORWARD_BACKWARD}`
- `cont_int = 0, const_str =”none”, const_date=01.01.2024…`
- `replace_missing_values(dataFrame, strategy=”strategy.MEAN”, column=0)` -> Replaces missing values on the “column” parameter according to the selected strategy. The “column” can be an index or column name as str.
- `replace_mean(dataframe, column)`
- `replace_median(dataframe, column)`
- `replace_constant(dataframe, column, constant)`
- `replace_remove_row(dataframe, column)`
- `replace_remove_column(dataframe, column)`
- `replace_forward_backward(dataframe, column)` // fill missing value with previous/next value

### Outlier Handler
- `identify_outliers_iqr(data, threshold=1.5)`
- `handle_outliers_iqr(data, threshold=1.5, replacement=None)` //replacement: Value to replace outliers with (e.g., median, mean) or None to remove outliers


### Scaler
- `standardize_data(dataframe)`
- `normalize_data(dataframe)`
- `robust_scale_data(dataframe)`
- `normalize_vectors(dataframe)`
- `log_transform_data(dataframe)`


### Text Cleaner
- `remove_common_words(dataframe, column)`
- `convert_to_lowercase(dataframe, column)` // Stopwords are words like "the", "is", "and", "in", etc., that occur frequently in a language
- `remove_punctuation(dataframe, column)`
- `lemmatization(dataframe, column)`
- `expand_contractions(dataframe, column)` // (e.g., "can't" to "cannot", "won't" to "will not")
- `remove_special_characters(dataframe, column, remove=[‘.’])`
- `remove_numerical(dataframe, column)`
- `filter_words(dataframe, column, remove=[“fuck”])`


### Data Type Converter
- 


### Categorical Encoder
- `label_encoding(dataframe, column)`
- `one_hot_encoding(dataframe, column)`
- `ordinal_encoding(dataframe, column)`


### Date Time Handler
- `convert_date_to_strings(dataframe column)`
- `extract_components(dataframe, column)`
- `reformat_date(dataframe, column)`
- `calculate_datetime_differences()`
- `convert_datetime_to_different_timezones`
- `shift_time()`
- `handle_irregular_time_intervals()`
