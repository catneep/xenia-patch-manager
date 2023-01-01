from dataclasses import dataclass

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QMessageBox,
    QPushButton,
    QWidget,
    QComboBox,
    QHBoxLayout,
    QLabel,
)

from Models.Patch import Patch

class PatchToggle:
  def __init__(self, patch: Patch):
    self.patch = patch
    self.widget = QCheckBox(self.patch.data['name'])
    self.widget.setCheckState(
      Qt.CheckState.Checked
      if self.patch.data["is_enabled"]
      else Qt.CheckState.Unchecked
    )
    self.widget.toggled.connect(
      lambda toggle_status: self.patch.toggle_state(
        state= toggle_status
      )
    )

@dataclass(frozen= True, order= False)
class Dialog:
  title: str
  body: str
  icon: str = 'info'

  def _get_icon(self):
    return {
      'info': QMessageBox.Icon.Information,
      'warning': QMessageBox.Icon.Warning,
      'error': QMessageBox.Icon.Critical,
    }[self.icon]

  def show(self):
    dialog = QMessageBox()
    dialog.setIcon(self._get_icon())
    dialog.setWindowTitle(self.title)
    dialog.setText(self.body)
    dialog.exec()

class Button(QPushButton):
  def __init__(self, text: str, action, disabled= False):
    super().__init__()
    self.clicked.connect(
      lambda: action()
    )
    self.setText(text)
    if disabled:
      self.setDisabled(True)

class FilesHeader(QWidget):
  def __init__(self, combo: QComboBox):
    super().__init__()
    layout = QHBoxLayout()
    layout.addWidget(
        QLabel('Game:')
    )
    layout.addWidget(combo)
    layout.addStretch()
    self.setLayout(layout)

class FilesCombo(QComboBox):
  def __init__(self, tomls: tuple, action):
    super().__init__()
    if len(tomls) < 1:
        self.setPlaceholderText('No items found')
        self.setDisabled(True)
        return

    self.setPlaceholderText('Select a file')
    self.addItems(tomls)
    self.currentTextChanged.connect(
        lambda name: action(name)
    )