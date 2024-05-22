from imblearn.over_sampling import RandomOverSampler, SMOTENC
from imblearn.under_sampling import RandomUnderSampler
from .base import BaseProcessor, Processor

class RandomOverSamplerProcessor(RandomOverSampler, BaseProcessor) :     
    def __init__(self) :
        super().__init__()
    
    def _process(self,X, y, cont_columns, cat_columns) :
        return X, y

    def _unprocess(self,X, y) :
        return X, y

class RandomUnderSamplerProcessor(RandomUnderSampler, BaseProcessor) :
    def __init__(self) :
        super().__init__()
    
    def _process(self,X, y, cont_columns, cat_columns) :
        return X, y

    def _unprocess(self,X, y) :
        return X, y

class SMOTENCProcessor(SMOTENC, BaseProcessor) :
    def __init__(self) :
        super().__init__(categorical_features=[])
        
    def _process(self,X, y, cont_columns, cat_columns) :
        self.processor = Processor()    
        processed_X = self.processor.process(X, scale_cols=cont_columns, encode_cols=cat_columns)
        cat_columns_ids = [processed_X.columns.get_loc(col_name) for col_name in cat_columns]
        self.categorical_features = cat_columns_ids
        return processed_X, y

    def _unprocess(self,X, y) :
        unprocessed_X = self.processor.unprocess(X)
        return unprocessed_X, y
        
