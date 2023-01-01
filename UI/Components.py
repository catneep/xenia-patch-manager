from dataclasses import dataclass

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QMessageBox,
    QPushButton,
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
  def __init__(self, text: str, action):
    super().__init__()
    self.clicked.connect(
      lambda: action()
    )
    self.setText(text)
