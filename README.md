
# Customer Segmentation
### Description
In this project, we analyzed demographics data for customers of a mail-order sales company in Germany, comparing it against demographics information for the general population. We used unsupervised learning techniques to perform customer segmentation, identifying the parts of the population that best describe the core customer base of the company. Then, we applied what you've learned on a third dataset with demographics information for targets of a marketing campaign for the company, and use a model to predict which individuals are most likely to convert into becoming customers for the company. The data we used has been provided by our partners at Bertelsmann Arvato Analytics, and represents a real-life data science task.

### Project Breakdown
There are four parts to this project as discused below:
- Data Cleaning
- Feature Relevance
- Customer Segmentation
- Supervised Learning Model

#### Data Cleaning
In this section, we wrote some function to clean our data. Most of the algorithms we used in this project requires data to be in numeric format. A big chunk of our data cleaning process involves comverting dataframe string columns to numeric.

#### Feature Relevance
In this section, we analysed all the features we have in the dataset to come up with the most reasonable ones. Each dataset has 366 features which is too much. At the end of the section, we streamlined our dataset down to 100 features. The three algorithms we used are Variance Threshold, Correlation Matrix and Unsupervised Random Forest (using feature importance).

#### Customer Segmentation
In this section we were able to extract members of the general population that are likely to become customers. This is a typical example of unsupervised learning. We used K-Means Clustering to select population that falls in the same cluster as our customers population.

#### Supervised Learning Model
In this section, we created a model for prediction on a test data. We used RandomForestClassifier and XGBoostClassifier to make our predictions. One of the challenges we ran into was inbalance dataset. However, we used Synthetic Minority Oversampling Technique (SMOTE). Also we were able to create a custom data cleansing transformer that we used in our machine learning pipeline.

#### Project Files


### Installation
Most of the libraries needed comes pre-installed with python but some other installations are needed:
-   SQLAlchemy: `pip install SQLAlchemy`
-   nltk: `pip install --user -U nltk`
-   plotly: `pip install plotly`
### Instructions:
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Go to `app` directory: `cd app`

3. Run your web app: `python run.py`

4. Click the `PREVIEW` button to open the homepage
