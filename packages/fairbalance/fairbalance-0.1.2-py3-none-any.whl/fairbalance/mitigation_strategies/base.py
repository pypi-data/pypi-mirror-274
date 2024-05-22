
import functools
import pandas as pd

class BaseMitigationStrategy :
    def __init__(self, sampler) :
        self.sampler = sampler
    
    def _get_dataframe_and_protected_attribute(self, dataset, protected_attributes) :
        df = dataset.copy()
        if len(protected_attributes) > 1 :
            return self._make_super_protected(df, protected_attributes)
        return df, protected_attributes[0]
    
    def _get_final_dataframe(self, dataset, protected_attributes, protected_attribute) :
        if len(protected_attributes) > 1 :
            dataset = dataset.drop(columns = [protected_attribute])
        return dataset
    
    def _make_super_protected(self, dataset: pd.DataFrame, protected_attributes: list) :
        """
        Make a super protected attribute that is the combination of all given protected attributes called "protected_superclass"

        Args:
            dataset (pd.DataFrame): dataset to mitigate, that includes the target column.
            protected_attributes (list): protected attributes to combine
            
        Returns:
            ([pd.DataFrame, str]): the transformed dataset and the name "super protected" column
        """

        df = dataset.copy()
        superprotected_column = functools.reduce(lambda a, b : a + "_" + b, protected_attributes)
        df[superprotected_column] = ""
        for protected_attribute in protected_attributes :

            df[superprotected_column] += df[protected_attribute].apply(str)  + "_"
                       
        df[superprotected_column] = df[superprotected_column].apply(lambda x : x[:-1])
        
        
        return df, superprotected_column

    def _highest_ratio(self, dataset: pd.DataFrame, target: pd.DataFrame, classes: dict, protected_attribute: str) :
            """
            Give the highest ratio of positive output on negative output of all the classes of the protected attribute. Necessary for balance_output_for_attribute.

            Args:
                dataset (pd.DataFrame): dataset to mitigate, that includes the target column.
                target (str): the target column name
                classes (dict): the classes of the protected attribute
                protected_attribute (str): the protected attribute to calculate the highest ratio for.

            Returns:
                ([float, str]): the highest ratio and the associated class
            """
            
            r_max = 0
            c_max = classes[0]
            dataset.loc[:, "target"] = target
            for c in classes :
                r = dataset[dataset[protected_attribute] == c]["target"].value_counts()[1]/dataset[dataset[protected_attribute] == c]["target"].value_counts()[0]
                if r > 1 :
                    r = 1/r
                if r > r_max :
                    r_max = r
                    c_max = c
            return r_max, c_max
