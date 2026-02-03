import sys
import math
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush, QFont
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QSlider, QLabel
)


class DrillAnimationWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.state = "IDLE"
        self.running = True

        self.dt = 0.016
        self.speed = 1.0

        # Carriage position (0..1) along rail
        self.carriage_pos = 0.05

        # Targets:
        # IDLE and WEIGHING are same height
        self.target_idle = 0.10
        self.target_weigh = 0.10
        self.target_drill = 0.80

        self.rot_phase = 0.0
        self.rot_speed = 0.0

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(int(self.dt * 1000))

        self.setMinimumSize(900, 520)

    def set_state(self, state: str):
        self.state = state
        if state == "DRILLING":
            self.rot_speed = 8.0
        else:
            self.rot_speed = 0.0

    def set_speed(self, s: float):
        self.speed = s

    def tick(self):
        if not self.running:
            return

        if self.state == "IDLE":
            target = self.target_idle
        elif self.state == "WEIGHING":
            target = self.target_weigh
        else:
            target = self.target_drill

        alpha = 0.08 * self.speed
        self.carriage_pos = (1 - alpha) * self.carriage_pos + alpha * target

        self.rot_phase += self.rot_speed * self.dt * self.speed
        self.rot_phase %= (2 * math.pi)

        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        W = self.width()
        H = self.height()

        p.fillRect(0, 0, W, H, QColor("#ffffff"))

        ground_y = int(H * 0.78)
        ground_h = int(H * 0.16)

        base_x = int(W * 0.20)
        base_y = int(H * 0.18)
        base_w = int(W * 0.10)
        base_h = int(H * 0.45)

        rail_x = base_x + int(base_w * 0.85)
        rail_y = base_y + int(base_h * 0.05)
        rail_w = int(W * 0.018)
        rail_h = int(base_h * 0.90)

        carriage_w = int(W * 0.07)
        carriage_h = int(H * 0.09)

        carriage_y = rail_y + int(self.carriage_pos * (rail_h - carriage_h))
        carriage_x = rail_x + int(rail_w * 0.65)

        bit_w = int(W * 0.028)
        bit_h = int(H * 0.32)
        bit_x = carriage_x + int(carriage_w * 0.52) - bit_w // 2
        bit_y = carriage_y + carriage_h

        # Weight dimensions
        weight_w = int(W * 0.07)
        weight_h = int(H * 0.05)

        # Weight positions:
        # - IDLE: moved away to the left (not under drill)
        # - WEIGHING: directly under drill-bit (as in your sketch)
        if self.state == "WEIGHING":
            weight_x = bit_x - (weight_w // 2) + (bit_w // 2)
            weight_y = ground_y - weight_h - 6
        else:
            weight_x = base_x - int(W * 0.10)
            weight_y = ground_y - weight_h - 6

        # --- Ground ---
        p.setPen(QPen(QColor("#111111"), 3))
        p.setBrush(QBrush(QColor("#7a5a4f")))
        p.drawRoundedRect(int(W * 0.08), ground_y, int(W * 0.4), ground_h, 18, 18)

        # --- Base ---
        p.setPen(QPen(QColor("#111111"), 3))
        p.setBrush(QBrush(QColor("#1f77c9")))
        p.drawRoundedRect(base_x, base_y, base_w, base_h, 18, 18)

        # --- Rail ---
        p.setPen(QPen(QColor("#111111"), 3))
        p.setBrush(QBrush(QColor("#b5b5b5")))
        p.drawRoundedRect(rail_x, rail_y, rail_w, rail_h, 10, 10)

        # --- Carriage ---
        p.setPen(QPen(QColor("#111111"), 3))
        p.setBrush(QBrush(QColor("#1f77c9")))
        p.drawRoundedRect(carriage_x, carriage_y, carriage_w, carriage_h, 14, 14)

        bracket_w = int(carriage_w * 0.75)
        bracket_h = int(carriage_h * 0.55)
        bracket_x = carriage_x + int(carriage_w * 0.15)
        bracket_y = carriage_y - int(carriage_h * 0.55)
        p.drawRoundedRect(bracket_x, bracket_y, bracket_w, bracket_h, 14, 14)

        # --- Drill bit ---
        p.setPen(QPen(QColor("#111111"), 3))
        p.setBrush(QBrush(QColor("#f5f5f5")))
        p.drawRoundedRect(bit_x, bit_y, bit_w, bit_h, 10, 10)

        # --- Red stripes (rotation illusion) ---
        stripe_pen = QPen(QColor("#d62728"), 4)
        p.setPen(stripe_pen)

        spacing = max(12, int(bit_h * 0.10))
        offset = int((self.rot_phase / (2 * math.pi)) * spacing)

        p.save()
        p.setClipRect(bit_x, bit_y, bit_w, bit_h)

        for y in range(bit_y - spacing, bit_y + bit_h + spacing, spacing):
            y0 = y + offset
            x1, y1 = bit_x - int(bit_w * 0.2), y0 + int(bit_w * 0.8)
            x2, y2 = bit_x + bit_w + int(bit_w * 0.2), y0 - int(bit_w * 0.8)
            p.drawLine(x1, y1, x2, y2)

        p.restore()

        # --- Weight (green) ---
        p.setPen(QPen(QColor("#111111"), 3))
        p.setBrush(QBrush(QColor("#2ca02c")))
        p.drawRoundedRect(weight_x, weight_y, weight_w, weight_h, 12, 12)

        # --- Text ---
        ground_top = ground_y
        bit_tip_y = bit_y + bit_h
        depth_px = max(0, bit_tip_y - ground_top)

        p.setPen(QPen(QColor("#111111"), 1))
        p.setFont(QFont("Arial", 12))
        p.drawText(int(W * 0.62), int(H * 0.18), f"STATE: {self.state}")
        p.drawText(int(W * 0.62), int(H * 0.22), f"Speed: {self.speed:.2f}x")
        p.drawText(int(W * 0.62), int(H * 0.26), f"Depth(px): {depth_px}")

        if depth_px > 0:
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QBrush(QColor(0, 0, 0, 35)))
            p.drawEllipse(bit_x - 10, ground_top - 8, bit_w + 20, 18)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Space Rover Drill GUI - Animation")

        self.anim = DrillAnimationWidget()

        btn_idle = QPushButton("Idle")
        btn_weigh = QPushButton("Weighing")
        btn_drill = QPushButton("Drilling")
        btn_stop = QPushButton("Stop")

        btn_idle.clicked.connect(lambda: self.anim.set_state("IDLE"))
        btn_weigh.clicked.connect(lambda: self.anim.set_state("WEIGHING"))
        btn_drill.clicked.connect(lambda: self.anim.set_state("DRILLING"))

        def stop_toggle():
            self.anim.running = not self.anim.running
            btn_stop.setText("Start" if not self.anim.running else "Stop")

        btn_stop.clicked.connect(stop_toggle)

        speed_label = QLabel("Speed")
        speed_slider = QSlider(Qt.Orientation.Horizontal)
        speed_slider.setMinimum(10)
        speed_slider.setMaximum(300)
        speed_slider.setValue(100)

        speed_slider.valueChanged.connect(lambda v: self.anim.set_speed(v / 100.0))

        root = QVBoxLayout()
        self.setLayout(root)

        root.addWidget(self.anim)

        controls = QHBoxLayout()
        controls.addWidget(btn_idle)
        controls.addWidget(btn_weigh)
        controls.addWidget(btn_drill)
        controls.addWidget(btn_stop)
        controls.addSpacing(20)
        controls.addWidget(speed_label)
        controls.addWidget(speed_slider)

        root.addLayout(controls)

        self.resize(1000, 600)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
