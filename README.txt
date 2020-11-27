Este script quando executado pede que o usuário insira um número de no mínimo 50, em seguida extrai do API random color essa quantidade de cores em formato json. 

As cores contêm varias informações, porém as mais relevantes para esse script são seu ID, nome, código hex e a ordem com que foram extraidas. Tendo essas informações o script gera um scatterplot com linha ID x Posição, onde as cores com mais de 50% vermelho em seu RGB são marcadas com bolinhas vermelhas. O gráfico é mostrado em uma simples página na web criada por Flask, para visualiza-lo é necessário copiar o endereço dado pela command line depois da execução do script.

O script também gera um arquivo de texto com a lista de todos os nomes únicos entre as cores geradas, esse arquivo é salvo no mesmo diretório do script.

É necessário que o script seja executado de um diretório contendo uma pasta chamada 'templates' com o arquivo html correspondente.

Esse script requer a instalação de alguns módulos sendo estes: Flask, webcolors, requests e matplotlib. 

Para informações mais detalhadas, confira os comentários presentes no script.
