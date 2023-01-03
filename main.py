import os, sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from Models.SessionData import SessionData
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
    Button,
    FilesHeader,
    FilesCombo,
    DirectoryInput,
)

session_data = SessionData()
WINDOW = None

def render_current_toml_data(filename: str):
    _ELEMENTS_PER_COLUMN = 8
    WINDOW.sections['body'].clear_content()
    _current_file_path = f'{session_data.get_parent_directory()}/{filename}'
    session_data.set_toml(
        parse_toml(_current_file_path)
    )
    session_data.set_current_file(_current_file_path)

    session_data.set_patches(
        _generate_patch_toggles(
            data= get_toml_patches(
                toml= session_data.get_toml()
            )
        )
    )
    print('Current session data:', session_data)

    # Place elements in grid (n x 8)
    for index, patch in enumerate(
        session_data.get_patches()
    ):
        _grid_position = reversed(
            divmod(index, _ELEMENTS_PER_COLUMN)
        )

        WINDOW.sections['body'].add_child(
            patch.widget,
            coords= tuple(_grid_position)
        )
    
    print('Loaded toml:', filename)
    print(
        'Parsed data:',
        f'{str(session_data.get_toml())[:24]}...'
    )

def update_patch_directory(header: FilesHeader, directory: str):
    session_data.set_parent_directory(directory)
    session_data.set_current_file(None)
    header.combo.update_data(
        get_toml_files(
            path= session_data.get_parent_directory()
        )
    )
    header.update()

    # Then overwrite saved path
    if os.path.exists('path.txt'):
        with open('path.txt', 'w') as path_file:
            path_file.write(
                f'{session_data.get_parent_directory()}\n'
            )

def _generate_patch_toggles(data) -> tuple:
    stack = []
    for key in data:
        stack.append(
            PatchToggle(data[key])
        )
    return tuple(stack)

def _save_changes_handler():
    if not session_data.current_file:
        return

    saved = save_toml(
        path= session_data.get_current_file(),
        data= session_data.get_toml()
    )

    Dialog(
        title= 'Success',
        body= 'Configuration updated successfully'
    ).show() if saved else Dialog(
        title= 'Error',
        body= 'Configuration couldn\'t be updated',
        icon= 'error'
    ).show()

def _backup_conf_handler():
    if not session_data.current_file:
        return

    backup_path = backup_file(
        filepath= session_data.get_current_file()
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('assets/icon.png'))

    # Get route from file as fallback
    if os.path.exists('path.txt'):
        with open('path.txt', 'r') as path_file:
            line = path_file.readline().strip()
            if line:
                sys.argv.append(line)

    # Exit if there's no directory
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

        sys.exit(0)

    session_data.set_parent_directory(
        os.path.abspath(sys.argv[1])
    )

    files_header = FilesHeader(
        combo= FilesCombo(
            tomls= get_toml_files(
                session_data.get_parent_directory()
            ),
            action= render_current_toml_data
        )
    )

    directory_input = DirectoryInput(
        session_data.get_parent_directory()
    )
    directory_input.set_on_change(
        lambda: update_patch_directory(header= files_header, directory= directory_input.get_directory())
    )

    WINDOW = MainWindow('Xenia Patch Manager')
    WINDOW.sections['header'].add_child(
        directory_input,
        coords= (0,0)
    ).add_child(
        files_header,
        coords= (1,0)
    )

    WINDOW.sections['footer'].add_child(
        Button(
            text= 'Save Changes',
            action= lambda: _save_changes_handler(),
        )
    ).add_child(
        Button(
            text= 'Backup configuration',
            action= lambda: _backup_conf_handler(),
        )
    )

    with open('assets/styles.css', 'r') as stylesheet:
        app.setStyleSheet(stylesheet.read())

    WINDOW.show()
    app.exec()
