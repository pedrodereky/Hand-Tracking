Hand Tracking
Este projeto implementa um sistema de rastreamento das mãos em tempo real utilizando OpenCV e MediaPipe. Ele detecta até duas mãos simultaneamente, identifica landmarks, determina a quantidade de dedos levantados, acompanha o movimento da ponta do dedo indicador e exibe informações úteis, como FPS, diretamente no vídeo.
Descrição Geral
O sistema captura imagens da webcam, processa os frames com o módulo Hands do MediaPipe e aplica lógica própria para:
Detectar mãos e landmarks.
Identificar quais dedos estão levantados.
Obter a posição da ponta do dedo indicador.
Desenhar esqueleto da mão e landmarks na tela.
Exibir FPS.
Operar com baixa latência.
O código possui configurações ajustáveis, tornando-o adequado para testes, aplicações interativas e desenvolvimento de interfaces baseadas em gestos.
Funcionalidades
Rastreamento de até duas mãos simultaneamente.
Detecção de landmarks em tempo real.
Cálculo independente dos dedos levantados.
Obtenção precisa da posição do dedo indicador.
Renderização completa da mão com linhas e marcações.
Configuração de resolução da câmera.
Cálculo de FPS utilizando medição de tempo.
Código estruturado em funções para facilitar expansão.
Tecnologias Utilizadas
Python
OpenCV
MediaPipe
NumPy
Webcam integrada ou USB
Instalação
Instale as dependências:
pip install opencv-python mediapipe numpy
Execute o script:
python hand_tracking.py
Estrutura do Código
Configurações iniciais: resolução, número máximo de mãos, confiança mínima, IDs dos dedos.
Funções utilitárias:
count_fingers: identifica dedos levantados.
get_finger_tip_position: retorna a posição da ponta do dedo indicador.
Loop principal:
Captura da webcam.
Processamento dos landmarks.
Desenho da mão no frame.
Exibição de FPS.
Impressão no terminal: quantidade de dedos levantados e coordenadas da ponta do dedo.
Possíveis Extensões
Reconhecimento de gestos personalizados.
Controle por gestos para interfaces ou jogos.
Integração com aplicações de automação.
Sistema de desenho na tela usando o movimento do dedo indicador.
Reconhecimento de sinais ou poses estáticas.
Licença
Este projeto pode ser adaptado para qualquer finalidade. Caso deseje, posso gerar uma licença padrão como MIT, Apache ou GPL.
