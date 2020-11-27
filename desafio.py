"""Gerador de gráfico de cores aleatório

Este script quando executado pede que o usuário insira um número de no mínimo 50, em seguida extrai do API random color essa quantidade de cores em formato json. 

As cores contêm varias informações, porém as mais relevantes para esse script são seu ID, nome, código hex e a ordem com que foram extraidas. Tendo essas informações o script gera um scatterplot com linha ID x Posição, onde as cores com mais de 50% vermelho em seu RGB são marcadas com bolinhas vermelhas. O gráfico é mostrado em uma simples página na web criada por Flask, para visualiza-lo é necessário copiar o endereço dado pela command line depois da execução do script.

O script também gera um arquivo de texto com a lista de todos os nomes únicos entre as cores geradas, esse arquivo é salvo no mesmo diretório do script.

É necessário que o script seja executado de um diretório contendo uma pasta chamada 'templates' com o arquivo html correspondente.

Esse script requer a instalação de alguns módulos sendo estes: Flask, webcolors, requests e matplotlib. 

"""

from flask import Flask, render_template
import webcolors as wc
import requests
import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from io import BytesIO
import base64

# Abaixo as listas vazias onde as variáveis relevantes para outras operações serão armazenadas
id_list = []
color_names = []
hex_list = []
red_list = [] 

def is_it_red(hex_color):
    # Função simples que verificar se a cor dada tem mais de 50% de vermelho no sistema RGB
    # Retorna preto ou vermelho, porque será usada para representar graficamente o resultado
    #A função hex_to_rgb_percent retorna um string na forma 'x%' e logo tem que ser formatado para ser convertido em float
    red_percent = float((wc.hex_to_rgb_percent(hex_color)[0]).split('%')[0]) 
    if red_percent >= 50: 
        return 'red'
    else:
        return 'black'
        
def importar(n_amostra):
    # Função que popula as lista previamente criadas usando o API random color
    for i in range(n_amostra):
        response = requests.get('https://random-data-api.com/api/color/random_color').json()
        id_list.append(response['id'])
        hex_list.append(response['hex_value'])
        color_names.append(response['color_name'])
        red_list.append(is_it_red(response['hex_value']))

def find_unique():
    # Essa função cria uma lista apenas com as cores de nomes únicos
    # Em seguida as formata em uma string e então a salva como arquivo .txt
    unq_colors_txt = ""
    unique_colors = list(set(color_names))
    for i, color in enumerate(unique_colors):
        if i == 0:
            unq_colors_txt += "{}{}, ".format(color[0].upper(), color[1:])
        elif i == len(unique_colors) - 1:
            unq_colors_txt += "{}.".format(color)
        else:
            unq_colors_txt += "{}, ".format(color)

    with open("unq_colors.txt", "w") as f:
        f.write(unq_colors_txt)    
    
    return unq_colors_txt

# Aqui o usuário insere o tamanho da amostra de cores
# O código abaixo impede o usuário de inserir valores inválidos (como numero menores que 50 ou letras)
while True:
    try:
        t_amostra = int(input("Escolha o tamanho da amostra (min 50): "))
        if t_amostra < 50:
            print('Valor inferior a 50, insira outro valor')
        else:
            break
    except ValueError:
        print('Valor inválido, insira outro valor')

importar(t_amostra)
find_unique()

app = Flask(__name__)
@app.route('/')
def plotter():
    # Essa função cria uma página simples na web contendo o gráfico ID x Posição
    img = BytesIO()
    fig, ax = plt.subplots()
    fig.set_size_inches(12, 4.75)

    for i in range(len(id_list)):
        #Os pontos cujo o RGB tem mais de 50% vermelho serão coloridos em vermelho para alertar o usuário
        ax.scatter(i+1, id_list[i], s=20, color=red_list[i])

    ax.plot(range(1,(len(id_list)+ 1)), id_list, color = 'black', alpha=0.5)
    plt.xlabel("Posição")
    plt.ylabel("ID").set_rotation(0)
    ax.set_xticks([num for num in range(0, len(id_list)+1, 5)])

    if 'red' in red_list: #A legenda só sera adicionada caso exista alguma cor com mais de 50% de vermelho
        red_patch = mpatches.Patch(color='red', label='Igual ou mais de 50% vermelho')
        plt.legend(handles=[red_patch], loc='upper right', bbox_to_anchor = (1, 1.1))
    
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return render_template('plot.html', plot_url=plot_url, texto=find_unique())

if __name__ == "__main__":
    app.run()
         
