"""Taller evaluable"""

import glob

import pandas as pd


def load_input(input_directory):
    # Lea los archivos de texto en la carpeta input/ y almacene el contenido en
    # un DataFrame de Pandas. Cada línea del archivo de texto debe ser una
    # entrada en el DataFrame.
    """Load text files in 'input_directory/'"""
    filenames = glob.glob(input_directory + "/*.*")
    dataframes=[pd.read_csv(filename, sep=";", names=["text"]) for filename in filenames]
    dataframes=pd.concat(dataframes).reset_index(drop=True)
    return dataframes

def clean_text(dataframe):
    """Text cleaning"""
    #
    # Elimine la puntuación y convierta el texto a minúsculas.
    #
    dataframe=dataframe.copy()
    dataframe['text']=dataframe['text'].str.lower()
    dataframe['text']=dataframe['text'].str.replace(",","").str.replace(".","")
    return dataframe



def count_words(dataframe):
    dataframe=dataframe.copy()
    dataframe['text']=dataframe['text'].str.split()
    dataframe=dataframe.explode('text').reset_index(drop=True) #explode para voltear las gilas por columas. Reset para que no se repita el número
    dataframe=dataframe.rename(columns={'text':'word'})
    dataframe['count']=1
    conteo=dataframe.groupby(['word'], as_index=False).agg(
        {
        'count':sum
        }
    )
    return conteo
    """Word count"""


def save_output(dataframe, output_filename):
    """Save output to a file."""

    dataframe.to_csv(output_filename,index=False, sep=";")


#
# Escriba la función job, la cual orquesta las funciones anteriores.
#
def run(input_directory, output_filename):
    dataframe=load_input(input_directory)
    dataframe=clean_text(dataframe)
    dataframe=count_words(dataframe)
    save_output(dataframe,output_filename)
    """Call all functions."""


if __name__ == "__main__":
    run(
        "input",
        "output.txt",
    )
