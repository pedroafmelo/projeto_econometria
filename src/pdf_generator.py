# -*- coding: UTF-8 -*-
"""Import modules"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
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
        from src.utils import Utils

        self.static = StaticVariables()
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

        c = self.c # pdf_canvas

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
        
        c.drawString(80, 590, f"Taxa de Glicose e Incidência de Diabetes{'.' * 42} 5")
        c.linkAbsolute(contents="Direcionar para problema 2 do projeto",
                       destinationname="page_5",
                       Rect=(80, 591, 515, 600), Border='[0,0,0]')
        
        c.drawString(80, 570, f"Link para repositório{'.' * 79}")
        c.linkURL(self.static.github,
                  (80, 571, 515, 580), relative = 0)

        c.showPage()
        print("Created Summary")


    def salary_model_pages(self) -> None:
        """Generate 1st model pages
        return None"""

        from src.salary_model import SalaryModel

        model = SalaryModel("salario_mercado.csv")

        c = self.c
        c.setFont("Helvetica-Bold", 14)
        c.bookmarkPage("page_3")

        # 1st and 2nd questions

        c.drawString(220, 675, "Análise do modelo salarial")

        latex_eq_buf = self.utils._render_latex_img(
            r"\log(salario_i) = \beta_0 + \beta_1 educ_i + \beta_2 homem_i + e_i",
            quality=500
            )
        img = ImageReader(latex_eq_buf)
        c.drawImage(img, 170, 470, width=250, height=140)
        
        text = """
            O primeiro modelo deste projeto utiliza uma equação de Mincer para quantificar
            a relação existente entre o salário por hora do trabalhador com os anos de
            educação formal e o sexo do trabalhador. O modelo é descrito na equação abaixo:
        """
        self.utils._render_paragraph(c, text, 100, 565)

        text = """
            1 - Os resultados do modelo estimado estão descritos no quadro abaixo:
        """
        self.utils._render_paragraph(c, text, 100, 485)

        matrix = model._build_mult_model(["educ", "homem"])
        text = """
            2 - A partir da análise dos resultados do modelo em questão, observa-se que o sinal
            do estimador <I>Beta1</I> associado à variável <I>educ</I> é positivo, o que evidencia
            uma relação direta entre a quantidade de anos formais de estudo e o salário de um 
            trabalhador. Ainda, é importante ressaltar que, por causa da aplicação do <I>log</I>   
            à variável dependente, o valor de <I>Beta1</I> representa a variação esperada relativa
            do salário do trabalhador (dividido por 100) quando se tem um ano a mais de educação 
            formal. Sob esse contexto, o sinal esperado do estimador realmente era positivo, tendo
            em vista que espera-se que uma pessoa com uma formação mais completa tenha maiores salários."""

        self.utils._render_table(c, matrix, 105, 370)
        self.utils._render_paragraph(c, text, 100, 160)

     
        text = """
            3 -
            """
        matrix = model._calculate_mean()

        self.utils._render_paragraph(c, text, 100, 110)
        self.utils._render_table(c, matrix, 190, 80)

        c.showPage()

        c.bookmarkPage("page_4")

        text = """
            4 - A equação que indica a diferença salarial média 
            entre homens e mulheres com características idênticas 
            é dada abaixo:
            """
        
        latex_eq_buf = self.utils._render_latex_img(
            r"dif\_salarial\_media = -0.033 \times Salario_i", 
            quality=500)
        
        img = ImageReader(latex_eq_buf)
        c.drawImage(img, 170, 555, width=250, height=170)
        
        self.utils._render_paragraph(c, text, 100, 675)

        text = """
            Tomando os resultados como base, nota-se que o valor negativo de 
            0,033 para o estimador de Beta2 mostra o que a variável <I>dummy</I>
            homem altera o intercepto do modelo em aproximadamente 3,3% para baixo,
            sendo assim a <I>dummy</I> de intercepto do nosso modelo. Entretanto,
            quando o teste de hipótese é realizado, com a H0 afirmando que o Beta2 é nulo
            e a H1 afirmando que o Beta2 é não nulo, a um nível de significância alpha 
            de 5%, o resultado do p-valor maior que alpha implica na não rejeição da H0.
            Ainda, há uma outra forma de se chegar à mesma conclusão, que é a apartir da
            análise do intervalo de confiança do Beta2, que inclui o valor 0, o que
            reforça o caráter não significante do nosso estimador e, consequentemente
            mostra a falta de influência da variável sexo no salário do trabalhador,
            mesmo que o modelo e a análise das médias salariais mostrem o contrário.
            """
        
        self.utils._render_paragraph(c, text, 100, 370)

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

        matrix = model._basic_statistics()

        text = "1 - "
        self.utils._render_paragraph(c, text, 60, 600)
        self.utils._render_table(c, matrix, 60, 530)

        text = """
            Nota: não faz sentido gerar média ou desvio padrão 
            para a variável diabetes.
            """  
        
        self.utils._render_paragraph(c, text, 100, 475)

        text = """
            2 - 
            """  
        
        self.utils._render_paragraph(c, text, 60, 440)

        graph_1 = ImageReader(model._plot_graphs()[0])
        c.drawImage(graph_1, 60, 240, width=250, height=200)
        graph_2 = ImageReader(model._plot_graphs()[1])
        c.drawImage(graph_2, 310, 240, width=250, height=200)

        text = """
            Acerca do gráfico que relaciona a idade do indivíduo com o nível de glicose,
            o conjunto de dados parece ter sido colhido de um grupo com grande concentração
            de idade entre 20 e 40 anos, o que pode trazer um pouco de viés à análise mas, 
            em geral, o nível de glicose parece se elevar conforme a idade avança. Além disso,
            no segundo gráfico, este parece possuir uma concentração de observações no centro 
            do plano, onde as pessoas possuem idade que varia de 20 a 40 anos e pressão de 40
            a 100, mas sem uma forte evidência de relação entre as variáveis. 
            """  
        
        self.utils._render_paragraph(c, text, 100, 70)

        c.showPage()

        text = """
            3 - 
            """  
        
        self.utils._render_paragraph(c, text, 60, 675)

        matrix = model._build_simple_model(["idade", "glicose"])

        c.setFont("Helvetica-Bold", 14)

        c.drawString(255, 675, "Idade x Glicose")

        self.utils._render_table(c, matrix, 145, 570)

        text = r"""
            No primeiro modelo proposto, a Constante (Beta0) mostra o nível 
            de glicose quando o indivíduo tem 0 ano de idade. Além disso, o 
            valor positivo de 0.97 para Beta1 mostra a relação positiva entre
            as variáveis, onde o nível de glicose varia em 0.97 ponto para cada
            ano a mais de idade do observado. Ainda sobre este modelo, observa-se
            que o p-valor dos estimadores apontam uma forte sifnificância estatística,
            o que faz com que eles sejam considerados estimadores válidos para os
            parâmetros deste modelo, tendo em vista que podem ser considerados
            significantes a 1% de significância.
            """  
        
        self.utils._render_paragraph(c, text, 100, 360)

        text = """
            4 - 
            """  
        
        self.utils._render_paragraph(c, text, 60, 300)

        reg_idade_glicose = model._plot_reg_lines()[0]
        img = ImageReader(reg_idade_glicose)
        c.drawImage(img, 60, 100, width=250, height=200)

        reg_pressao_imc = model._plot_reg_lines()[1]
        img = ImageReader(reg_pressao_imc)
        c.drawImage(img, 310, 100, width=250, height=200)

        c.showPage()

        c.bookmarkPage("page_6")

        text = """
            5 - 
            """  
        
        self.utils._render_paragraph(c, text, 60, 680)

        matrix = model._build_mult_model("glicose", ["idade"])

        self.utils._render_table(c, matrix, 100, 590)

        text = r"""
            Neste último modelo construído, cujos resultados estão apresentados acima,
            a relação entre o nível de glicose e as variáveis idade e a dummy <I>d_gravidez</I>
            é mensurada de forma linear e, a partir da análise do quadro acima,
            pode-se analisar a influência das variáveis independentes na taxa de glicose.
            Nesse contexto, observa-se que o valor da constante (97.318) mostra o valor 
            do nível de glicose para mulheres que não tiveram gestações  e com 0 ano. 
            Ainda, conforme a idade é elevada em 1 unidade, ocorre uma variação no nível de glicose 
            de 0.73 unidades, que é justamente o valor captado pelo estimador Beta1 associado
            à variável idade. Além disso, o estimador Beta2, coeficiente atrelado à variável 
            <I>d_gravidez</I>, com o valor negativo de -1.012 é uma variável <I>dummy</I>
            de intercepto, representando portanto a diferença média no nível de glicose
            de mulheres que já tiveram alguma gestação e das que não tiveram, a uma
            mesma idade. Entretanto, ao observar o p-valor de cada um dos estimadores,
            nota-se que o Beta0 e o Beta1 são estatisticamente significantes, já que o seu 
            p-valor é inferior ao alpha utilizado (5%). Já com relação ao Beta2, pode-se
            notar que o seu estimador não é estatisticamente significante a 5%, o que nos leva
            a não rejeitar uma possível hipótese H0 de um teste de hipóteses, que afirma que o valor
            de Beta0 é nulo. Assim, tal variável <I>dummy</I> não deve ser validada neste modelo.
            """  
        
        self.utils._render_paragraph(c, text, 100, 180)

        c.save()


