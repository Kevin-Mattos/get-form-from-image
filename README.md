# Estampar Contornos!
 
Referência: 
 
<img src="https://user-images.githubusercontent.com/60194291/93954206-7a8d8880-fd23-11ea-8b11-7684b79bc6e0.PNG" width="500" height="500" />

Caminho da estampagem:

 ![Exemplo desenhando contorno](https://media.giphy.com/media/CY953MIBz2l0JS8SZW/giphy.gif)
 
 
## Requerimentos

Você vai precisar das seguintes bibliotecas: 

* [cv2](https://pypi.org/project/opencv-python/)
* [PIL](https://pypi.org/project/Pillow/)
* [pandas](https://pandas.pydata.org/)
* [numpy](https://numpy.org/)
* [pygame](https://www.pygame.org/news)

## Uso

 Para iniciar salve em formato pdf ou jpg os arquivos dentro da pasta Pdfs, em seguida execute contourfinding.py, que ira processar as imagens e salvar(opcional) os contornos de fora encontrados em uma imagem nas Imagens e salvar as coordenadas nos Outputs.
 Para visualizar o caminho e **obter as coordenadas redimencionadas** que a máquina de estampagem irá percorrer execute seePlot.py

## TODOs
 * Refatorações (organizar melhor a estrutura do código)
 * Otimizações
 * Salvar as novas coordenadas que foram redimencionadas para caber na janela do pygame(esse tamanho é alterável)
 * Adicionar nas coordenadas o caminho para ir para a próxima imagem, por enquando só esta mostrando no pygame
 * Remover funções que não são mais utilizadas

