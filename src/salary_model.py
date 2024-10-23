# -*- coding: UTF-8 -*-
"""Import modules"""
from os import path

import numpy as np
import pandas as pd
import statsmodels.api as sm


class SalaryModel:
    """
    Econometric model
    class
    """

    def __init__(self, data_path: str):
        """Initialize instance"""

        # import local module
        from src.static import StaticVariables
        from src.utils import Utils

        self.static = StaticVariables()
        self.utils = Utils()
        self.data = pd.read_csv(
            path.join(self.static.data_dir, data_path)
        )

    
    def __str__(self):
        """String class 
        representation"""

        return "Salary Econometric Model Class"
    

    def __repr__(self):
        """Default class 
        representation"""

        return "Salary Econometric Model Class"
    

    def _build_mult_model(self,indep_cols: list) -> list:
        """Build Mult Reg
        Model"""

        # func for question 1

        try:

            # create log_salario column
            data = (
                self.data
                .assign(
                    log_salario = lambda x: x["salario"].apply(lambda x: np.log(x))
                    )
                    .fillna(0)
            )

            # define vars vectors
            x = np.array(data[indep_cols], dtype=float)
            y = np.array(data["log_salario"], dtype=float)

            # set independent variable
            x_sm = sm.add_constant(x)

            # run model
            result = sm.OLS(y, x_sm).fit()

            # build results matrix
            parameters = result.params.round(3).tolist()
            parameters.insert(0, "Parâmetros")

            std_errors = result.bse.round(3).tolist()
            std_errors.insert(0, "Erro Padrão")

            p_values = result.pvalues.tolist()
            p_values = [f"{p:.3e}" for p in p_values]
            p_values.insert(0, "P Values")

            conf_int = result.conf_int().round(3).tolist()
            conf_int_str = [f"[{ci[0]}, {ci[1]}]" for ci in conf_int]
            conf_int_str.insert(0, "Intervalo de Confiança")

            header = ["Constante"] + indep_cols

            result_matrix = [
                ["Estatística", *header],
                parameters,
                std_errors,
                p_values,
                conf_int_str
                ]

            return result_matrix
        
        except Exception as error:
            raise OSError(error) from error


    def _calculate_mean(self) -> list:
        """calculates salary means
        return matrix"""

        # func for question 3
        
        # agregate dataset by gender
        data_salary = (
            self.data
            .groupby("homem")
            ["salario"]
            .agg("mean")
        )

        # build result matrix
        result_matrix = [["Estatística", "Mulher", "Homem"],
                         ["Média Salarial ($)", float(data_salary[0].round(2)), 
                          float(data_salary[1].round(2))]]

        return result_matrix