# -*- coding: UTF-8 -*- 
"""Import local modules"""
from src.pdf_generator import PDFGen


def main():
    gen_pdf = PDFGen()
    gen_pdf()

if __name__ == "__main__":
    main()