# -*- coding: UTF-8 -*-
"""Import modules"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from os import path
import time


class PDFGen:
    """
    .pdf generator 
    class
    """

    def __init__(self):
        """Initialize instance"""

        # import local module
        from src.static import StaticVariables

        self.static = StaticVariables()

        try:
            self.c = canvas.Canvas(path.join(
                    self.static.docs_dir,
                    self.static.pdf_name), pagesize=letter)
            print("Created .pdf file! \n")
        except:
            print("Couldn't create .pdf file")


    def __str__(self):
        """String representation"""
        
        return f"{self.static.pdf_name} PDF Generator"
    
    
    def __repr__(self):
        """Default representation"""
        
        return f"{self.static.pdf_name} PDF Generator"
    

    def __call__(self):
        """
        Call PDFGen 
        class
        """
        self.gen_cover()
        time.sleep(3)
        self.gen_summary()
        time.sleep(3)
        self.salary_model_pages()
    

    def gen_cover(self) -> None:
        """ 
        Generate pdf cover
        return None
        """

        c = self.c

        c.setFont("Helvetica-Bold", 14)
        c.bookmarkPage("page_1")

        c.drawImage(path.join(
            self.static.img_dir,
            "cabecalho.png"), 0,660, width=700, height=300
        )
        c.drawImage(path.join(
            self.static.img_dir,
            "logo_ufpb.png"), 40, 600, width=150, height=100),
        
        c.drawString(173, 675, self.static.univ_name)
        c.drawString(158, 655, self.static.cent_name)
        c.drawString(188, 635, self.static.dept_name)
        c.drawString(178, 615, self.static.teacher_name)

        c.drawString(90, 450, self.static.authors[0])
        c.drawString(360, 450, self.static.authors[1])
        c.drawString(185, 280, self.static.title)

        c.drawString(255, 100, "João Pessoa")
        c.drawString(225, 70, 
                     f"{self.static.date.day} de Outubro de {self.static.date.year}"
                     )
        
        c.drawImage(path.join(
            self.static.img_dir,
            "rodape.png"), 0, -272, width=700, height=300
        )
        # c.save()
        c.showPage()
        print("Created Cover!")


    def gen_summary(self) -> None:
        """Generate linked summary
        return None"""

        c = self.c

        c.setFont("Helvetica-Bold", 14)
        c.bookmarkPage("page_2")

        c.drawAlignedString(350, 675, "NAVEGAÇÃO")

        c.setFont("Helvetica", 14)

        c.drawString(80, 610, f"Mercado de Trabalho{'.' * 74} 3")
        c.linkAbsolute(contents="Direcionar para problema 1 do projeto",
                       destinationname="page_3",
                       Rect=(80, 611, 515, 625), Border='[0,0,0]')
        c.drawString(80, 590, f"Taxa de Glicose e Incidência de Diabetes{'.' * 42} 6")
        # c.linkAbsolute(contents="Direcionar para problema 2 do projeto",
        #                destinationname="page_6",
        #                Rect=(80, 590, 515, 600), Border='[0,0,0]')

        c.showPage()
        print("Created Summary")


    def salary_model_pages(self) -> None:
        """Generate 1st model pages
        return None"""

        c = self.c

        c.setFont("Helvetica-Bold", 14)
        c.bookmarkPage("page_3")

        c.showPage()

        
        c.save()


