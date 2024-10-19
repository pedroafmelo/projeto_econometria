# -*- coding: UTF-8 -*-
"""Import modules"""
import matplotlib.pyplot as plt
import seaborn as sns
import io
from os import path
from pandas import DataFrame


class Utils:
    """ Utilities class """

    def __init__(self):
        """ Initialize instance """

        # import local modules
        from src.static import StaticVariables

        self.static = StaticVariables()

    
    def _render_latex_img(self, equation: str, quality = 300):
        """Render latex
        equation as img"""

        fig, ax = plt.subplots()

        ax.text(0.5, 0.5, f"${equation}$", fontsize=20,
                ha="center", va="center")
        ax.axis("off")

        buf = io.BytesIO()
        plt.savefig(buf, format="png",
                    dpi=quality, bbox_inches="tight",
                    pad_inches=0.1)
        buf.seek(0)
        plt.close(fig)

        return buf
    
    
    def _render_graphics(self, graphic_type: str, filename: str,
                         title: str, data: DataFrame, axes: list,
                         quality: int = 300):
        """Render models
        Graphics"""
        
        graphs_types = {"scatterplot": plt.scatter(data=data, x=axes[0], y=axes[1]),
                        "barplot": plt.bar(data=data, x=axes[0], y=axes[1]),
                        "boxplot": sns.boxplot(data=data, x=axes[0], y=axes[1])}
        
        graphs_types[graphic_type]

        plt.title(title.title())
        plt.xlabel(axes[0].title())
        plt.ylabel(axes[1].title())

        buf = io.BytesIO()
        
        plt.savefig(buf, format="png", dpi=quality)
        plt.close()

        return