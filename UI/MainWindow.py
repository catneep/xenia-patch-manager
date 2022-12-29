from __future__ import annotations
from dataclasses import dataclass, field

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
  QApplication,
  QPushButton,
  QLabel,
  QMainWindow,
  QVBoxLayout,
  QHBoxLayout,
  QGridLayout,
  QWidget,
  QLayout,
  QScrollArea,
)

class WindowSection:
  def __init__(self, name, scroll= False):
    self.name = name
    self._children = []
    self.widget = QScrollArea() if scroll else QWidget()
    self.layout: QLayout = None
    self.rendered: bool = False

  def __repr__(self):
    return f'Section({self.name})<Counts: {len(self._children)}/{self.layout.count() if self.layout != None else -1}, Rendered: {self.rendered}>'

  def _initialize_scrollbar(self):
    # self.widget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    self.widget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
    self.widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.widget.setWidgetResizable(True)

  def set_layout(self, layout: QLayout=  QHBoxLayout()) -> WindowSection:
    self.layout = layout
    self.widget.setLayout(layout)
    if type(self.widget) is QScrollArea:
      self._initialize_scrollbar()
    return self
  
  def add_child(self, widget: QWidget, coords: tuple = None) -> WindowSection:
    self._children.append(widget)
    if coords:
      self.layout.addWidget(widget, coords[0], coords[1])
    else:
      self.layout.addWidget(widget)
    return self.refresh()
  
  def refresh(self) -> WindowSection:
    self.layout.update()
    self.widget.update()
    return self
  
  def toggle_rendered(self) -> bool:
    self.rendered = not self.rendered
    return self.rendered
  
  def clear_content(self) -> WindowSection:
    for i in reversed(range(self.layout.count())):
      item = self.layout.itemAt(i).widget()
      item.setParent(None)
    self._children = []
    return self.refresh()

class MainWindow(QMainWindow):
  def __init__(self, name: str = 'QT Window', width= 600, height= 400):
    super().__init__()
    self.name = name
    self.setWindowTitle(name)
    self.setFixedSize(width, height)

    self.body = QWidget()
    self.body.setLayout(QVBoxLayout())
    self.setCentralWidget(self.body)

    # Declare UI sections
    self._layouts = {
      'header': QGridLayout(),
      'body': QGridLayout(),
      'footer': QHBoxLayout(),
    }
    self.sections = {
      'header': WindowSection('header'),
      'body': WindowSection('body', scroll= True),
      'footer': WindowSection('footer'),
    }

    # Add to window
    for key in self.sections:
      section = self.sections[key]
      section.set_layout(self._layouts[key])

      self.body.layout().addWidget(section.widget)
  
  def refresh(self, section= 'body') -> MainWindow:
    self.sections[section].refresh()
    return self

  def change_UI(self):
    print('Pressed!')
    # self.sections['body'].clear_content()
    self.sections['body'].add_child(
      QLabel('This was added')
    )

if __name__ == "__main__":
  app = QApplication([])
  window = MainWindow()

  button = QPushButton('Button 1')
  button.clicked.connect(window.change_UI)

  window.sections['header'].add_child(
    QLabel('Bruh')
  ).add_child(
    QLabel('1')
  ).add_child(
    QLabel('2')
  )
  # window.sections['body'].add_child(
  #   button
  # )
  for i in range(3):
    for j in range(6):
      window.sections['body'].add_child(
        QLabel(f'label {i},{j}'), (j,i)
      )
  window.sections['footer'].add_child(
    QLabel('My Footer')
  )
  
  window.show()
  app.exec()