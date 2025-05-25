import sys
from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QComboBox, QCheckBox,
    QSpinBox, QDoubleSpinBox, QColorDialog, QLabel, QGridLayout
)
from PyQt6.QtGui import QColor, QIcon, QPixmap
from PyQt6.QtCore import QSize

class ColorButton(QPushButton):
    def __init__(self, label, default_color=QColor(255,255,255)):
        super().__init__(label)
        self.color = default_color
        self.setFixedSize(120, 30)
        self._update_style()
        self.clicked.connect(self.choose)

    def _update_style(self):
        pix = QPixmap(16, 16)
        pix.fill(self.color)
        self.setIcon(QIcon(pix))
        self.setIconSize(QSize(16, 16))

    def choose(self):
        col = QColorDialog.getColor(self.color)
        if col.isValid():
            self.color = col
            self._update_style()

class PlanetDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Planet..." )
        self.setMinimumSize(600, 400)
        self.code_result = None
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        grid = QGridLayout()

        grid.addWidget(QLabel("Name:"), 0, 0)
        self.name_input = QLineEdit(); self.name_input.setPlaceholderText("erekir")
        grid.addWidget(self.name_input, 0, 1)
        grid.addWidget(QLabel("Parent:"), 0, 2)
        self.parent_input = QLineEdit(); self.parent_input.setPlaceholderText("sun or null")
        grid.addWidget(self.parent_input, 0, 3)

        grid.addWidget(QLabel("Radius:"), 1, 0)
        self.radius_input = QDoubleSpinBox(); self.radius_input.setRange(0.0, 100.0); self.radius_input.setSingleStep(0.1)
        grid.addWidget(self.radius_input, 1, 1)
        grid.addWidget(QLabel("Sector Grid:"), 1, 2)
        self.sector_input = QSpinBox(); self.sector_input.setRange(0, 20)
        grid.addWidget(self.sector_input, 1, 3)

        grid.addWidget(QLabel("Orbit Spacing:"), 2, 0)
        self.orbit_input = QDoubleSpinBox(); self.orbit_input.setRange(0.0, 50.0); self.orbit_input.setSingleStep(0.1)
        grid.addWidget(self.orbit_input, 2, 1)
        grid.addWidget(QLabel("Start Sector:"), 2, 2)
        self.start_input = QSpinBox(); self.start_input.setRange(0, 1000)
        grid.addWidget(self.start_input, 2, 3)

        self.accessible_cb = QCheckBox("Accessible")
        self.hasAtmos_cb   = QCheckBox("Has Atmosphere")
        self.bloom_cb      = QCheckBox("Bloom")
        self.visible_cb    = QCheckBox("Visible")
        self.tidalLock_cb  = QCheckBox("Tidal Lock")
        grid.addWidget(self.accessible_cb, 3, 0)
        grid.addWidget(self.hasAtmos_cb,   3, 1)
        grid.addWidget(self.bloom_cb,      3, 2)
        grid.addWidget(self.visible_cb,    3, 3)
        grid.addWidget(self.tidalLock_cb,  4, 0)

        grid.addWidget(QLabel("Default Env:"), 5, 0)
        self.env_combo = QComboBox(); self.env_combo.addItems(["none","terrestrial","underwater","scorching","space"])
        grid.addWidget(self.env_combo, 5, 1)

        self.atmos_btn = ColorButton("Atmosphere", QColor(48,180,153))
        self.icon_btn  = ColorButton("Icon",       QColor(255,146,102))
        self.land_btn  = ColorButton("LandCloud",  QColor(237,101,66))
        grid.addWidget(QLabel("Atmos Color:"), 6, 0); grid.addWidget(self.atmos_btn, 6, 1)
        grid.addWidget(QLabel("Icon Color:"),   7, 0); grid.addWidget(self.icon_btn,  7, 1)
        grid.addWidget(QLabel("LandCloud Color:"),8, 0); grid.addWidget(self.land_btn,  8, 1)

        layout.addLayout(grid)

        btn_layout = QVBoxLayout()
        self.create_btn = QPushButton("Create")
        self.create_btn.clicked.connect(self._on_create)
        btn_layout.addWidget(self.create_btn)
        layout.addLayout(btn_layout)

    def _on_create(self):
        nm = self.name_input.text() or "planet"
        pr = self.parent_input.text() or 'null'
        code = [f"{nm} = new Planet(\"{nm}\", {pr}, {self.radius_input.value()}f{(f', {self.sector_input.value()}' if self.sector_input.value()>0 else '')}){{"]
        for attr, cb in [("accessible",self.accessible_cb),("hasAtmosphere",self.hasAtmos_cb),
                         ("bloom",self.bloom_cb),("visible",self.visible_cb),("tidalLock",self.tidalLock_cb)]:
            if cb.isChecked(): code.append(f"    {attr} = true;")
        env = self.env_combo.currentText().upper()
        code.append(f"    defaultEnv = Env.{env};")
        code.append(f"    orbitSpacing = {self.orbit_input.value()}f;")
        code.append(f"    startSector = {self.start_input.value()};")
        for name, btn in [("atmosphereColor",self.atmos_btn),("iconColor",self.icon_btn),("landCloudColor",self.land_btn)]:
            hex = btn.color.name().upper()[1:]
            code.append(f"    {name} = Color.valueOf(\"{hex}\");")
        code.append("};")

        self.code_result = "\n".join(code)
        self.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = PlanetDialog()
    if dlg.exec():
        print(dlg.code_result)
    sys.exit()
