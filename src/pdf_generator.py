# -*- coding: UTF-8 -*-
"""Import modules"""
from os import path

from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


class PDFGen:
    """
    .pdf generator 
    class
    """

    def __init__(self):
        """Initialize instance"""

        # import local module
        from src.static import DiabetesAnswers, SalaryAnswers, StaticVariables
        from src.utils import Utils

        self.static = StaticVariables()
        self.salary_answers = SalaryAnswers()
        self.diab_answers = DiabetesAnswers()
        self.utils = Utils()

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
    

    def __call__(self) -> None:
        """
        Call PDFGen 
        class
        """
        self.gen_cover()
        self.gen_summary()
        self.salary_model_pages()
        self.diabetes_model_pages()
    

    def gen_cover(self) -> None:
        """ 
        Generate pdf cover
        return None
        """

        c = self.c #pdf canvas

        # set font config
        c.setFont("Helvetica-Bold", 14)

        # bookmark page (link page)
        c.bookmarkPage("page_1")

        # cover images
        c.drawImage(path.join(
            self.static.img_dir,
            "cabecalho.png"), 0,660, width=700, height=300
        )
        c.drawImage(path.join(
            self.static.img_dir,
            "logo_ufpb.png"), 40, 600, width=150, height=100),
        
        c.drawImage(path.join(
            self.static.img_dir,
            "rodape.png"), 0, -272, width=700, height=300
        )

        # cover informations
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
        
        # finish page
        c.showPage()

        print("Created Cover!")


    def gen_summary(self) -> None:
        """Generate linked summary
        return None"""

        c = self.c

        c.setFont("Helvetica-Bold", 14)
        c.bookmarkPage("page_2")

        # page title
        c.drawAlignedString(350, 675, "NAVEGAÇÃO")

        # change font config
        c.setFont("Helvetica", 14)

        # creating a linked summary
        c.drawString(80, 610, f"Mercado de Trabalho{'.' * 74} 3")
        c.linkAbsolute(contents="Direcionar para problema 1 do projeto",
                       destinationname="page_3",
                       Rect=(80, 611, 515, 625), Border='[0,0,0]')
        
        c.drawString(80, 590, f"Taxa de Glicose e Incidência de Diabetes{'.' * 42} 5")
        c.linkAbsolute(contents="Direcionar para problema 2 do projeto",
                       destinationname="page_5",
                       Rect=(80, 591, 515, 600), Border='[0,0,0]')
        
        # github repo
        c.drawString(80, 570, f"Link para repositório{'.' * 79}")
        c.linkURL(self.static.github,
                  (80, 571, 515, 580), relative = 0)

        c.showPage()

        print("Created Summary")


    def salary_model_pages(self) -> None:
        """Generate 1st model pages
        return None"""

        # import local module
        from src.salary_model import SalaryModel
        model = SalaryModel("salario_mercado.csv")

        c = self.c

        c.setFont("Helvetica-Bold", 14)
        c.bookmarkPage("page_3")

        # page title
        c.drawString(220, 675, "Análise do modelo salarial")

        # render and print model equation as .png
        latex_eq_buf = self.utils._render_latex_img(
            self.salary_answers.equation_1,
            quality=500
            )
        img = ImageReader(latex_eq_buf)
        c.drawImage(img, 170, 470, width=250, height=140)
        
        # print introduction
        self.utils._render_paragraph(c, self.salary_answers.intro, 100, 565)

        # question 1 answer
        c.setFont("Helvetica", 14)
        c.drawString(100, 500, "1 - ")
        self.utils._render_paragraph(c, self.salary_answers.question_1, 100, 475)
        # run salary model
        matrix = model._build_mult_model(["educ", "homem"])
        # print model table
        self.utils._render_table(c, matrix, 105, 370)

        # question 2 answer
        c.drawString(100, 330, "2 - ")
        self.utils._render_paragraph(c, self.salary_answers.question_2, 100, 140)

        # salary_means table     
        matrix = model._calculate_mean()

        # question 3
        c.drawString(100, 100, "3 - ")
        # render and print question 3 table
        self.utils._render_table(c, matrix, 190, 65)

        c.showPage()

        # New page
        c.bookmarkPage("page_4")

        # render and print model equation as .png
        latex_eq_buf = self.utils._render_latex_img(
            self.salary_answers.equation_2, 
            quality=500)
        img = ImageReader(latex_eq_buf)
        c.drawImage(img, 170, 555, width=250, height=170)
        
        # print question 4 part 1 and 2
        self.utils._render_paragraph(c, self.salary_answers.question_4_1, 100, 675)
        
        self.utils._render_paragraph(c, self.salary_answers.question_4_2, 100, 370)

        c.showPage()

        print("Salary Model Done")


    def diabetes_model_pages(self) -> None:
        """Generate 2nd model pages
        return None"""

        from src.diabetes_model import DiabetesModel

        model = DiabetesModel("diabetes_dados.csv")

        c = self.c
        c.setFont("Helvetica-Bold", 14)
        c.bookmarkPage("page_5")

        c.drawString(190, 675, "Análise do modelo de diabetes")

        # render and print question 1 table
        matrix = model._basic_statistics()

        c.setFont("Helvetica", 14)
        c.drawString(100, 620, "1 - ")
        self.utils._render_table(c, matrix, 60, 540)
        # notes
        self.utils._render_paragraph(c, self.diab_answers.notes, 100, 485)
        
        # render and print question 2 graphics
        c.drawString(100, 440, "2 - ")
        graph_1 = ImageReader(model._plot_graphs()[0])
        c.drawImage(graph_1, 60, 240, width=250, height=200)
        graph_2 = ImageReader(model._plot_graphs()[1])
        c.drawImage(graph_2, 310, 240, width=250, height=200)

        # question 2 answer       
        self.utils._render_paragraph(c, self.diab_answers.question_2, 100, 70)

        c.showPage()
        
        # new page
        c.setFont("Helvetica", 14)
        c.bookmarkPage("page_6")
        c.drawString(100, 675, "3 - ")

        # run question 3 model 1
        matrix = model._build_simple_model(["idade", "glicose"])
        c.setFont("Helvetica-Bold", 14)

        # graph title
        c.drawString(255, 675, "Idade x Glicose")
        self.utils._render_table(c, matrix, 142, 570)
        self.utils._render_paragraph(c, self.diab_answers.question_3_1, 100, 400)

         # run question 3 model 2
        matrix = model._build_simple_model(["imc", "pressao_arterial"])

        # graph title
        c.drawString(230, 360, "IMC x Pressão Arterial")
        self.utils._render_table(c, matrix, 145, 255)
        self.utils._render_paragraph(c, self.diab_answers.question_3_2, 100, 60)
        
        c.showPage()

        # new page
        c.setFont("Helvetica", 14)
        c.bookmarkPage("page_7")
        
        # question 4
        c.drawString(100, 675, "4 - ")

        # plotting graphs with regline
        regplot_idade_glicose = model._plot_reg_lines()[0]
        img = ImageReader(regplot_idade_glicose)
        c.drawImage(img, 60, 470, width=250, height=200)

        regplot_pressao_imc = model._plot_reg_lines()[1]
        img = ImageReader(regplot_pressao_imc)
        c.drawImage(img, 310, 470, width=250, height=200)
        
        # question 5
        c.drawString(100, 440, "5 & 6 - ")
        matrix = model._build_mult_model("glicose", ["idade"])
        self.utils._render_table(c, matrix, 100, 335)
        self.utils._render_paragraph(c, self.diab_answers.question_6_1, 100, 40)

        c.showPage()

        # new page, continue question 5 and 6
        self.utils._render_paragraph(c, self.diab_answers.question_6_2, 100, 580)

        c.save()

        print("Diabetes Model Done")