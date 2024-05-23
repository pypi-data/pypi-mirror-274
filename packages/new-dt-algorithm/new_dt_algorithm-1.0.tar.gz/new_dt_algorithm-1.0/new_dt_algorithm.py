import numpy as np
import  warnings
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
warnings.filterwarnings('ignore')
import pandas as pd
from sklearn.feature_selection import mutual_info_classif
from scipy.stats import kruskal, f_oneway
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from statsmodels.stats.outliers_influence import variance_inflation_factor as vif
from sklearn.ensemble import RandomForestClassifier
import statsmodels.api as sm  
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import pandas as pd

class new_dt_algorithm:
    """
    A class for implementing a new decision tree-based algorithm for feature selection and model training.

    This class provides functionality for data preprocessing, feature selection, and model training using a decision tree approach.
    The primary goal is to select important features and build a stable decision tree model that generalizes well to test data.

    Attributes:
        model: The trained decision tree model.
        mi_cutoff (float): Mutual information cutoff threshold for feature selection.
        ks_test_cutoff (float): Kolmogorov-Smirnov test cutoff threshold for feature selection.
        anova_test_cutoff (float): ANOVA test cutoff threshold for feature selection.
        test_data (DataFrame): Test dataset after preprocessing.
        train_data (DataFrame): Train dataset after preprocessing.
        mi_features (list): Features selected based on mutual information.
        ks_features (list): Features selected based on Kolmogorov-Smirnov test.
        anova_features (list): Features selected based on ANOVA test.
        iv_features (list): Features selected based on Information Value calculation.
        logit_features (list): Features selected based on Logistic Regression.
        non_ml_features (list): Features selected using non-machine learning methods.
        rf_features (list): Features selected based on Random Forest.
        final_features (list): Final selected features for model training.

    Methods:
        __init__: Initialize the object with default attributes.
        read_data: Read and preprocess the input data.
        training_decision_tree: Train a decision tree model with specified parameters.
    """

    def __init__(self):
        """
        Initialize the object with default attributes.

        This method initializes the object with default attributes set to None, which will be populated
        during the preprocessing and feature selection steps.
        """
        self.data  =None
        self.model = None
        self.mi_cutoff = None
        self.ks_test_cutoff = None
        self.anova_test_cutoff = None
        self.iv_cutoff = None
        self.ml_cutoff = None
        self.rf_cutoff = None
        self.test_data = None
        self.train_data = None
        self.mi_features = None
        self.ks_features = None
        self.anova_features = None
        self.iv_features = None
        self.logit_features = None
        self.non_ml_features = None
        self.rf_features = None
        self.final_features = None

        
        

    def read_data(self, data, Target, na_impute=-99999):
        """
        Read and preprocess data.

        This method reads the input DataFrame, preprocesses it, and stores it for further analysis.

        Parameters:
            data (DataFrame): Input DataFrame containing the dataset.
            Target (str): Name of the target variable in the dataset.
            na_impute (int, optional): Value to use for imputing missing values. Default is -99999.

        Returns:
            None

        Preprocessing Steps:
        1. Convert column names to lowercase.
        2. Convert the target variable to numeric, coercing errors.
        3. Remove columns and rows that contain all missing values.
        4. Fill missing values with the specified imputation value.
        5. Drop columns with only one unique value or with more than 25 unique values or compound strings with delimiter '-'.
        6. Convert categorical variables into dummy/indicator variables.
        7. Convert all columns to numeric type.
        8. If a column has only two unique values, convert it to integer type.

        Note:
        - Columns with 'unnamed' in their names are dropped from the dataset.
        """
        self.__init__()
        self.data = data
        self.Target = Target.lower()
        self.data.columns = self.data.columns.str.lower()
        self.data  = self.data.loc[:, ~self.data.columns.duplicated()]
        self.data[self.Target] = pd.to_numeric(self.data[self.Target], errors='coerce')
        if self.data[self.Target].nunique()>2:
            self.data = self.data[self.data[self.Target]!=self.data[self.Target].min()]
        self.data = self.data.dropna(axis=1, how="all")
        self.data = self.data.dropna(axis=0, how="all")
        self.data = self.data.fillna(na_impute)
        self.data.reset_index(drop=True,inplace=True)
        for col in self.data.columns:
            if self.data[col].nunique() <= 1:
                del self.data[col]
            else:    
                try:
                    pd.to_numeric(self.data[col])
                except Exception as e: 
                    if (self.data[col].nunique() > 25) or (len(self.data[col].astype(str).str.split('-').loc[0]) > 1):
                        del self.data[col]
                    else:
                        self.data = pd.get_dummies(self.data, columns=[col])
        
        for col in self.data.columns:
            self.data[col] = pd.to_numeric(self.data[col])
            if self.data[col].value_counts().reset_index().shape[0] == 2:
                self.data[col] = self.data[col].astype(int)   
        
        self.data = self.data.drop([x for x in list(self.data.columns) if 'unnamed' in x], axis=1)
        for col in self.data.drop([self.Target],axis=1).columns:
            try:
                self.data[col] = self.data[col].astype('float64')
                self.data[col].replace(to_replace = {np.inf : -99999 , -np.inf : -99999}, inplace=True)

            except Exception as e:
                del self.data[col]
        self.data.reset_index(drop=True,inplace=True)

        
    def add_or_remove_feature(self, addition_feature_name=None, removing_feature_name=None):
        """
        Add or remove a feature from the dataset.

        Parameters:
            addition_feature_name (str): The name of the feature to add.
            removing_feature_name (str): The name of the feature to remove.

        Returns:
            None
        """
        # Ensure that features have been filtered first
        if self.final_features is None:
            print('Please filter features first.')
        else:
            # Add a feature if addition_feature_name is provided and it exists in the dataset
            if addition_feature_name is not None:
                if addition_feature_name in self.data.columns:
                    self.final_features.append(addition_feature_name)

            # Remove a feature if removing_feature_name is provided and it exists in the final features
            if removing_feature_name is not None:
                if removing_feature_name in self.final_features:
                    self.final_features.remove(removing_feature_name)
                              
    def iv_woe(self, data, target, bins=10, show_woe=False):
        """
        Calculate Information Value (IV) and Weight of Evidence (WoE) for given data and target variable.

        Parameters:
            data (DataFrame): Input DataFrame containing independent variables and the target variable.
            target (str): Name of the target variable.
            bins (int): Number of bins for continuous variables.
            show_woe (bool): Flag to display the WoE table.

        Returns:
            DataFrame: DataFrame containing IV values for each independent variable.
            DataFrame: DataFrame containing WoE values for each category of each independent variable.
        """
        import pandas as pd
        import numpy as np

        newDF, woeDF = pd.DataFrame(), pd.DataFrame()

        # Extract column names of independent variables
        selected_features = list(data.drop([target], axis=1).columns)

        # Calculate WoE and IV for each independent variable
        for ivar in selected_features:
            if (data[ivar].dtype.kind in 'bifc') and (len(np.unique(data[ivar])) > 10):
                # For continuous variables, discretize into bins
                binned_x = pd.qcut(data[ivar], bins, duplicates='drop')
                d0 = pd.DataFrame({'x': binned_x, 'y': data[target]})
            else:
                d0 = pd.DataFrame({'x': data[ivar], 'y': data[target]})

            # Calculate counts and sums for events and non-events
            d = d0.groupby("x", as_index=False).agg({"y": ["count", "sum"]})
            d.columns = ['Cutoff', 'N', 'Events']
            d['% of Events'] = np.maximum(d['Events'], 0.5) / d['Events'].sum()
            d['Non-Events'] = d['N'] - d['Events']
            d['% of Non-Events'] = np.maximum(d['Non-Events'], 0.5) / d['Non-Events'].sum()
            d['WoE'] = np.log(d['% of Events'] / d['% of Non-Events'])
            d['IV'] = d['WoE'] * (d['% of Events'] - d['% of Non-Events'])
            d.insert(loc=0, column='Variable', value=ivar)

            # Concatenate IV values
            temp = pd.DataFrame({"Variable": [ivar], "IV": [d['IV'].sum()]}, columns=["Variable", "IV"])
            newDF = pd.concat([newDF, temp], axis=0)

            # Concatenate WoE values
            woeDF = pd.concat([woeDF, d], axis=0)

            # Show WoE table
            if show_woe:
                print(d)

        return newDF, woeDF



    def feature_selection_auto(self,mi_cutoff = 0,ks_test_cutoff = 0.10, anova_test_cutoff=0.10, iv_cutoff=0.005, ml_cutoff=100000, rf_cutoff=0.800):

        """
        Filter features using multiple iterations of feature selection methods.

        This method performs multiple iterations of feature selection using various techniques
        including Mutual Information, Kruskal-Wallis H-test, ANOVA test, Information Value, Logistic Regression,
        Multicollinearity removal, and Random Forest. Features are iteratively selected and filtered
        based on their relevance, statistical significance, and predictive power with respect to the target variable.

        Parameters:
        - mi_cutoff (float, optional): Mutual Information cutoff value. Default is 0.
        - ks_test_cutoff (float, optional): Kruskal-Wallis test cutoff value. Default is 0.10.
        - anova_test_cutoff (float, optional): ANOVA test cutoff value. Default is 0.10.
        - iv_cutoff (float, optional): Information Value (IV) cutoff value. Default is 0.005.
        - ml_cutoff (int, optional): Multicollinearity cutoff value. Default is 100000.
        - rf_cutoff (float, optional): Random Forest cutoff value. Default is 0.80.

        Returns:
        None

        Notes:
        - This method iterates through multiple feature selection techniques sequentially.
        - Each iteration applies a specific feature selection method with the specified cutoff values.
        - The order of iterations is as follows:
            1. Mutual Information iteration
            2. Kruskal-Wallis H-test iteration
            3. ANOVA test iteration
            4. Information Value iteration
            5. Logistic Regression iteration
            6. Multicollinearity removal iteration
            7. Random Forest iteration
        - The specified cutoff values determine the threshold for selecting features in each iteration.
        - Features selected in each iteration are stored and updated in the respective class attributes.

        """
        if self.data is None:
            print('pls read data first')
        else:            
            self.mi_cutoff = mi_cutoff
            self.ks_test_cutoff = ks_test_cutoff
            self.anova_test_cutoff = anova_test_cutoff
            self.iv_cutoff = iv_cutoff
            self.ml_cutoff = ml_cutoff
            self.rf_cutoff = rf_cutoff

            # First iteration based on mutual information
            self.mutual_information_iteration(mi_cutoff = mi_cutoff)

            # Second iteration based on statistical test
            self.Kruskal_test_iteration(ks_test_cutoff = ks_test_cutoff)

            # Third iteration based on ANOVA test
            self.anova_test_iteration(anova_test_cutoff=anova_test_cutoff)

            # Fourth iteration based on information value
            self.information_value_iteration(iv_cutoff=iv_cutoff)

            # Fifth iteration based on L1 Logistic Regression
            self.logistic_iteration()

            # Sixth iteration based on multicollinearity removal
            self.multicollinearity_iteration(ml_cutoff=ml_cutoff)

            # Seventh iteration based on Random Forest
            self.random_forest_iteration(rf_cutoff=rf_cutoff)

    def mutual_information_iteration(self,mi_cutoff = 0):

        """
        Perform feature selection using Mutual Information.

        This method applies Mutual Information to assess the importance of each feature
        with respect to the target variable. Features with Mutual Information values above
        a specified cutoff threshold are selected for inclusion in the model.

        Parameters:
        - mi_cutoff (float, optional): The cutoff threshold for Mutual Information values.
          Features with Mutual Information above this threshold will be selected. Default is 0.

        Attributes Modified:
        - mi_features (list): List of selected features after Mutual Information test iteration.
        - final_features (list): List of selected features after Mutual Information test iteration.

        Notes:
        - If `mi_features` attribute is already populated, indicating that the method has been
          executed previously, a message will be printed indicating the same.

        - If `final_features` attribute is None, the method will use all features except the
          target variable for feature selection. Otherwise, it will use the features specified
          in `final_features`.

        - Mutual Information is a measure of the amount of information obtained about one
          random variable through another random variable. It quantifies the amount of
          dependence between the variables.

        - Features with Mutual Information values above the cutoff threshold are selected
          for inclusion in the model.

        - After feature selection, the selected features are stored in both `mi_features` and
          `final_features` attributes.

        - A message indicating the number of selected features out of total features is printed
          to provide feedback on the feature selection process.

        Mutual Information Test Explanation:
        Mutual Information measures the amount of information shared between two random variables.
        In this context, Mutual Information is used to assess the relevance of each feature with
        respect to the target variable.

        The method computes Mutual Information values for each feature using the `mutual_info_classif`
        function. Features with Mutual Information values above the specified cutoff threshold are
        considered to be informative for predicting the target variable and are selected for inclusion
        in the model.

        If the method has been executed previously, it will skip the feature selection process
        and print a message indicating that the Mutual Information iteration has already been executed.
        """
        if self.data is None:
            print('pls read data first')
        else:            
            if self.mi_features is None:
                self.mi_cutoff = mi_cutoff
                if self.final_features is None:
                    mi_values = mutual_info_classif(self.data.drop([self.Target],axis=1), self.data[[self.Target]])
                    top_k_indices = np.argsort(mi_values)[::-1][:]
                    top_k_features = self.data.drop([self.Target],axis=1).columns[top_k_indices]
                    mi_features = [feature for feature, mi_val in zip(top_k_features, mi_values[top_k_indices]) if mi_val > self.mi_cutoff]
                    self.mi_value = pd.DataFrame([(feature, mi_val) for feature, mi_val in zip(top_k_features, mi_values[top_k_indices]) if mi_val > self.mi_cutoff], columns=['Feature', 'MI_Value']).copy()
                    print(f"{len(mi_features)} features remaining out of {self.data.shape[1]-1} after mutual information test iteration")
                    self.mi_features = mi_features.copy()
                    self.final_features = mi_features.copy()
                else:
                    mi_values = mutual_info_classif(self.data[self.final_features], self.data[[self.Target]])
                    top_k_indices = np.argsort(mi_values)[::-1][:]
                    top_k_features = self.data[self.final_features].columns[top_k_indices]
                    mi_features = [feature for feature, mi_val in zip(top_k_features, mi_values[top_k_indices]) if mi_val > self.mi_cutoff]
                    self.mi_value = pd.DataFrame([(feature, mi_val) for feature, mi_val in zip(top_k_features, mi_values[top_k_indices])], columns=['Feature', 'MI_Value']).copy()
                    print(f"{len(mi_features)} features remaining out of {len(self.final_features)} after mutual information test iteration")
                    self.mi_features = mi_features.copy()
                    self.final_features = mi_features.copy()           
            else:
                 print('mi iteration already executed if you want iteration pls assign class.mi_features=None')



    def Kruskal_test_iteration(self,ks_test_cutoff = 0.10):
        """
        Perform feature selection using ANOVA F-test.

        This method applies ANOVA F-test to assess the statistical significance of each feature
        with respect to the target variable. Features with p-values below a specified cutoff threshold
        are selected for inclusion in the model.

        Parameters:
        - anova_test_cutoff (float, optional): The cutoff threshold for p-value from ANOVA test.
          Features with p-values below this threshold will be selected. Default is 0.10.

        Attributes Modified:
        - anova_features (list): List of selected features after ANOVA test iteration.
        - final_features (list): List of selected features after ANOVA test iteration.

        Notes:
        - If `anova_features` attribute is already populated, indicating that the method has been
          executed previously, a message will be printed indicating the same.

        - If `final_features` attribute is None, the method will use all features except the
          target variable for feature selection. Otherwise, it will use the features specified
          in `final_features`.

        - ANOVA F-test is performed for each feature to determine whether the means of the feature
          values differ significantly across different classes of the target variable.

        - Features with p-values below the cutoff threshold are selected for inclusion in the model.

        - After feature selection, the selected features are stored in both `anova_features` and
          `final_features` attributes.

        - A message indicating the number of selected features out of total features is printed
          to provide feedback on the feature selection process.

        ANOVA Test Explanation:
        The ANOVA, or Analysis of Variance, test compares the means of three or more groups to
        determine if there are statistically significant differences between them. It assesses
        whether the variation between group means is greater than the variation within groups.

        The test generates an F-statistic and a p-value. A low p-value indicates that at least
        one group mean is significantly different from the others.

        When applied in this method, the dataset is grouped by unique classes of the target variable,
        and the ANOVA F-test is performed for each feature. Features with p-values below the specified
        cutoff threshold are considered statistically significant and selected for inclusion in the model.

        If the method has been executed previously, it will skip the feature selection process
        and print a message indicating that the ANOVA test iteration has already been executed.
        """
        if self.data is None:
            print('pls read data first')
        else:            
            if self.ks_features is None:
                self.ks_test_cutoff = ks_test_cutoff
                if self.final_features is None:     
                    ks_features = []
                    all_features = []
                    all_pvalue =[]
                    for feature in self.data.drop([self.Target],axis=1).columns:
                        result = kruskal(*[self.data[self.data[self.Target] == group][feature] for group in self.data[self.Target].unique()])
                        all_features.append(feature)
                        all_pvalue.append(result.pvalue)
                        if result.pvalue < self.ks_test_cutoff:
                            ks_features.append(feature)
                    print(f"{len(ks_features)} features remaining out of {self.data.shape[1]-1} after Kruskal test iteration")
                    self.ks_features = ks_features.copy()
                    self.final_features = ks_features.copy()
                    self.ks_pvalue = pd.DataFrame({'Feature': all_features, 'P_Value': all_pvalue}).copy()
                else: 
                    all_features = []
                    all_pvalue = []            
                    ks_features = []
                    for feature in self.final_features:
                        result = kruskal(*[self.data[self.data[self.Target] == group][feature] for group in self.data[self.Target].unique()])
                        all_features.append(feature)
                        all_pvalue.append(result.pvalue)               
                        if result.pvalue < self.ks_test_cutoff:
                            ks_features.append(feature)
                    print(f"{len(ks_features)} features remaining out of {len(self.final_features)} after Kruskal test iteration")
                    self.ks_features = ks_features.copy()
                    self.final_features = ks_features.copy()
                    self.ks_pvalue = pd.DataFrame({'Feature': all_features, 'P_Value': all_pvalue}).copy()
            else:
                 print('krushal test iteration already executed if you want proceed pls assign class.ks_features=None')


    def anova_test_iteration(self,anova_test_cutoff =0.10):
        """
        Perform feature selection using ANOVA F-test.

        This method applies ANOVA F-test to assess the statistical significance of each feature
        with respect to the target variable. Features with p-values below a specified cutoff threshold
        are selected for inclusion in the model.

        Parameters:
        - anova_test_cutoff (float, optional): The cutoff threshold for p-value from ANOVA test.
          Features with p-values below this threshold will be selected. Default is 0.10.

        Attributes Modified:
        - anova_features (list): List of selected features after ANOVA test iteration.
        - final_features (list): List of selected features after ANOVA test iteration.

        Notes:
        - If `anova_features` attribute is already populated, indicating that the method has been
          executed previously, a message will be printed indicating the same.

        - If `final_features` attribute is None, the method will use all features except the
          target variable for feature selection. Otherwise, it will use the features specified
          in `final_features`.

        - ANOVA F-test is performed for each feature to determine whether the means of the feature
          values differ significantly across different classes of the target variable.

        - Features with p-values below the cutoff threshold are selected for inclusion in the model.

        - After feature selection, the selected features are stored in both `anova_features` and
          `final_features` attributes.

        - A message indicating the number of selected features out of total features is printed
          to provide feedback on the feature selection process.

        ANOVA Test Explanation:
        The ANOVA, or Analysis of Variance, test compares the means of three or more groups to
        determine if there are statistically significant differences between them. It assesses
        whether the variation between group means is greater than the variation within groups.

        The test generates an F-statistic and a p-value. A low p-value indicates that at least
        one group mean is significantly different from the others.

        When applied in this method, the dataset is grouped by unique classes of the target variable,
        and the ANOVA F-test is performed for each feature. Features with p-values below the specified
        cutoff threshold are considered statistically significant and selected for inclusion in the model.

        If the method has been executed previously, it will skip the feature selection process
        and print a message indicating that the ANOVA test iteration has already been executed.
        """
        if self.data is None:
            print('pls read data first')
        else:            
            if self.anova_features is None:
                self.anova_test_cutoff = anova_test_cutoff
                if self.final_features is None:     
                    anova_features = []
                    all_features = []
                    all_pvalue = []              
                    for feature_column in self.data.drop([self.Target],axis=1).columns:
                        groups = [self.data[self.data[self.Target] == cls][feature_column] for cls in self.data[self.Target].unique()]
                        f_statistic, p_value = f_oneway(*groups)
                        all_features.append(feature_column)
                        all_pvalue.append(p_value)                             
                        if p_value < self.anova_test_cutoff:
                            anova_features.append(feature_column)
                    print(f"{len(anova_features)} features remaining out of {self.data.shape[1]-1} after Anova test iteration")
                    self.anova_features = anova_features.copy()
                    self.final_features = anova_features.copy()
                    self.anova_pvalue = pd.DataFrame({'Feature': all_features, 'P_Value': all_pvalue}).copy()            
                else:   
                    anova_features = []
                    all_features = []
                    all_pvalue = []              
                    for feature_column in self.final_features:
                        groups = [self.data[self.data[self.Target] == cls][feature_column] for cls in self.data[self.Target].unique()]
                        f_statistic, p_value = f_oneway(*groups)
                        all_features.append(feature_column)
                        all_pvalue.append(p_value)                             
                        if p_value < self.anova_test_cutoff:
                            anova_features.append(feature_column)
                    print(f"{len(anova_features)} features remaining out of {len(self.final_features)} after Anova test iteration")
                    self.anova_features = anova_features.copy()
                    self.final_features = anova_features.copy()  
                    self.anova_pvalue = pd.DataFrame({'Feature': all_features, 'P_Value': all_pvalue}).copy()

            else:
                 print('Anova test iteration already executed if you want proceed pls assign class.anova_features=None')

    def information_value_iteration(self,iv_cutoff =0.005):
        """
        Perform feature selection based on Information Value (IV) calculation.

        This method calculates the Information Value (IV) for each feature to assess its predictive
        power for the target variable. Features with IV above a specified cutoff threshold are selected
        for inclusion in the model.

        Parameters:
        - iv_cutoff (float, optional): The cutoff threshold for Information Value (IV).
          Features with IV above this threshold will be selected. Default is 0.005.

        Attributes Modified:
        - iv_features (list): List of selected features after information value iteration.
        - final_features (list): List of selected features after information value iteration.

        Notes:
        - If `iv_features` attribute is already populated, indicating that the method has been
          executed previously, a message will be printed indicating the same.

        - If `final_features` attribute is None, the method will use all features except the
          target variable for feature selection. Otherwise, it will use the features specified
          in `final_features`.

        - Information Value (IV) and Weight of Evidence (WOE) are calculated for each feature
          using the `iv_woe` method.

        - Features with IV above the cutoff threshold are selected for inclusion in the model.

        - After feature selection, the selected features are stored in both `iv_features` and
          `final_features` attributes.

        - A message indicating the number of selected features out of total features is printed
          to provide feedback on the feature selection process.
        """
        if self.data is None:
            print('pls read data first')
        else:            
            if self.iv_features is None:
                self.iv_cutoff = iv_cutoff
                if self.final_features is None:
                    iv, woe = self.iv_woe(data=self.data, target=self.Target, bins=10, show_woe=False)
                    self.woe = woe.copy()
                    self.iv = iv.copy()                
                    iv_features = iv[iv['IV'] > self.iv_cutoff]['Variable'].to_list()                
                    print(f"{len(iv_features)} features remaining out of {self.data.shape[1]-1} after information value iteration")
                    self.iv_features = iv_features.copy()
                    self.final_features = iv_features.copy()
                else:   
                    iv, woe = self.iv_woe(data=self.data[self.final_features+[self.Target]], target=self.Target, bins=10, show_woe=False)
                    self.woe = woe.copy()
                    self.iv = iv.copy()                
                    iv_features = iv[iv['IV'] > self.iv_cutoff]['Variable'].to_list()        
                    print(f"{len(iv_features)} features remaining out of {len(self.final_features)} after information value iteration")
                    self.iv_features = iv_features.copy()
                    self.final_features = iv_features.copy()        
            else:
                 print('information value iteration already executed if you want proceed pls assign class.iv_features=None')



    def logistic_iteration(self):
        """
        Perform feature selection using Logistic Regression with L1 regularization.

        This method applies Logistic Regression with L1 regularization to select important features
        from the dataset based on their coefficients. Features with non-zero coefficients are selected
        as they contribute to the logistic regression model.

        Attributes Modified:
        - logit_features (list): List of selected features after logistic iteration.
        - final_features (list): List of selected features after logistic iteration.

        Notes:
        - If `logit_features` attribute is already populated, indicating that the method has been
          executed previously, a message will be printed indicating the same.

        - If `final_features` attribute is None, the method will use all features except the
          target variable for feature selection. Otherwise, it will use the features specified
          in `final_features`.

        - The method scales the features using StandardScaler before applying logistic regression.

        - Logistic Regression with L1 regularization (Lasso) is employed to penalize and shrink
          coefficients, effectively performing feature selection by setting coefficients of
          unimportant features to zero.

        - After fitting the logistic regression model, features with non-zero coefficients
          are selected and stored in both `logit_features` and `final_features` attributes.

        - A message indicating the number of selected features out of total features is printed
          to provide feedback on the feature selection process.
        """
        if self.data is None:
            print('pls read data first')
        else:            
            if self.logit_features is None:
                if self.final_features is None:
                    scaler = StandardScaler()
                    X_train = self.data.drop([self.Target],axis=1).copy()
                    X_train_scaled = scaler.fit_transform(X_train)
                    log_reg = LogisticRegression(penalty='l1', solver='liblinear', random_state=42)
                    log_reg.fit(X_train_scaled, self.data[[self.Target]])
                    selected_features_indices = np.where(log_reg.coef_ != 0)[1]
                    logit_features = list(X_train[X_train.columns[selected_features_indices]].columns)               
                    print(f"{len(logit_features)} features remaining out of {self.data.shape[1]} after logistic iteration")
                    self.logit_features = logit_features.copy()
                    self.final_features = logit_features.copy()
                else:   
                    scaler = StandardScaler()
                    X_train = self.data[self.final_features].copy()
                    X_train_scaled = scaler.fit_transform(X_train)
                    log_reg = LogisticRegression(penalty='l1', solver='liblinear', random_state=42)
                    log_reg.fit(X_train_scaled,self.data[[self.Target]])
                    selected_features_indices = np.where(log_reg.coef_ != 0)[1]
                    logit_features = list(X_train[X_train.columns[selected_features_indices]].columns)


                    print(f"{len(logit_features)} features remaining out of {len(self.final_features)} after logistic iteration")
                    self.logit_features = logit_features.copy()
                    self.final_features = logit_features.copy()        
            else:
                 print('logistic iteration already executed if you want proceed pls assign class.logit_features=None')


    def multicollinearity_iteration(self,ml_cutoff = 100000):
        """
        Perform feature selection to mitigate multicollinearity issues.

        This method addresses multicollinearity among features by iteratively removing
        features with high Variance Inflation Factor (VIF) until the maximum VIF value
        falls below a specified cutoff threshold.

        Parameters:
        - ml_cutoff (float, optional): The cutoff threshold for maximum VIF value.
          Features with VIF above this threshold will be considered collinear and removed.
          Default is 100000.

        Attributes Modified:
        - non_ml_features (list): List of selected features after multicollinearity iteration.
        - final_features (list): List of selected features after multicollinearity iteration.

        Notes:
        - If `non_ml_features` attribute is already populated, indicating that the method has been
          executed previously, a message will be printed indicating the same.

        - If `final_features` attribute is None, the method will use all features except the
          target variable for feature selection. Otherwise, it will use the features specified
          in `final_features`.

        - The method employs StandardScaler to scale the features before calculating VIF.

        - The VIF is computed for each feature using Ordinary Least Squares (OLS) regression.
          Features with VIF above the cutoff threshold are identified and removed iteratively
          until no feature has a VIF value exceeding the threshold.

        - After feature selection, the remaining non-collinear features are stored in both
          `non_ml_features` and `final_features` attributes.

        - A message indicating the number of selected features out of total features is printed
          to provide feedback on the feature selection process.
        """
        if self.data is None:
            print('pls read data first')
        else:            
            if self.non_ml_features is None:
                self.ml_cutoff = ml_cutoff
                if self.final_features is None:
                    scaler = StandardScaler()
                    X_scaled_ml = scaler.fit_transform(self.data.drop([self.Target],axis=1))
                    X_scaled_ml = pd.DataFrame(X_scaled_ml, columns=list(self.data.drop([self.Target],axis=1).columns))
                    vif_data = pd.DataFrame()
                    vif_data["Variable"] = ['var']
                    vif_data["VIF"] = [1000000000000]
                    def compute_vif(col):
                        temp = pd.DataFrame({'Variable': col, 'VIF': 1 / (1 - sm.OLS(X_scaled_ml[col].values, sm.add_constant(X_scaled_ml.drop(col, axis=1))).fit().rsquared_adj)}, index=[0])                            
                        return temp
                    while vif_data["VIF"].max() > self.ml_cutoff: 
                        vif_data = pd.concat([compute_vif(col) for col in list(X_scaled_ml.columns)], axis=0).reset_index(drop=True)
                        max_vif_variable = vif_data[vif_data['VIF'] == vif_data['VIF'].max()]['Variable'].to_list()[0]
                        if vif_data["VIF"].max() > self.ml_cutoff:
                            X_scaled_ml = X_scaled_ml.drop(columns=max_vif_variable)
                            print(f" {max_vif_variable} removed with vif {vif_data['VIF'].max()}")
                    non_ml_features = list(X_scaled_ml.columns) 

                    print(f"{len(non_ml_features)} features remaining out of {self.data.shape[1]-1} after multicollinearity iteration")
                    self.non_ml_features = non_ml_features.copy()
                    self.final_features = non_ml_features.copy()
                else:   
                    scaler = StandardScaler()
                    X_scaled_ml = scaler.fit_transform(self.data[self.final_features])
                    X_scaled_ml = pd.DataFrame(X_scaled_ml, columns=self.final_features)
                    vif_data = pd.DataFrame()
                    vif_data["Variable"] = ['var']
                    vif_data["VIF"] = [1000000000000]
                    def compute_vif(col):
                        temp = pd.DataFrame({'Variable': col, 'VIF': 1 / (1 - sm.OLS(X_scaled_ml[col].values, sm.add_constant(X_scaled_ml.drop(col, axis=1))).fit().rsquared_adj)}, index=[0])                            
                        return temp
                    while vif_data["VIF"].max() > self.ml_cutoff: 
                        vif_data = pd.concat([compute_vif(col) for col in list(X_scaled_ml.columns)], axis=0).reset_index(drop=True)
                        max_vif_variable = vif_data[vif_data['VIF'] == vif_data['VIF'].max()]['Variable'].to_list()[0]
                        if vif_data["VIF"].max() > self.ml_cutoff:
                            X_scaled_ml = X_scaled_ml.drop(columns=max_vif_variable)
                            print(f" {max_vif_variable} removed with vif {vif_data['VIF'].max()}")
                    non_ml_features = list(X_scaled_ml.columns) 

                    print(f"{len(non_ml_features)} features remaining out of {len(self.final_features)} after multicollinearity iteration")
                    self.non_ml_features = non_ml_features.copy()
                    self.final_features = non_ml_features.copy()        
            else:
                 print('multicollinearity iteration already executed if you want proceed pls assign class.non_ml_features=None')

    def random_forest_iteration(self, rf_cutoff=0.80):
        """
        Perform feature selection using Random Forest algorithm.

        This method applies Random Forest algorithm to select important features from the dataset
        based on their importance scores. It iterates through features sorted by importance,
        selecting features whose cumulative importance exceeds a specified cutoff threshold.

        Parameters:
        - rf_cutoff (float, optional): The cutoff threshold for cumulative feature importance.
          Features with cumulative importance above this threshold will be selected. Default is 0.80.

        Attributes Modified:
        - rf_features (list): List of selected features after Random Forest iteration.
        - final_features (list): List of selected features after Random Forest iteration.
        - rf_feature_importance_df (DataFrame): DataFrame containing feature importances
          obtained from Random Forest model.

        Notes:
        - If `rf_features` attribute is already populated, indicating that the method has been
          executed previously, a message will be printed indicating the same.

        - If `final_features` attribute is None, the method will use all features except the
          target variable for feature selection. Otherwise, it will use the features specified
          in `final_features`.

        - The Random Forest model is trained with the following parameters:
          - `n_estimators`: Number of trees in the forest, calculated as one-fourth of the
            number of features in the dataset.
          - `min_samples_leaf`: Minimum number of samples required to be at a leaf node,
            calculated as 5% of the total number of samples divided by one-fourth of the
            number of features.
          - `max_samples`: Number of samples to draw from the dataset to train each tree,
            set to 50% of the dataset size.
          - `max_depth`: Maximum depth of the trees in the forest, set to 3.

        - After training the model, feature importances are calculated and stored in
          `rf_feature_importance_df` DataFrame, which is sorted in descending order based
          on feature importance scores.

        - Features are iterated through based on their importance scores, starting from
          the most important features. Features are selected until the cumulative importance
          exceeds the specified cutoff threshold (`rf_cutoff`). The selected features are then
          stored in both `rf_features` and `final_features` attributes.

        - A message indicating the number of selected features out of total features is printed
          to provide feedback on the feature selection process.
        """
        if self.data is None:
            print('pls read data first')
        else:            
            if self.rf_features is None:
                self.rf_cutoff = rf_cutoff
                if self.final_features is None:
                    X_train = self.data.drop([self.Target], axis=1).copy()
                    y_train = self.data[[self.Target]]
                    model = RandomForestClassifier(
                        n_estimators=int(X_train.shape[1] / 4),
                        min_samples_leaf=max(int((X_train.shape[0] / int(X_train.shape[1] / 4)) * 0.05), 50),
                        max_samples=0.5, max_depth=3
                    )
                    model.fit(X_train, y_train)
                    feature_importance_df = pd.DataFrame({
                        'Feature': X_train.columns,
                        'Importance': model.feature_importances_
                    })
                    feature_importance_df = feature_importance_df.sort_values(['Importance'], ascending=False)
                    self.rf_feature_importance_df = feature_importance_df.copy()
                    for i in feature_importance_df['Importance']:
                        if feature_importance_df[feature_importance_df['Importance'] >= i]['Importance'].sum() >= self.rf_cutoff:
                            rf_features = feature_importance_df[feature_importance_df['Importance'] >= i]['Feature'].to_list()
                            break

                    print(f"{len(rf_features)} features remaining out of {self.data.shape[1]-1} after random_forest_iteration")
                    self.rf_features = rf_features.copy()
                    self.final_features = rf_features.copy()
                else:
                    X_train = self.data[self.final_features].copy()
                    y_train = self.data[[self.Target]]
                    model = RandomForestClassifier(
                        n_estimators=int(X_train.shape[1] / 4),
                        min_samples_leaf=max(int((X_train.shape[0] / int(X_train.shape[1] / 4)) * 0.05), 50),
                        max_samples=0.5, max_depth=3
                    )
                    model.fit(X_train, y_train)
                    feature_importance_df = pd.DataFrame({
                        'Feature': X_train.columns,
                        'Importance': model.feature_importances_
                    })
                    feature_importance_df = feature_importance_df.sort_values(['Importance'], ascending=False)
                    self.rf_feature_importance_df = feature_importance_df.copy()
                    for i in feature_importance_df['Importance']:
                        if feature_importance_df[feature_importance_df['Importance'] >= i]['Importance'].sum() >= self.rf_cutoff:
                            rf_features = feature_importance_df[feature_importance_df['Importance'] >= i]['Feature'].to_list()
                            break

                    print(f"{len(rf_features)} features remaining out of {len(self.final_features)} after random_forest_iteration")
                    self.rf_features = rf_features.copy()
                    self.final_features = rf_features.copy()
            else:
                print('random forest iteration already executed if you want proceed pls assign class.rf_features=None')

    def training_decision_tree(self, min_pop_per=0.05, max_pop_per=0.20, max_depth=3, test_size=0.2):
        
        """
        Train a decision tree model with specified parameters.

        This method trains a decision tree model using the specified parameters and selects the random state 
        that minimizes the 'bad difference' value, which is calculated based on the distribution of predicted 
        probabilities and the actual target values.

        Parameters:
            min_pop_per (float): Minimum population percentage for leaf nodes.
            max_pop_per (float): Maximum population percentage for leaf nodes.
            max_depth (int): Maximum depth of the decision tree.
            test_size (float): Size of the test dataset.

        Returns:
            None

        Preprocessing Steps:
        1. Split the dataset into train and test sets using different random states.
        2. Train a decision tree model for each split with specified parameters.
        3. Calculate predicted probabilities for the test set.
        4. Calculate population percentage and bad rate for each predicted probability group.
        5. Calculate the bad difference value based on population percentage and bad rate.
        6. Select the random state that minimizes the bad difference value.
        7. Train the decision tree model with the selected random state using the full train dataset.

        Note:
        - This method prints the selected random state.
        - It updates the `test_data`, `train_data`, and `model` attributes of the object.
        """
        # Save the current feature combination
        if self.data is None:
            print('pls read data first')
        else:    
            if self.final_features is None:
                self.final_features  = list(self.data.drop([self.Target],axis=1).columns).copy()
            current_combination = self.final_features

            # Initialize lists to store random state and bad difference values
            random_st = []
            bad_diff_value = []

            # Iterate over random states
            for i in range(1, 100):

                # Split data into train and test sets
                X_train, X_test, y_train, y_test = train_test_split(self.data[current_combination], 
                                                                    self.data[[self.Target]], 
                                                                    test_size=test_size, 
                                                                    random_state=i, 
                                                                    stratify=self.data[self.Target])

                # Create copies of the datasets
                original_dataset_train = pd.concat([pd.DataFrame(X_train, columns=X_train.columns),
                                                    pd.DataFrame(y_train, columns=[self.Target])], axis=1)
                original_dataset_test = pd.concat([pd.DataFrame(X_test, columns=X_test.columns),
                                                   pd.DataFrame(y_test, columns=[self.Target])], axis=1)

                # Create copies for manipulation
                X_t_test = original_dataset_test.copy()
                subset_data = original_dataset_train.copy()

                # Prepare data for model training
                X_t = subset_data.drop([self.Target], axis=1)
                y_t = subset_data[self.Target]

                # Train the decision tree model
                model = DecisionTreeClassifier(random_state=42, max_depth=max_depth,
                                               min_samples_leaf=max(50,int(round((subset_data.shape[0]) * min_pop_per, 0))))
                model.fit(X_t, y_t)

                # Calculate predicted probabilities
                X_t_test['predict_prob'] = model.predict_proba(X_t_test.drop([self.Target], axis=1))[:, 1]
                X_t_test['dummy'] = 1

                # Calculate population percentage and bad rate
                def custom_sum_product(group):
                    return pd.Series({'Pop%': group['dummy'].sum() / X_t_test.shape[0],
                                      'bad_rate': (group[self.Target].sum() / group['dummy'].sum())})

                X_t_test = X_t_test.groupby('predict_prob').apply(custom_sum_product).reset_index()

                # Calculate bad difference value
                if (X_t_test.reset_index()['Pop%'].max()<=max_pop_per)&(X_t_test.reset_index()['Pop%'].min()>=min_pop_per):
                    bad_diff = abs((X_t_test['predict_prob'] - X_t_test['bad_rate']) * X_t_test['Pop%']).sum()
                    bad_diff_value.append(bad_diff)
                else:
                    bad_diff_value.append(100)
                random_st.append(i)

            # Find the random state with the lowest bad difference value
            results = pd.DataFrame({'random_state': random_st, 'bad_diff': bad_diff_value})
            results = results[results['bad_diff'] == results['bad_diff'].min()]

            # Handle multiple best results
            if results.shape[0] > 1:
                ran_state = 42
                print('Please adjust min_max_pop split.')
            else:
                ran_state = results.reset_index()['random_state'].tolist()[0]
            print(f'current random state {ran_state}.')

            # Train the decision tree model with the selected random state
            X_train, X_test, y_train, y_test = train_test_split(self.data[current_combination], 
                                                                self.data[[self.Target]], 
                                                                test_size=test_size, 
                                                                random_state=ran_state, 
                                                                stratify=self.data[self.Target])

            # Create copies of the datasets
            original_dataset_train = pd.concat([pd.DataFrame(X_train, columns=X_train.columns),
                                                pd.DataFrame(y_train, columns=[self.Target])], axis=1)
            original_dataset_test = pd.concat([pd.DataFrame(X_test, columns=X_test.columns),
                                               pd.DataFrame(y_test, columns=[self.Target])], axis=1)

            # Prepare data for model training
            X_t_test = original_dataset_test.copy()
            subset_data = original_dataset_train.copy()

            X_t = subset_data.drop([self.Target], axis=1)
            y_t = subset_data[self.Target]

            # Update train and test datasets and save the trained model
            self.test_data = X_t_test.copy()
            self.train_data = subset_data.copy()
            model = DecisionTreeClassifier(random_state=42, max_depth=max_depth,
                                           min_samples_leaf=max(50,int(round((subset_data.shape[0]) * min_pop_per, 0))))
            model.fit(X_t, y_t)
            self.model = model




    def plot_current_tree(self, figure_size=(30, 25), fontsize=10):
        """
        Plot the current decision tree model.

        Parameters:
            figure_size (tuple): Size of the figure.
            fontsize (int): Font size of the plot.

        Returns:
            None
        """
        # Check if the model has been trained
        if self.model is None:
            print('Please train the model first.')
        else:
            # Plot the decision tree
            plt.figure(figsize=figure_size)
            plot_tree(self.model, 
                      feature_names=self.final_features, 
                      class_names=[str(c) for c in self.data[self.Target].unique()], 
                      filled=True, 
                      fontsize=fontsize, 
                      rounded=True, 
                      proportion=True)
            plt.show()
            
    def performance_current_tree(self):
        """
        Evaluate the performance of the current tree model using training and test data.

        Prints the population percentage and bad rate for different predicted probabilities.

        Returns:
            None
        """
        # Check if the model has been trained
        if self.model is None:
            print('Please train the model first.')
        else:
            # Performance evaluation on training data
            train_data = self.train_data.copy()
            train_data['predict_prob'] = self.model.predict_proba(train_data.drop([self.Target], axis=1))[:, 1]
            train_data['dummy'] = 1

            def custom_sum_product(group):
                return pd.Series({'Pop%': group['dummy'].sum() / train_data.shape[0],
                                  'bad_rate': (group[self.Target].sum() / group['dummy'].sum())})

            train_result = train_data.groupby('predict_prob').apply(custom_sum_product)
            print("Training Data:")
            print(train_result)

            # Performance evaluation on test data
            test_data = self.test_data.copy()
            test_data['predict_prob'] = self.model.predict_proba(test_data.drop([self.Target], axis=1))[:, 1]
            test_data['dummy'] = 1

            def custom_sum_product(group):
                return pd.Series({'Pop%': group['dummy'].sum() / test_data.shape[0],
                                  'bad_rate': (group[self.Target].sum() / group['dummy'].sum())})

            test_result = test_data.groupby('predict_prob').apply(custom_sum_product)
            print("\nTest Data:")
            print(test_result)
