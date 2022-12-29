import os, sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QLineEdit,
    QHBoxLayout,
    QMessageBox,
    QLabel,
    QWidget,
    QComboBox,
    QPushButton,
)

from Models.Data import SessionData
from Data.Input import (
    backup_file,
    get_toml_files,
    get_toml_patches,
    parse_toml,
    save_toml,
)
from UI.MainWindow import MainWindow
from UI.Components import (
    Dialog,
    PatchToggle,
)

def generate_file_combo(files: tuple) -> QComboBox:
    combo = QComboBox()
    if len(files) < 1:
        combo.setPlaceholderText('No items found')
        combo.setDisabled(True)
        return combo

    combo.setPlaceholderText('Select a file')
    combo.addItems(files)
    combo.currentTextChanged.connect(
        lambda name: render_current_toml_data(filename= name)
    )
    return combo

current_toml = SessionData()
PATCHES: tuple = None
WINDOW = None
FILE_PATH = ""

def render_current_toml_data(filename: str):
    _ELEMENTS_PER_COLUMN = 8
    WINDOW.sections['body'].clear_content()
    current_toml.set_toml(
        parse_toml(f'{FILE_PATH}/{filename}')
    )
    current_toml.set_filepath(f'{FILE_PATH}/{filename}')

    PATCHES = generate_patch_toggles(
        data= get_toml_patches(
            toml= current_toml.get_toml()
        )
    )

    # Place elements in grid (n x 8)
    for index, patch in enumerate(PATCHES):
        _grid_position = reversed(divmod(index, _ELEMENTS_PER_COLUMN))

        WINDOW.sections['body'].add_child(
            patch.widget,
            coords= tuple(_grid_position)
        )
    
    print('Loaded toml:', filename)
    print('Parsed data:', f'{str(current_toml.get_toml())[:24]}...')

def generate_patch_toggles(data) -> tuple:
    stack = []
    for key in data:
        stack.append(
            PatchToggle(data[key])
        )
    return tuple(stack)

def generate_save_button() -> QPushButton:
    def _handle_save():
        saved = save_toml(
            path= current_toml.get_filepath(),
            data= current_toml.get_toml()
        )

        Dialog(
            title= 'Success',
            body= 'Configuration updated successfully'
        ).show() if saved else Dialog(
            title= 'Error',
            body= 'Configuration couldn\'t be updated',
            icon= 'error'
        ).show()
        

    btn = QPushButton('Save Changes')
    btn.clicked.connect(
        lambda: _handle_save()
    )
    return btn

def generate_path_header() -> QWidget:
    txt = QLineEdit()
    scan_directory = lambda: print('Scanning path:', txt.text())

    btn = QPushButton('Scan directory')
    btn.clicked.connect(
        scan_directory
    )

    widget = QWidget()
    widget.setLayout(QHBoxLayout())
    widget.layout().addWidget(
        QLabel('Search path:')
    )
    widget.layout().addWidget(
        txt
    )
    widget.layout().addWidget(
        btn
    )

    return widget

def generate_file_header(tomls: tuple) -> QWidget:
    layout = QHBoxLayout()
    layout.addWidget(
        QLabel('Game:')
    )
    layout.addWidget(
        generate_file_combo(tomls)
    )
    layout.addStretch()

    widget = QWidget()
    widget.setLayout(layout)
    return widget

def generate_backup_button() -> QPushButton:
    def _handle_backup():
        backup_path = backup_file(
            filepath= current_toml.get_filepath()
        )
        if not backup_path:
            Dialog(
                title= 'Error',
                body= "Backup couldn't be created",
                icon= 'error'
            ).show()
            return

        Dialog(
            title= 'Success',
            body= f'Backup created at {backup_path}'
        ).show()

    btn = QPushButton('Backup configuration')
    btn.clicked.connect(
        lambda: _handle_backup()
    )
    return btn

def show_success_dialog():
    dialog = QMessageBox()
    dialog.setWindowTitle("Success")
    dialog.setText("Patch configuration was updated")
    dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('assets/icon.png'))

    # Get route from file as fallback
    if os.path.exists('path'):
        with open('path', 'r') as path_file:
            line = path_file.readline().strip()
            print('line', line)
            if line:
                sys.argv.append(line)

    if (
        (len(sys.argv) < 2) or
        not (os.path.exists(sys.argv[1]))
    ):
        print(sys.argv)
        Dialog(
            title= 'Error',
            body= 'Invalid directory provided',
            icon= 'error'
        ).show()

        exit(0)

    FILE_PATH = sys.argv[1]
    WINDOW = MainWindow('Xenia Patch Manager')
    WINDOW.sections['header'].add_child(
         generate_file_header(
            tomls= get_toml_files(FILE_PATH)
        ), coords= (0,0)
    )

    WINDOW.sections['footer'].add_child(
        generate_save_button()
    ).add_child(
        generate_backup_button()
    )

    WINDOW.show()
    app.exec()
