from dataclasses import dataclass

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QWidget,
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
    self.combo = combo
    self.combo.setFixedWidth(450)
    layout = QHBoxLayout()
    layout.addWidget(
        QLabel('Game:')
    )
    layout.addWidget(self.combo)
    layout.addStretch()
    self.setLayout(layout)

class FilesCombo(QComboBox):
  def __init__(self, tomls: tuple, action):
    super().__init__()
    self.update_data(tomls)
    self.currentTextChanged.connect(
        lambda name: action(name)
    )

  def update_data(self, tomls):
    print('Updating combo...')
    print(f'Rendering {len(tomls)} tomls in combo')
    self.clear()
    if len(tomls) < 1:
        self.setPlaceholderText('No items found')
        self.setDisabled(True)
        return

    self.setPlaceholderText('Select a file')
    self.addItems(tomls)
    self.setDisabled(False)

class FileBrowser(QFileDialog):
  def __init__(self,):
    super().__init__()
    self.setFileMode(QFileDialog.FileMode.Directory)

class DirectoryInput(QWidget):
  def __init__(self, directory):
    super().__init__()
    self.directory = directory
    self._txt_edit = QLineEdit()
    self._txt_edit.setEnabled(False)
    self._txt_edit.setText(directory)
    btn = QPushButton('Browse')
    btn.clicked.connect(
      lambda: self._browse()
    )

    layout = QHBoxLayout()
    layout.addWidget(
        QLabel('Root directory:')
    )
    layout.addWidget(
      self._txt_edit
    )
    layout.addWidget(
      btn
    )
    self.setLayout(layout)
    self.on_change = None

  def _browse(self):
    browser = FileBrowser()
    if (browser.exec()):
      files = browser.selectedFiles()
      if len(files) < 1:
        return
      
      # Get first directory selected
      self.set_directory(files[0])
      if self.on_change:
        self.on_change()

      print(
        "Selected:",
        browser.selectedFiles()
      )

  def set_directory(self, directory: str):
    print("Directory changed:", directory)
    self.directory = directory
    self._txt_edit.setText(directory)

  def get_directory(self) -> str:
    return self.directory.replace('\\','/')
  
  def set_on_change(self, action):
    self.on_change = action
