from sys import prefix
import pandas as pd
from sklearn.calibration import LabelEncoder
from sklearn.preprocessing import MinMaxScaler




class Processor :
    """Dataset processor to dummify, encode and scale columns and adapt it to learning or mitigation.
    A Processor object shouldn't be used to process different datasets. If you need to process two different datasets, 
    it is good practice to use two different processors.
    
    Parameters
    ----------
    prefix_sex : str, optional 
        The prefix separator for dummification and undummification. It shouldn't be in any columns name of the dataset. Default to "~". 
    """

    def __init__(self, prefix_sep: str = "~") :
        self.prefix_sep = prefix_sep
        self.scalers = {}
        self.label_encoders = {}
        self.types = {}
    
    def _get_columns_types(self, dataset: pd.DataFrame) :
        self.types = dataset.dtypes
    
    def _dummify(self, dataset: pd.DataFrame, columns: list) :
        """Dummify the given columns using the prefix separator defined when initializing the Processor object.
        For example, a column "Race" with values "Male" and "Female" and prefix_sep="~" will become two columns 
        "Race~Male" and "Race~Female" with values 1 and 0.
        
        Parameters
        ----------
        dataset : pd.Dataframe 
            The dataset to transform
        columns : list 
            The columns to dummify
        
        Returns 
        ----------
        [pd.DataFrame] : The dummified dataset  
        """
        for column in columns :
            assert column in dataset.columns, f"feature {column} not in the dataset"
            assert self.prefix_sep not in column, f"""'{self.prefix_sep}' is the prefix separator for the dummifying process, but is in the column name {column}""" 
        
        return pd.get_dummies(data = dataset, columns=columns, prefix_sep=self.prefix_sep, dtype='int')
    
    def _encode(self, dataset: pd.DataFrame, columns: list) :
        """Encode the given columns.
        Encode the different labels of a column to give them Int values. for example, a column "Race" with values 
        "Male" and "Female" would be transformed into a column "Race" with values 1 and 2 where 1 encodes "Male" and 
        2 encodes "Female".
        
        Parameters
        ----------
        dataset : pd.Dataframe
            The dataset to transform
        columns : list
            The columns to dummify
        
        Returns 
        ----------
        [pd.DataFrame] : The encoded dataset  
        """
        for feature in columns :
            assert feature in dataset.columns, f"feature {feature} not in the dataset"
            le = LabelEncoder()
            dataset[feature] = le.fit_transform(dataset[feature])
            self.label_encoders[feature] = le
       
        return dataset
            
    def _scale(self, dataset: pd.DataFrame, columns: list) :
        """
        Scale the given columns.
        Scales the columns using the skLearn StandardScaler.
        
        Parameters
        ----------
        dataset : pd.Dataframe
            The dataset to transform
        columns : list 
            The columns to dummify
        
        Returns
        ----------
        [pd.DataFrame] : The scaled dataset  
        """
        for feature in columns :
            assert feature in dataset.columns, f"feature {feature} not in the dataset"
            scaler = MinMaxScaler()
            dataset[feature] = scaler.fit_transform(dataset[feature].values.reshape(-1, 1))
            self.scalers[feature] = scaler
        
        return dataset
        
    def process(self, dataset: pd.DataFrame, dummify_cols: list = [], 
                scale_cols: list = [], encode_cols: list = []) :
        """
        Process the datasets by dummifying, scaling and encoding the necessary columns.

        Parameters
        ----------
        dataset : pd.DataFrame 
            The dataset to transform.
        dummify_cols : list, optional 
            The columns to dummifying. Defaults to [].
        scale_cols : list, optional
            he columns to scale. Defaults to [].
        encode_cols : list, optional 
            The columns to encode. Defaults to [].

        Returns
        ----------
        [pd.DataFrame] : The transformed dataset.
        """
        df = dataset.copy()
        self._get_columns_types(df) 

        self.dummify_cols = dummify_cols
        self.scale_cols = scale_cols
        self.encode_cols = encode_cols
        
        #stardard normalization for columns to scale 
        if scale_cols :
            df = self._scale(df, scale_cols)
                
        #one-hot encoding for columns to dummify
        if dummify_cols :
            df = self._dummify(df, dummify_cols)
        
        #label encoding for columns to encode
        if encode_cols :
            df = self._encode(df, encode_cols)
    
        return df
    
    
    def _undummify(self, dataset: pd.DataFrame) :
        """Undummify the columns previously dummified.

        Parameters
        ----------
        dataset : pd.DataFrame 
            The dataset to transform

        Returns:
        ----------
        [pd.dataFrame] : The transformed dataset
        """
        undummified = self._undummify_df(dataset)
        for column in self.dummify_cols :
            undummified[column] = undummified[column].astype(self.types[column])
        return  undummified
    
    def _unencode(self, dataset: pd.DataFrame) :
        """Unencode the columns previously encoded.

        Parameters
        ----------
        dataset : pd.DataFrame 
            The dataset to transform

        Returns
        ----------
        [pd.dataFrame] : The transformed dataset
        """
        for feature in self.encode_cols :
            le = self.label_encoders[feature]
            dataset[feature] = le.inverse_transform(dataset[feature])
        return dataset
    
    def _unscale(self, dataset: pd.DataFrame) :
        """Unscale the columns previously scaled.

        Parameters
        ----------
        dataset : pd.DataFrame 
            The dataset to transform

        Returns
        ----------
        [pd.dataFrame] : The transformed dataset
        """
        for feature in self.scale_cols :
            scaler = self.scalers[feature]
            dataset[feature] = scaler.inverse_transform(dataset[[feature]])
        return dataset
    
    def unprocess(self, dataset: pd.DataFrame) :
        """Unprocess all the process made when Processor.process was called.

        Parameters
        ----------
        dataset : pd.DataFrame 
            The dataset to transform.

        Returns
        ----------
        [pd.dataFrame] : The transformed dataset
        """
        
        df = dataset.copy()
        
        #remove dummies
        if self.dummify_cols :
            df = self._undummify(df)
        
        #remove encoding
        if self.encode_cols :
            df = self._unencode(df)
        
        #remove scaling
        if self.scale_cols :
            df = self._unscale(df)
            
        return df



class BaseProcessor(Processor) :
    """Dataset processor to dummify, encode and scale columns and adapt it to learning or mitigation.
    A Processor object shouldn't be used to process different datasets. If you need to process two different datasets, 
    it is good practice to use two different processors.
    
    Parameters
    ----------
    prefix_sex : str, optional 
        The prefix separator for dummification and undummification. It shouldn't be in any columns name of the dataset. Default to "~". 
    """
    def __init__(self, prefix_sep: str = "~") :
        
        super().__init__(prefix_sep=prefix_sep)
        
    
    def _process(self, X, y, cont_columns, cat_columns) :
        pass
    
    def _unprocess(self, X, y) :
        pass
    
    def set_categorical_features(self, cat_features) :
        self.categorical_features = cat_features
        
