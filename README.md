# Estampar Contornos!
 
## Requerimentos

Você vai precisar das seguintes bibliotecas: 

* [cv2](https://pypi.org/project/opencv-python/)
* [PIL](https://pypi.org/project/Pillow/)
* [pandas](https://pandas.pydata.org/)
* [numpy](https://numpy.org/)
* [pygame](https://www.pygame.org/news)

## Uso

 Para iniciar, salve em formato pdf ou jpg os arquivos dentro da pasta Pdfs, em seguida execute contourfinding.py, que ira processar as imagens e salvar os contornos em uma imagem(opcional) nas Imagens e salvar as coordenadas nos Outputs.
 Para visualizar o caminho que a maquina de estampagem ira percorrer, execute seePlot.py

## TODOs
 * Refatorações (organizar melhor a estrutura do código)
 * Otimizações
 * Salvar as novas coordenadas que foram redimencionadas para caber na janela do pygame(esse tamanho é alterável)
 * Adicionar nas coordenadas o caminho para ir para a próxima imagem, por enquando só esta mostrando no pygame
 * Remover funções que não são mais utilizadas
