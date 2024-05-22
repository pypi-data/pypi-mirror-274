from .base import BaseMitigationStrategy
from ..processors.base import BaseProcessor

import pandas as pd

class BalanceOutput(BaseMitigationStrategy) :
    """Test

    Args:
        BaseMitigationStrategy (_type_): _description_
    """
    def __init__(self, sampler: BaseProcessor) :
        super().__init__(sampler)
    
    def balance(self, dataset: pd.DataFrame, target: pd.DataFrame = None, protected_attributes: list = None, 
                       cont_columns: list = None, cat_columns: list = None) :
        
        df, protected_attribute = self._get_dataframe_and_protected_attribute(dataset, protected_attributes)
        
        X_processed, y_processed = self.sampler._process(df, target, cont_columns, cat_columns)
        X_resampled, y_resampled = self.sampler.fit_resample(X_processed, y_processed)
        X_final, y_final = self.sampler._unprocess(X_resampled, y_resampled)
        
        X_final = self._get_final_dataframe(X_final, protected_attributes, protected_attribute)
        
        return X_final, y_final     


class BalanceAttributes(BaseMitigationStrategy) :
    def __init__(self, sampler: BaseProcessor) :
        super().__init__(sampler)

    def balance(self, dataset: pd.DataFrame, target: pd.DataFrame = None, protected_attributes: list = None, 
                cont_columns: list = None, cat_columns: list = None) :
        
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
    def __init__(self, sampler: BaseProcessor) :
        super().__init__(sampler)
    
    def balance(self, dataset: pd.DataFrame, target: pd.DataFrame = None, protected_attributes: list = None, 
                cont_columns: list = None, cat_columns: list = None) :

        df, protected_attribute = self._get_dataframe_and_protected_attribute(dataset, protected_attributes)
        
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
      