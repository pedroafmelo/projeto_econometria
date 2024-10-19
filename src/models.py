# -*- coding: UTF-8 -*-
"""Import modules"""
from datetime import datetime
import numpy as np
import pandas as pd
from os import path


class Models:
    """
    Econometric models
    class
    """

    def __init__(self, data_path: str):
        """Initialize instance"""

        # import local module
        from src.static import StaticVariables
        from src.utils import utils

        self.static = StaticVariables()
        self.data = pd.read_csv(
            path.join(self.static.data_dir, data_path)
        )


    def basic_statistics(self) -> list:
        """calculates basic stats
        return matrix"""

        means = [self.data[column].mean() for column in self.data.columns]
        stds = [self.data[column].std() for column in self.data.columns]

        result_matrix = [list(self.data.columns),
                         means.insert(0, "Média"),
                         stds.insert(0, "Desvio\nPadrão")]

        return result_matrix


    def calculate_parameters(self):
        """Calculates model parameters"""
        
        
        return