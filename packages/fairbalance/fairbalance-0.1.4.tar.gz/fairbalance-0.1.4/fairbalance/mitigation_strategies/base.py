
import functools
import pandas as pd

class BaseMitigationStrategy :
    """
    Base class for the mitigation strategies.
    
    Warning: This class should not be used directly. Use the derive classes
    instead.
    """
    def __init__(self, sampler) :
        self.sampler = sampler
    
    def _get_dataframe_and_protected_attribute(self, dataset: pd.DataFrame, protected_attributes = None) :
        """Returns the final dataframe and protected attribute. Used to make the "super attribute" if needed.
        If not needed, returns the original dataset and the single protected attribute.

        Parameters
        ----------
        dataset : pd.DataFrame 
            The dataset to work on.
        protected_attributes : list, optional 
            If it contains only one attribute, the dataset and the attribute are returned.
            If it contains more, makes a composite attribute first, then returns the dataset 
            and the composite attribute name. Defaults to None.

        Returns
        ----------
            [pd.DataFrame, str]: The final dataset and the protected attribute to work with.
        """
        df = dataset.copy()
        if protected_attributes and len(protected_attributes) > 1 :
            return self._make_super_protected(df, protected_attributes)
        return df, protected_attributes[0]
    
    def _get_final_dataframe(self, dataset, protected_attributes = None, protected_attribute = None) :
        """Returns the final dataframe after all processes are done.

        Parameters
        ----------
        dataset : pd.DataFrame 
            The dataset to work on.
        protected_attributes : list, optional 
            The list of protected attributes. Default to Nonz
        protected_attribute : str, optional 
            The name of the protected attribute used in the process. Defaults to None.

        Returns
        ----------
        [pd.DataFrame] : The processed final dataset.
        """
        if protected_attributes and len(protected_attributes) > 1 :
            dataset = dataset.drop(columns = [protected_attribute])
        return dataset
    
    def _make_super_protected(self, dataset: pd.DataFrame, protected_attributes: list) :
        """Make a super protected attribute that is the combination of all given protected attributes called "protected_superclass"

        Parameters
        ----------
        dataset : pd.DataFrame
            dataset to mitigate. It can include the target column but it is not necessary.
        protected_attributes : list 
            The list of protected attributes to combine into a single "super attribute".
            
        Returns
        ----------
        [pd.DataFrame, str] : the transformed dataset and the name "super protected" column
        """

        df = dataset.copy()
        superprotected_column = functools.reduce(lambda a, b : a + "_" + b, protected_attributes)
        df[superprotected_column] = ""
        for protected_attribute in protected_attributes :

            df[superprotected_column] += df[protected_attribute].apply(str)  + "_"
                       
        df[superprotected_column] = df[superprotected_column].apply(lambda x : x[:-1])
        
        
        return df, superprotected_column

    def _highest_ratio(self, dataset: pd.DataFrame, target: pd.DataFrame, classes: dict, protected_attribute: str) :
            """Give the highest ratio of positive output on negative output of all the classes of the protected attribute. 
            Necessary for balance_output_for_attribute.

            Parameters
            ----------
            dataset : pd.DataFrame 
                dataset to mitigate that does not include the target column.
            target : pd.Series
                the target column.
            classes : dict
                the classes of the given protected attribute
            protected_attribute : str
                the protected attribute for which to calculate the highest ratio of positive output.

            Returns
            ----------
            [float, str] : the highest ratio and the associated class
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
