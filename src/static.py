# -*- coding: UTF-8 -*-
"""Import modules"""
from os import path
from dataclasses import dataclass, field
from datetime import datetime

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

    def __post_init__(self):
        self.authors = ["Pedro Augusto A. F. de Melo",
                     "Gabriel Batista Pontes"]