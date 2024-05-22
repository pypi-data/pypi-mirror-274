from .base import BaseMitigationStrategy
from ..processors.base import BaseProcessor

import pandas as pd

class BalanceOutput(BaseMitigationStrategy) :
    """
    Balances the outputs of the dataset with no regards to the protected attributes.

    Parameters
    ----------
    sampler : processors.BaseProcessor
        Defines the sampling method to balance the output. Object must inherit from the processors.BaseProcessor class.
        Current available sampling methods are RandomOverSamplerProcessor, SMOTENCProcessor and RandomUnderSamplingProcessor.
        
    Attributes
    ---------- 
    None
    """
    
    def __init__(self, sampler: BaseProcessor) :
        super().__init__(sampler)
    
    def balance(self, dataset: pd.DataFrame, target: pd.DataFrame, protected_attributes: list = None, 
                       cont_columns: list = None, cat_columns: list = None) :
        """Balances the dataset.

        Parameters
        ----------
        dataset : pd.DataFrame 
            The dataset to balance, without the target column.
        target : pd.Series 
            The target column. 
        protected_attributes : list, optional
            The protected attributes. Not used in this function but kept for API consistency. Defaults to None.
        cont_columns : list, optional
            The names of the continuous columns of the dataset. Defaults to None.
        cat_columns : list, optional 
            The names of the categorical columns of the dataset. Defaults to None.

        Returns
        ----------
        [pd.DataFrame, pd.Series]: The resampled dataset and the resampled output.
        """
        
        df, protected_attribute = self._get_dataframe_and_protected_attribute(dataset, protected_attributes)
        
        if protected_attribute not in cat_columns :
            cat_columns.append(protected_attribute)
        
        X_processed, y_processed = self.sampler._process(df, target, cont_columns, cat_columns)
        X_resampled, y_resampled = self.sampler.fit_resample(X_processed, y_processed)
        X_final, y_final = self.sampler._unprocess(X_resampled, y_resampled)
        
        X_final = self._get_final_dataframe(X_final, protected_attributes, protected_attribute)
        
        return X_final, y_final     


class BalanceAttributes(BaseMitigationStrategy) :
    """
    Balances the protected attributes given to the balance() method with no regards to the output.

    Parameters
    ----------
    sampler : processors.BaseProcessor
        Defines the sampling method to balance the output. Object must inherit from the processors.BaseProcessor class.
        Current available sampling methods are RandomOverSamplerProcessor, SMOTENCProcessor and RandomUnderSamplingProcessor.
        
    Attributes
    ---------- 
    None
    """
    def __init__(self, sampler: BaseProcessor) :
        super().__init__(sampler)

    def balance(self, dataset: pd.DataFrame, target: pd.DataFrame, protected_attributes: list, 
                cont_columns: list = None, cat_columns: list = None) :
        """Balances the dataset.

        Parameters
        ----------
        dataset : pd.DataFrame 
            The dataset to balance, without the target column.
        target : pd.Series 
            The target column. 
        protected_attributes : list
            The protected attributes to balance.
        cont_columns : list, optional
            The names of the continuous columns of the dataset. Defaults to None.
        cat_columns : list, optional 
            The names of the categorical columns of the dataset. Defaults to None.

        Returns
        ----------
        [pd.DataFrame, pd.Series]: The resampled dataset and the resampled output.
        """
        
        df, protected_attribute = self._get_dataframe_and_protected_attribute(dataset, protected_attributes)
        

        X_processed, y_processed = self.sampler._process(df, target, cont_columns, cat_columns)
        
        protected_attribute_column = X_processed[protected_attribute]
        X_processed = X_processed.drop(columns=[protected_attribute])
        X_processed.loc[:,"target"] = y_processed
        new_cat_columns = [column for column in cat_columns if column != protected_attribute] + ["target"]
        cat_columns_ids = [X_processed.columns.get_loc(col_name) for col_name in new_cat_columns]
        self.sampler.set_categorical_features(cat_columns_ids)

        X_resampled, protected_attribute_resampled = self.sampler.fit_resample(X_processed, protected_attribute_column)
        X_resampled.loc[:, protected_attribute] = protected_attribute_resampled
        y_resampled = X_resampled["target"]
        X_resampled = X_resampled.drop(columns=["target"])
        
        X_final, y_final = self.sampler._unprocess(X_resampled, y_resampled)
        X_final = self._get_final_dataframe(X_final, protected_attributes, protected_attribute)

        return X_final, y_final
        
class BalanceOutputForAttributes(BaseMitigationStrategy) :
    """
    Balances the outputs of the protected attributes given to the balance().

    Parameters
    ----------
    sampler : processors.BaseProcessor
        Defines the sampling method to balance the output. Object must inherit from the processors.BaseProcessor class.
        Current available sampling methods are RandomOverSamplerProcessor, SMOTENCProcessor and RandomUnderSamplingProcessor.
        
    Attributes
    ---------- 
    None
    """
    def __init__(self, sampler: BaseProcessor) :
        super().__init__(sampler)
    
    def balance(self, dataset: pd.DataFrame, target: pd.DataFrame, protected_attributes: list, 
                cont_columns: list = None, cat_columns: list = None) :
        """Balances the dataset.

        Parameters
        ----------
        dataset : pd.DataFrame 
            The dataset to balance, without the target column.
        target : pd.Series 
            The target column. 
        protected_attributes : list, optional
            The protected attributes for which to balance the output.
        cont_columns : list, optional
            The names of the continuous columns of the dataset. Defaults to None.
        cat_columns : list, optional 
            The names of the categorical columns of the dataset. Defaults to None.

        Returns
        ----------
        [pd.DataFrame, pd.Series]: The resampled dataset and the resampled output.
        """

        df, protected_attribute = self._get_dataframe_and_protected_attribute(dataset, protected_attributes)
        
        if protected_attribute not in cat_columns :
            cat_columns.append(protected_attribute)
        
        classes = list(df[protected_attribute].unique())
        highest_r, class_with_highest_r = self._highest_ratio(df, target, classes, protected_attribute)
        self.sampler.sampling_strategy = highest_r
        X_final = pd.DataFrame(columns = df.columns)
        y_final = pd.Series()
        for class_ in classes :
            
                # keep only the rows with given class
            class_df = df[df[protected_attribute] == class_]
            class_target = target[df[protected_attribute] == class_]
            
            if class_ != class_with_highest_r :  
                # resample the target for this class
                if len(class_target.unique()) > 1 :
                    X_processed, y_processed = self.sampler._process(class_df, class_target, cont_columns, cat_columns)
                    X_resampled, y_resampled = self.sampler.fit_resample(X_processed, y_processed)
                    X_class_final, y_class_final = self.sampler._unprocess(X_resampled, y_resampled)
                        
                else :
                    X_class_final = class_df
                    y_class_final = class_target
            
                # append the resampled class in final dfs
                X_final = pd.concat([X_final, X_class_final], ignore_index=True)
                y_final = pd.concat([y_final, y_class_final])
            
            else :
                X_final = pd.concat([X_final, class_df], ignore_index=True)
                y_final = pd.concat([y_final, class_target])
                
        
        
        X_final = self._get_final_dataframe(X_final, protected_attributes, protected_attribute)

        return X_final, y_final
      