# -*- coding: UTF-8 -*-
"""Import modules"""
from dataclasses import dataclass, field
from datetime import datetime
from os import path


@dataclass
class StaticVariables:
    """ 
    Static variables 
    dataclass
    """

    img_dir: str = path.join(
        path.dirname(path.dirname(__file__)), "img"
        )
    data_dir: str = path.join(
        path.dirname(path.dirname(__file__)), "data"
        )
    
    docs_dir: str = path.join(
        path.dirname(path.dirname(__file__)), "docs"
        )
    
    date = datetime.today().date()
    pdf_name: str = "projeto_final_econometria.pdf"
    univ_name: str = "UNIVERSIDADE FEDERAL DA PARAÍBA"
    cent_name: str = "CENTRO DE CIÊNCIAS SOCIAIS APLICADAS"
    dept_name: str = "DEPARTAMENTO DE ECONOMIA"
    teacher_name: str = "PROF. ANTÔNIO VINÍCIUS BARBOSA"
    authors: list = field(default_factory=list)
    title: str =  "PROJETO FINAL - ECONOMETRIA I"
    github: str = "https://github.com/pedroafmelo/projeto_econometria"

    def __post_init__(self):
        self.authors = ["Pedro Augusto A. F. de Melo",
                     "Gabriel Batista Pontes"]



# Answers below



@dataclass
class SalaryAnswers:
    """Salary Model
    Answers dataclass"""

    equation_1: str = r"\log(salario_i) = \beta_0 + \beta_1 educ_i + \beta_2 homem_i + e_i"
    equation_2: str = r"dif\_salarial\_media = -0.033 \times Salario_i"

    intro: str =  """
            O primeiro modelo deste projeto utiliza uma equação de Mincer para quantificar
            a relação existente entre o salário por hora do trabalhador com os anos de
            educação formal e o sexo do trabalhador. O modelo é descrito na equação abaixo:
        """

    question_1: str =  """
            Os resultados do modelo estimado estão descritos no quadro abaixo:
        """
    
    question_2: str = """
            A partir da análise dos resultados do modelo em questão, observa-se que o sinal
            do estimador <I>Beta1</I> associado à variável <I>educ</I> é positivo, o que evidencia
            uma relação direta entre a quantidade de anos formais de estudo e o salário de um 
            trabalhador. Ainda, é importante ressaltar que, por causa da aplicação do <I>log</I>   
            à variável dependente, o valor de <I>Beta1</I> representa a variação esperada relativa
            do salário do trabalhador (dividido por 100) quando se tem um ano a mais de educação 
            formal. Sob esse contexto, o sinal esperado do estimador realmente era positivo, tendo
            em vista que espera-se que uma pessoa com uma formação mais completa tenha maiores salários.
            """
    
    question_4_1: str = """
            A equação que indica a diferença salarial média 
            entre homens e mulheres com características idênticas 
            é dada abaixo:
            """
    
    question_4_2: str = """
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
    

@dataclass
class DiabetesAnswers:
    """ Diabetes Model
    Answers dataclass"""

    notes: str = """
            Nota: não faz sentido gerar média ou desvio padrão 
            para a variável diabetes.
            """ 
    
    question_2: str = """
            Acerca do gráfico que relaciona a idade do indivíduo com o nível de glicose,
            o conjunto de dados parece ter sido colhido de um grupo com grande concentração
            de idade entre 20 e 40 anos, o que pode trazer um pouco de viés à análise mas, 
            em geral, o nível de glicose parece se elevar conforme a idade avança. Além disso,
            no segundo gráfico, este parece possuir uma concentração de observações no centro 
            do plano, onde as pessoas possuem idade que varia de 20 a 40 anos e pressão de 40
            a 100, mas sem uma evidência de relação entre as variáveis mais moderada. 
            """  
    
    question_3_1: str = r"""
            No primeiro modelo proposto, a constante (Beta0) mostra o nível 
            de glicose quando o indivíduo tem 0 ano de idade. Além disso, o 
            valor positivo de 0.693 para Beta1 mostra a relação positiva entre
            as variáveis, onde o nível de glicose varia em Beta1 ponto para cada
            ano a mais de idade do observado. Ainda sobre este modelo, observa-se
            que o p-valor dos estimadores apontam uma forte significância estatística,
            o que faz com que eles sejam considerados estimadores válidos para os
            parâmetros deste modelo, tendo em vista que podem ser considerados
            significantes a 1%.
            """  

    question_3_2: str = r"""
            Neste segundo modelo, a constante apresenta o valor esperado 
            da pressão arterial para indivíduos com imc 0 (o que é impossível), 
            enquanto o valor do coeficiente imc apresenta o valor de 0.52, mostrando
            que o nível da pressão arterial da mulher deve ser elevado em 0.52 unidade
            quando se tem uma variação de uma unidade no imc. Ambos os estimadores são
            estatisticamente significantes a 1%, validando o nosso modelo utilizado 
            (analisando de forma isolada), podendo ser observado também na análise do intervalo de 
            confiança a 95% de confiança, em que o 0 não está inserido nos intervalos.
            """ 
     
    question_6_1: str = r"""
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
            mesma idade. 
        """
    
    question_6_2: str = r"""Entretanto, ao observar o p-valor de cada um dos estimadores,
            nota-se que o Beta0 e o Beta1 são estatisticamente significantes, já que o seu 
            p-valor é inferior ao alpha utilizado (5%). Já com relação ao Beta2, pode-se
            notar que o seu estimador não é estatisticamente significante a 5%, o que nos leva
            a não rejeitar uma possível hipótese H0 de um teste de hipóteses, que afirma que o valor
            de Beta0 é nulo. Assim, tal variável <I>dummy</I> não deve ser validada neste modelo.
            """
