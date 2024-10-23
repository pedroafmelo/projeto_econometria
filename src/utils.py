# -*- coding: UTF-8 -*-
"""Import modules"""
import matplotlib.pyplot as plt
import seaborn as sns
import io
from os import path
from pandas import DataFrame, Series
import numpy as np
import statsmodels.api as sm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.pdfgen.canvas import Canvas


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
                    pad_inches=0.01)
        buf.seek(0)
        plt.close(fig)

        return buf
    
    
    def _render_graphics(self, data: DataFrame,
                         title: str,  axes: list,
                         quality: int = 300,
                         regplot: bool = False,
                         predictions: Series = []):
        """Render pdfs
        Graphics"""
        
        try:
        
            plt.scatter(data=data, x=axes[0], y=axes[1])

            if regplot:
                regline = predictions
                plt.plot(np.array(data[axes[0]]), regline, color="red", label="Reg. Line")

            plt.title(title.title())
            plt.xlabel(axes[0].title())
            plt.ylabel(axes[1].title())

            buf = io.BytesIO()
            
            plt.savefig(buf, format="png", dpi=quality)
            buf.seek(0)

            plt.close()
        
        except Exception as error:
            raise OSError(error) from error

        return buf
    

    def _render_table(self, pdf_canvas: Canvas, 
                      matrix: list, x: float, y: float) -> None:
        """Render pdf
        Tables"""

        table = Table(matrix)

        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Cabeçalho
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        w, h = table.wrapOn(pdf_canvas, x, y)
    
        table.drawOn(pdf_canvas, x, y)

        return "Generated table"


    def _render_paragraph(self, canvas: Canvas, text: str, 
                          x: float, y: float) -> None:
        """Render pdf
        paragraphs"""

        style = ParagraphStyle(
            name="Normal",
            fontName="Helvetica",
            fontSize=12,
            leading=18,  
            textColor=colors.black,
            alignment=4  #justificado
        )

        paragraph = Paragraph(text, style)

        w, h = paragraph.wrapOn(canvas, 400, 600)

        paragraph.drawOn(canvas, x, y)

        return "Generated Paragraph"