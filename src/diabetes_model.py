# -*- coding: UTF-8 -*-
"""Import modules"""
from datetime import datetime
import numpy as np
import pandas as pd
from os import path
import statsmodels.api as sm
from io import BytesIO

class DiabetesModel:
    """
    Econometric models
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

        return "Glicose Econometric Model Class"
    
    def __repr__(self):
        """Default class 
        representation"""

        return "Glicose Econometric Model Class"


    def _basic_statistics(self) -> list:
        """calculates basic stats
        return matrix"""

        means = [self.data[column].mean().round(2) for column in self.data.columns]
        means.insert(0, "Média")

        stds = [self.data[column].std().round(2) for column in self.data.columns]
        stds.insert(0, "Desvio\nPadrão")

        result_matrix = [["statistic"] + list(self.data.columns),
                         means,
                         stds]

        return result_matrix


    def _plot_graphs(self) -> BytesIO:
        """Plot graphics"""

        img_idade_glicose = self.utils._render_graphics(
            self.data, 
            "Idade x Glicose", 
            ["idade", "glicose"]
        )

        img_pressao_imc = self.utils._render_graphics(
            self.data,
            "Pressão Arterial x IMC", 
            ["imc", "pressao_arterial"]
        )

        print("Rendered Graphics")
        
        return img_idade_glicose, img_pressao_imc
    

    def _build_simple_model(self, 
                            columns: list) -> list:
        """Build Simple Reg 
        Models"""

        try:
            data = self.data.fillna(0)

            x = np.array(data[columns[0]], dtype=float)
            y = np.array(data[columns[1]], dtype=float)

            x_sm = sm.add_constant(x)

            result = sm.OLS(y, x_sm).fit()

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

            result_matrix = [
                ["Estatística", "Constante", columns[0]],
                parameters,
                std_errors,
                p_values,
                conf_int_str
                ]

            return result_matrix
        
        except Exception as error:
            raise OSError(error) from error
        
        
    def _plot_reg_lines(self) -> BytesIO:
        """Plot graphics"""

        modelo_glicose = self._build_simple_model(["idade", "glicose"])

        predictions_glicose = modelo_glicose[1][1] + (modelo_glicose[1][2] * np.array(self.data["idade"]))

        reg_idade_glicose = self.utils._render_graphics(
            self.data, "Idade x Glicose", 
            ["idade", "glicose"],
            regplot=True,
            predictions=predictions_glicose
        )

        modelo_pressao = self._build_simple_model(["imc", "pressao_arterial"])

        predictions_pressao = modelo_pressao[1][1] + (modelo_pressao[1][2] * np.array(self.data["imc"]))

        reg_pressao_imc = self.utils._render_graphics(
            self.data, "Pressão Arterial x IMC", 
            ["imc", "pressao_arterial"],
            regplot=True,
            predictions=predictions_pressao
        )

        print("Rendered Graphics")
        
        return reg_idade_glicose, reg_pressao_imc
    

    def _build_mult_model(self, target_col: str,
                           indep_cols: list) -> list:
        """Build Mult Reg
        Model"""

        try:

            data = (
                self.data
                .assign(
                    d_gravidez = lambda x: np.where(x["n_gravidez"] > 1, 1, 0)
                    )
                    .fillna(0)
            )

            indep_cols = indep_cols + ["d_gravidez"]

            x = np.array(data[indep_cols], dtype=float)
            y = np.array(data[target_col], dtype=float)

            x_sm = sm.add_constant(x)

            result = sm.OLS(y, x_sm).fit()

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