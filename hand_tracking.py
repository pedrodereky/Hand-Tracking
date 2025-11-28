import cv2
import mediapipe as mp
import time
import numpy as np

# ===== CONFIGURAÇÕES =====
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
MAX_HANDS = 2
DETECTION_CONFIDENCE = 0.5
TRACKING_CONFIDENCE = 0.5
TIP_IDS = [4, 8, 12, 16, 20]
DRAWING_COLOR = (0, 255, 0)  # Verde
DRAWING_THICKNESS = 3

# ===== INICIALIZAÇÃO =====
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=MAX_HANDS,
    min_detection_confidence=DETECTION_CONFIDENCE,
    min_tracking_confidence=TRACKING_CONFIDENCE
)
mp_draw = mp.solutions.drawing_utils

# Abrir câmera com validação
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print(" Erro: Não foi possível abrir a câmera")
    exit(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

# ===== VARIÁVEIS PARA FPS =====
fps_time = time.time()
fps_counter = 0
current_fps = 0

# ===== CANVAS PARA DESENHO =====
canvas = np.zeros((CAMERA_HEIGHT, CAMERA_WIDTH, 3), dtype=np.uint8)
prev_pos = None

def contar_dedos(hand_landmarks):
    """Conta quantos dedos estão levantados"""
    dedos = []
    
    # Dedão (se baseia no eixo X)
    if hand_landmarks.landmark[TIP_IDS[0]].x < hand_landmarks.landmark[TIP_IDS[0] - 1].x:
        dedos.append(1)
    else:
        dedos.append(0)
    
    # Outros dedos (se baseiam no eixo Y)
    for id in range(1, 5):
        if hand_landmarks.landmark[TIP_IDS[id]].y < hand_landmarks.landmark[TIP_IDS[id] - 2].y:
            dedos.append(1)
        else:
            dedos.append(0)
    
    return dedos.count(1)

def get_finger_tip_position(hand_landmarks, frame_width, frame_height):
    """Retorna a posição do dedo indicador (TIP_IDS[1])"""
    tip = hand_landmarks.landmark[TIP_IDS[1]]  # Dedo indicador
    x = int(tip.x * frame_width)
    y = int(tip.y * frame_height)
    return (x, y)

try:
    while True:
        success, img = cap.read()
        if not success:
            print("⚠️ Erro ao capturar frame")
            continue

        # Flip para espelhar a imagem (mais intuitivo)
        img = cv2.flip(img, 1)

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        total_dedos_esquerda = 0
        total_dedos_direita = 0
        num_maos = 0

        if results.multi_hand_landmarks and results.multi_handedness:
            num_maos = len(results.multi_hand_landmarks)
            
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                dedos_levantados = contar_dedos(hand_landmarks)
                
                # Classificar mão esquerda ou direita
                if handedness.classification[0].label == "Right":
                    total_dedos_direita = dedos_levantados
                else:
                    total_dedos_esquerda = dedos_levantados

                # ===== DESENHO =====
                # Se apenas o dedo indicador está levantado, desenhar
                if dedos_levantados == 1:
                    current_pos = get_finger_tip_position(hand_landmarks, CAMERA_WIDTH, CAMERA_HEIGHT)
                    
                    # Desenhar ponto onde o dedo está
                    cv2.circle(img, current_pos, 5, DRAWING_COLOR, -1)
                    cv2.circle(canvas, current_pos, 5, DRAWING_COLOR, -1)
                    
                    # Desenhar linha entre posições
                    if prev_pos is not None:
                        cv2.line(img, prev_pos, current_pos, DRAWING_COLOR, DRAWING_THICKNESS)
                        cv2.line(canvas, prev_pos, current_pos, DRAWING_COLOR, DRAWING_THICKNESS)
                    
                    prev_pos = current_pos
                else:
                    prev_pos = None

        # ===== CALCULAR FPS =====
        fps_counter += 1
        if time.time() - fps_time > 1:
            current_fps = fps_counter
            fps_counter = 0
            fps_time = time.time()

        # ===== SOBREPOR CANVAS =====
        img = cv2.addWeighted(img, 1, canvas, 0.5, 0)

        # ===== MOSTRAR TEXTOS NA IMAGEM =====
        cv2.putText(img, f"Esquerda: {total_dedos_esquerda}", (30, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)
        cv2.putText(img, f"Direita: {total_dedos_direita}", (30, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
        cv2.putText(img, f"Total de maos: {num_maos}", (30, 220),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
        cv2.putText(img, f"FPS: {current_fps}", (30, 290),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 2)
        cv2.putText(img, "Leve 1 dedo para desenhar | 'C' limpar | 'ESC' sair", (30, CAMERA_HEIGHT - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow("Hand Tracking", img)

        # Controles
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            break
        elif key == ord('c') or key == ord('C'):  # Limpar desenho
            canvas = np.zeros((CAMERA_HEIGHT, CAMERA_WIDTH, 3), dtype=np.uint8)
            print(" Canvas limpo")

except KeyboardInterrupt:
    print("\n Encerrando...")
except Exception as e:
    print(f" Erro: {e}")
finally:
    cap.release()
    cv2.destroyAllWindows()
    print(" Recursos liberados")