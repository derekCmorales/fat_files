import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                             QTextEdit, QListWidget, QMessageBox, QDialog,
                             QFormLayout, QCheckBox, QTabWidget, QScrollArea,
                             QFrame, QComboBox)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPalette, QColor
from fat_system import FATSystem

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.fat_system = FATSystem()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Sistema FAT - Inicio de Sesión")
        self.setFixedSize(500, 450)
        self.setStyleSheet("background-color: white;")
        
        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # Título
        title = QLabel("Sistema FAT")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)
        
        subtitle = QLabel("Gestión de Archivos By Derek Calderón")
        subtitle.setFont(QFont("Arial", 14))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #7f8c8d;")
        layout.addWidget(subtitle)
        
        layout.addSpacing(30)
        
        # Usuario
        user_label = QLabel("Usuario:")
        user_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        user_label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(user_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Ingrese su usuario")
        self.username_input.setFixedHeight(50)
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 15px;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                font-size: 16px;
                color: #2c3e50;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        layout.addWidget(self.username_input)
        
        layout.addSpacing(15)
        
        # Contraseña
        pass_label = QLabel("Contraseña:")
        pass_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        pass_label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(pass_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Ingrese su contraseña")
        self.password_input.setFixedHeight(50)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(self.username_input.styleSheet())
        self.password_input.returnPressed.connect(self.login)
        layout.addWidget(self.password_input)
        
        layout.addSpacing(20)
        
        # Botón de login
        login_btn = QPushButton("Iniciar Sesión")
        login_btn.setFixedHeight(50)
        login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        login_btn.clicked.connect(self.login)
        layout.addWidget(login_btn)
        
        # Nota de admin
        note = QLabel("Usuario admin: admin / admin123")
        note.setFont(QFont("Arial", 11))
        note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        note.setStyleSheet("color: #95a5a6; margin-top: 15px;")
        layout.addWidget(note)
        
        self.setLayout(layout)
    
    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Por favor ingrese usuario y contraseña")
            return
        
        if self.fat_system.login(username, password):
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Usuario o contraseña incorrectos")
            self.password_input.clear()

class MainWindow(QMainWindow):
    def __init__(self, fat_system):
        super().__init__()
        self.fat_system = fat_system
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Sistema FAT - Gestión de Archivos")
        self.setMinimumSize(1000, 700)
        self.setStyleSheet("background-color: white;")
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #ecf0f1;
                color: #2c3e50;
                padding: 12px 24px;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #3498db;
                color: white;
            }
            QTabBar::tab:hover:!selected {
                background-color: #d5dbdb;
            }
        """)
        
        # Tabs de contenido
        self.tabs.addTab(self.create_files_tab(), "Archivos")
        self.tabs.addTab(self.create_trash_tab(), "Papelera")
        
        if self.fat_system.current_user.get("is_admin"):
            self.tabs.addTab(self.create_users_tab(), "Usuarios")
        
        main_layout.addWidget(self.tabs)
        
        central_widget.setLayout(main_layout)
        
    def create_header(self):
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                padding: 15px;
            }
        """)
        
        layout = QHBoxLayout()
        
        title = QLabel("Sistema FAT")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        layout.addWidget(title)
        
        layout.addStretch()
        
        user_label = QLabel(f"Usuario: {self.fat_system.current_user['username']}")
        user_label.setFont(QFont("Arial", 12))
        user_label.setStyleSheet("color: white;")
        layout.addWidget(user_label)
        
        logout_btn = QPushButton("Cerrar Sesión")
        logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)
        
        header.setLayout(layout)
        return header
    
    def create_files_tab(self):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Panel izquierdo - Lista de archivos
        left_panel = QFrame()
        left_panel.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        left_layout = QVBoxLayout()
        
        left_header = QLabel("Mis Archivos")
        left_header.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        left_header.setStyleSheet("color: #2c3e50;")
        left_layout.addWidget(left_header)
        
        self.files_list = QListWidget()
        self.files_list.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                padding: 5px;
                font-size: 13px;
                color: #2c3e50;
            }
            QListWidget::item {
                padding: 10px;
                border-radius: 3px;
                color: #2c3e50;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QListWidget::item:hover:!selected {
                background-color: #ecf0f1;
            }
        """)
        self.files_list.itemClicked.connect(self.show_file_details)
        left_layout.addWidget(self.files_list)
        
        # Botones de acción
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(10)
        
        create_btn = self.create_action_button("Crear Archivo", "#27ae60")
        create_btn.clicked.connect(self.create_file)
        btn_layout.addWidget(create_btn)
        
        open_btn = self.create_action_button("Abrir", "#3498db")
        open_btn.clicked.connect(self.open_file)
        btn_layout.addWidget(open_btn)
        
        modify_btn = self.create_action_button("Modificar", "#f39c12")
        modify_btn.clicked.connect(self.modify_file)
        btn_layout.addWidget(modify_btn)
        
        delete_btn = self.create_action_button("Eliminar", "#e74c3c")
        delete_btn.clicked.connect(self.delete_file)
        btn_layout.addWidget(delete_btn)
        
        perms_btn = self.create_action_button("Permisos", "#9b59b6")
        perms_btn.clicked.connect(self.manage_permissions)
        btn_layout.addWidget(perms_btn)
        
        refresh_btn = self.create_action_button("Actualizar", "#34495e")
        refresh_btn.clicked.connect(self.refresh_files_list)
        btn_layout.addWidget(refresh_btn)
        
        left_layout.addLayout(btn_layout)
        left_panel.setLayout(left_layout)
        
        # Panel derecho - Detalles
        right_panel = QFrame()
        right_panel.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        right_layout = QVBoxLayout()
        
        right_header = QLabel("Detalles del Archivo")
        right_header.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        right_header.setStyleSheet("color: #2c3e50;")
        right_layout.addWidget(right_header)
        
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                padding: 10px;
                font-size: 13px;
                color: #2c3e50;
            }
        """)
        right_layout.addWidget(self.details_text)
        
        right_panel.setLayout(right_layout)
        
        layout.addWidget(left_panel, 1)
        layout.addWidget(right_panel, 2)
        
        widget.setLayout(layout)
        self.refresh_files_list()
        return widget
    
    def create_trash_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        header = QLabel("Papelera de Reciclaje")
        header.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header.setStyleSheet("color: #2c3e50;")
        layout.addWidget(header)
        
        self.trash_list = QListWidget()
        self.trash_list.setStyleSheet(self.files_list.styleSheet())
        layout.addWidget(self.trash_list)
        
        btn_layout = QHBoxLayout()
        
        recover_btn = self.create_action_button("Recuperar", "#27ae60")
        recover_btn.clicked.connect(self.recover_file)
        btn_layout.addWidget(recover_btn)
        
        refresh_trash_btn = self.create_action_button("Actualizar", "#34495e")
        refresh_trash_btn.clicked.connect(self.refresh_trash_list)
        btn_layout.addWidget(refresh_trash_btn)
        
        layout.addLayout(btn_layout)
        
        widget.setLayout(layout)
        self.refresh_trash_list()
        return widget
    
    def create_users_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        header = QLabel("Gestión de Usuarios")
        header.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header.setStyleSheet("color: #2c3e50;")
        layout.addWidget(header)
        
        self.users_list = QListWidget()
        self.users_list.setStyleSheet(self.files_list.styleSheet())
        layout.addWidget(self.users_list)
        
        btn_layout = QHBoxLayout()
        
        create_user_btn = self.create_action_button("Crear Usuario", "#27ae60")
        create_user_btn.clicked.connect(self.create_user)
        btn_layout.addWidget(create_user_btn)
        
        delete_user_btn = self.create_action_button("Eliminar Usuario", "#e74c3c")
        delete_user_btn.clicked.connect(self.delete_user)
        btn_layout.addWidget(delete_user_btn)
        
        refresh_users_btn = self.create_action_button("Actualizar", "#34495e")
        refresh_users_btn.clicked.connect(self.refresh_users_list)
        btn_layout.addWidget(refresh_users_btn)
        
        layout.addLayout(btn_layout)
        
        widget.setLayout(layout)
        self.refresh_users_list()
        return widget
    
    def create_action_button(self, text, color):
        btn = QPushButton(text)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 13px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                opacity: 0.9;
                background-color: {color};
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(color)};
            }}
        """)
        return btn
    
    def darken_color(self, hex_color):
        """Oscurecer un color hex"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = max(0, int(r * 0.8))
        g = max(0, int(g * 0.8))
        b = max(0, int(b * 0.8))
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def refresh_files_list(self):
        self.files_list.clear()
        files = self.fat_system.list_files(include_deleted=False)
        for file in files:
            self.files_list.addItem(file['nombre'])
    
    def refresh_trash_list(self):
        self.trash_list.clear()
        files = self.fat_system.list_files(include_deleted=True)
        for file in files:
            self.trash_list.addItem(file['nombre'])
    
    def refresh_users_list(self):
        if not hasattr(self, 'users_list'):
            return
        self.users_list.clear()
        users = self.fat_system.get_all_users()
        for user in users:
            role = "Admin" if user.get("is_admin") else "Usuario"
            self.users_list.addItem(f"{user['username']} - {role}")
    
    def show_file_details(self, item):
        filename = item.text()
        metadata = self.fat_system.get_file_metadata(filename)
        
        if not metadata:
            self.details_text.setText("No se pudo cargar información del archivo")
            return
        
        details = f"""
<h3 style='color: #2c3e50;'>{metadata['nombre']}</h3>
<hr>
<p style='color: #2c3e50;'><b>Propietario:</b> {metadata['owner']}</p>
<p style='color: #2c3e50;'><b>Tamaño:</b> {metadata['total_caracteres']} caracteres</p>
<p style='color: #2c3e50;'><b>Creado:</b> {metadata['fecha_creacion'][:19].replace('T', ' ')}</p>
<p style='color: #2c3e50;'><b>Modificado:</b> {metadata['fecha_modificacion'][:19].replace('T', ' ')}</p>
<p style='color: #2c3e50;'><b>En papelera:</b> {'Sí' if metadata['papelera'] else 'No'}</p>

<h4 style='color: #2c3e50; margin-top: 20px;'>Permisos</h4>
<hr>
"""
        
        if metadata['permisos']:
            for user, perms in metadata['permisos'].items():
                lectura = "Si" if perms.get('lectura') else "No"
                escritura = "Si" if perms.get('escritura') else "No"
                details += f"<p style='color: #2c3e50;'><b>{user}:</b> Lectura: {lectura} | Escritura: {escritura}</p>"
        else:
            details += "<p style='color: #7f8c8d;'><i>Sin permisos asignados a otros usuarios</i></p>"
        
        self.details_text.setHtml(details)
    
    def create_file(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Crear Nuevo Archivo")
        dialog.setFixedSize(500, 450)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: #2c3e50;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Crear Nuevo Archivo")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)
        
        name_label = QLabel("Nombre del archivo:")
        name_label.setStyleSheet("color: #2c3e50; font-weight: bold;")
        layout.addWidget(name_label)
        
        name_input = QLineEdit()
        name_input.setPlaceholderText("nombre_archivo.txt")
        name_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 13px;
                color: #2c3e50;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        layout.addWidget(name_input)
        
        content_label = QLabel("Contenido:")
        content_label.setStyleSheet("color: #2c3e50; font-weight: bold;")
        layout.addWidget(content_label)
        
        content_input = QTextEdit()
        content_input.setPlaceholderText("Contenido del archivo...")
        content_input.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 13px;
                color: #2c3e50;
                background-color: white;
            }
            QTextEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        layout.addWidget(content_input)
        
        btn_layout = QHBoxLayout()
        
        create_btn = self.create_action_button("Crear", "#27ae60")
        create_btn.clicked.connect(lambda: self.do_create_file(dialog, name_input.text(), content_input.toPlainText()))
        btn_layout.addWidget(create_btn)
        
        cancel_btn = self.create_action_button("Cancelar", "#95a5a6")
        cancel_btn.clicked.connect(dialog.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def do_create_file(self, dialog, filename, content):
        if not filename:
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Por favor ingrese un nombre de archivo")
            msg.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
            msg.exec()
            return
        
        if self.fat_system.create_file(filename, content):
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Éxito")
            msg.setText(f"Archivo '{filename}' creado correctamente")
            msg.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
            msg.exec()
            self.refresh_files_list()
            dialog.accept()
        else:
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText("No se pudo crear el archivo. Puede que ya exista.")
            msg.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
            msg.exec()
    
    def open_file(self):
        current_item = self.files_list.currentItem()
        if not current_item:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Advertencia")
            msg.setText("Por favor seleccione un archivo")
            msg.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
            msg.exec()
            return
        
        filename = current_item.text()
        content = self.fat_system.get_file_content(filename)
        
        if content is None:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText("No tiene permisos para leer este archivo")
            msg.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
            msg.exec()
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Archivo: {filename}")
        dialog.setFixedSize(600, 500)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: #2c3e50;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel(f"Archivo: {filename}")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)
        
        content_text = QTextEdit()
        content_text.setPlainText(content)
        content_text.setReadOnly(True)
        content_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Courier New';
                font-size: 12px;
                color: #2c3e50;
            }
        """)
        layout.addWidget(content_text)
        
        close_btn = self.create_action_button("Cerrar", "#3498db")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def modify_file(self):
        current_item = self.files_list.currentItem()
        if not current_item:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Advertencia")
            msg.setText("Por favor seleccione un archivo")
            msg.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
            msg.exec()
            return
        
        filename = current_item.text()
        
        # Verificar permisos de escritura ANTES de abrir el diálogo
        metadata = self.fat_system.get_file_metadata(filename)
        if not metadata:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText("No se pudo acceder al archivo")
            msg.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
            msg.exec()
            return
        
        # Verificar si tiene permisos de escritura
        if metadata['owner'] != self.fat_system.current_user['username']:
            if not self.fat_system.current_user.get('is_admin'):
                user_perms = metadata['permisos'].get(self.fat_system.current_user['username'], {})
                if not user_perms.get('escritura', False):
                    msg = QMessageBox(self)
                    msg.setIcon(QMessageBox.Icon.Critical)
                    msg.setWindowTitle("Error")
                    msg.setText("No tiene permisos de escritura para este archivo")
                    msg.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
                    msg.exec()
                    return
        
        current_content = self.fat_system.get_file_content(filename)
        
        if current_content is None:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText("No tiene permisos para leer este archivo")
            msg.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
            msg.exec()
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Modificar: {filename}")
        dialog.setFixedSize(600, 500)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: #2c3e50;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel(f"Modificar: {filename}")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)
        
        info = QLabel("Contenido actual:")
        info.setStyleSheet("color: #7f8c8d;")
        layout.addWidget(info)
        
        content_input = QTextEdit()
        content_input.setPlainText(current_content)
        content_input.setStyleSheet("""
            QTextEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-family: 'Courier New';
                font-size: 12px;
                color: #2c3e50;
                background-color: white;
            }
            QTextEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        layout.addWidget(content_input)
        
        btn_layout = QHBoxLayout()
        
        save_btn = self.create_action_button("Guardar", "#27ae60")
        save_btn.clicked.connect(lambda: self.do_modify_file(dialog, filename, content_input.toPlainText()))
        btn_layout.addWidget(save_btn)
        
        cancel_btn = self.create_action_button("Cancelar", "#95a5a6")
        cancel_btn.clicked.connect(dialog.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def do_modify_file(self, dialog, filename, new_content):
        if self.fat_system.modify_file(filename, new_content):
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Éxito")
            msg.setText(f"Archivo '{filename}' modificado correctamente")
            msg.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
            msg.exec()
            self.refresh_files_list()
            dialog.accept()
        else:
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText("No tiene permisos para modificar este archivo")
            msg.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
            msg.exec()
    
    def delete_file(self):
        current_item = self.files_list.currentItem()
        if not current_item:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Advertencia")
            msg.setText("Por favor seleccione un archivo")
            msg.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
            msg.exec()
            return
        
        filename = current_item.text()
        
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle("Confirmar")
        msg.setText(f"¿Está seguro de eliminar '{filename}'?\nSe moverá a la papelera.")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
        reply = msg.exec()
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.fat_system.delete_file(filename):
                msg2 = QMessageBox(self)
                msg2.setIcon(QMessageBox.Icon.Information)
                msg2.setWindowTitle("Éxito")
                msg2.setText(f"Archivo '{filename}' movido a la papelera")
                msg2.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
                msg2.exec()
                self.refresh_files_list()
                self.details_text.clear()
            else:
                msg2 = QMessageBox(self)
                msg2.setIcon(QMessageBox.Icon.Critical)
                msg2.setWindowTitle("Error")
                msg2.setText("No tiene permisos para eliminar este archivo")
                msg2.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
                msg2.exec()
    
    def recover_file(self):
        current_item = self.trash_list.currentItem()
        if not current_item:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Advertencia")
            msg.setText("Por favor seleccione un archivo de la papelera")
            msg.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
            msg.exec()
            return
        
        filename = current_item.text()
        
        if self.fat_system.recover_file(filename):
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Éxito")
            msg.setText(f"Archivo '{filename}' recuperado correctamente")
            msg.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
            msg.exec()
            self.refresh_trash_list()
            self.refresh_files_list()
        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText("No tiene permisos para recuperar este archivo")
            msg.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
            msg.exec()
    
    def manage_permissions(self):
        current_item = self.files_list.currentItem()
        if not current_item:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Advertencia")
            msg.setText("Por favor seleccione un archivo")
            msg.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
            msg.exec()
            return
        
        filename = current_item.text()
        metadata = self.fat_system.get_file_metadata(filename)
        
        if metadata['owner'] != self.fat_system.current_user['username']:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText("Solo el propietario puede gestionar permisos")
            msg.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
            msg.exec()
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Permisos: {filename}")
        dialog.setFixedSize(450, 500)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: #2c3e50;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QLabel(f"Gestionar Permisos: {filename}")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)
        
        user_label = QLabel("Seleccionar usuario:")
        user_label.setStyleSheet("color: #2c3e50; font-weight: bold;")
        layout.addWidget(user_label)
        
        users = self.fat_system.get_all_users()
        user_combo = QComboBox()
        for user in users:
            if user['username'] != self.fat_system.current_user['username']:
                user_combo.addItem(user['username'])
        
        user_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 13px;
                color: #2c3e50;
                background-color: white;
            }
        """)
        layout.addWidget(user_combo)
        
        layout.addSpacing(10)
        
        perms_label = QLabel("Permisos:")
        perms_label.setStyleSheet("color: #2c3e50; font-weight: bold;")
        layout.addWidget(perms_label)
        
        read_check = QCheckBox("Lectura")
        write_check = QCheckBox("Escritura")
        
        read_check.setStyleSheet("font-size: 13px; color: #2c3e50;")
        write_check.setStyleSheet("font-size: 13px; color: #2c3e50;")
        
        layout.addWidget(read_check)
        layout.addWidget(write_check)
        
        layout.addSpacing(15)
        
        btn_layout = QHBoxLayout()
        
        apply_btn = self.create_action_button("Aplicar", "#27ae60")
        apply_btn.clicked.connect(lambda: self.do_set_permissions(
            dialog, filename, user_combo.currentText(), 
            read_check.isChecked(), write_check.isChecked()))
        btn_layout.addWidget(apply_btn)
        
        close_btn = self.create_action_button("Cerrar", "#95a5a6")
        close_btn.clicked.connect(dialog.reject)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
        
        # Mostrar permisos actuales
        current_perms = QLabel("Permisos actuales:")
        current_perms.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        current_perms.setStyleSheet("color: #2c3e50; margin-top: 10px;")
        layout.addWidget(current_perms)
        
        perms_text = QTextEdit()
        perms_text.setReadOnly(True)
        perms_text.setMaximumHeight(100)
        perms_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                padding: 8px;
                font-size: 12px;
                color: #2c3e50;
            }
        """)
        
        perms_html = ""
        if metadata['permisos']:
            for user, perms in metadata['permisos'].items():
                lectura = "Si" if perms.get('lectura') else "No"
                escritura = "Si" if perms.get('escritura') else "No"
                perms_html += f"<p style='color: #2c3e50;'><b>{user}:</b> Lectura: {lectura} | Escritura: {escritura}</p>"
        else:
            perms_html = "<p style='color: #7f8c8d;'><i>Sin permisos asignados</i></p>"
        
        perms_text.setHtml(perms_html)
        layout.addWidget(perms_text)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def do_set_permissions(self, dialog, filename, username, read, write):
        if not username:
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Error")
            msg.setText("No hay usuarios disponibles")
            msg.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
            msg.exec()
            return
        
        success = True
        success &= self.fat_system.set_permission(filename, username, "lectura", read)
        success &= self.fat_system.set_permission(filename, username, "escritura", write)
        
        if success:
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Éxito")
            msg.setText(f"Permisos actualizados para {username}")
            msg.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
            msg.exec()
            self.show_file_details(self.files_list.currentItem())
        else:
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText("No se pudieron actualizar los permisos")
            msg.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
            msg.exec()
    
    def create_user(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Crear Usuario")
        dialog.setFixedSize(450, 400)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: #2c3e50;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QLabel("Crear Nuevo Usuario")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)
        
        layout.addSpacing(10)
        
        username_label = QLabel("Nombre de usuario:")
        username_label.setStyleSheet("color: #2c3e50; font-weight: bold;")
        layout.addWidget(username_label)
        
        username_input = QLineEdit()
        username_input.setPlaceholderText("nombre_usuario")
        username_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 13px;
                color: #2c3e50;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        layout.addWidget(username_input)
        
        layout.addSpacing(10)
        
        password_label = QLabel("Contraseña:")
        password_label.setStyleSheet("color: #2c3e50; font-weight: bold;")
        layout.addWidget(password_label)
        
        password_input = QLineEdit()
        password_input.setPlaceholderText("contraseña")
        password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_input.setStyleSheet(username_input.styleSheet())
        layout.addWidget(password_input)
        
        layout.addSpacing(15)
        
        admin_check = QCheckBox("Usuario administrador")
        admin_check.setStyleSheet("font-size: 13px; color: #2c3e50;")
        layout.addWidget(admin_check)
        
        layout.addSpacing(20)
        
        btn_layout = QHBoxLayout()
        
        create_btn = self.create_action_button("Crear", "#27ae60")
        create_btn.clicked.connect(lambda: self.do_create_user(
            dialog, username_input.text(), password_input.text(), admin_check.isChecked()))
        btn_layout.addWidget(create_btn)
        
        cancel_btn = self.create_action_button("Cancelar", "#95a5a6")
        cancel_btn.clicked.connect(dialog.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def do_create_user(self, dialog, username, password, is_admin):
        if not username or not password:
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Por favor complete todos los campos")
            msg.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
            msg.exec()
            return
        
        if self.fat_system.create_user(username, password, is_admin):
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Éxito")
            msg.setText(f"Usuario '{username}' creado correctamente")
            msg.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
            msg.exec()
            self.refresh_users_list()
            dialog.accept()
        else:
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText("No se pudo crear el usuario. Puede que ya exista.")
            msg.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
            msg.exec()
    
    def delete_user(self):
        current_item = self.users_list.currentItem()
        if not current_item:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Advertencia")
            msg.setText("Por favor seleccione un usuario")
            msg.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
            msg.exec()
            return
        
        username = current_item.text().split(" - ")[0]
        
        if username == "admin":
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText("No se puede eliminar al administrador")
            msg.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
            msg.exec()
            return
        
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle("Confirmar")
        msg.setText(f"¿Está seguro de eliminar al usuario '{username}'?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
        reply = msg.exec()
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.fat_system.delete_user(username):
                msg2 = QMessageBox(self)
                msg2.setIcon(QMessageBox.Icon.Information)
                msg2.setWindowTitle("Éxito")
                msg2.setText(f"Usuario '{username}' eliminado correctamente")
                msg2.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
                msg2.exec()
                self.refresh_users_list()
            else:
                msg2 = QMessageBox(self)
                msg2.setIcon(QMessageBox.Icon.Critical)
                msg2.setWindowTitle("Error")
                msg2.setText("No se pudo eliminar el usuario")
                msg2.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
                msg2.exec()
    
    def logout(self):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle("Cerrar Sesión")
        msg.setText("¿Está seguro de cerrar sesión?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setStyleSheet("QLabel{color: #2c3e50;} QPushButton{min-width: 80px;}")
        reply = msg.exec()
        
        if reply == QMessageBox.StandardButton.Yes:
            self.fat_system.logout()
            self.close()
            login_window = LoginWindow()
            if login_window.exec() == QDialog.DialogCode.Accepted:
                main_window = MainWindow(login_window.fat_system)
                main_window.show()

def main():
    app = QApplication(sys.argv)
    
    # Configurar fuente global
    app.setFont(QFont("Arial", 10))
    
    # Configurar estilo para QMessageBox
    app.setStyleSheet("""
        QMessageBox {
            background-color: white;
        }
        QMessageBox QLabel {
            color: #2c3e50;
        }
        QMessageBox QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 8px 16px;
            font-weight: bold;
            min-width: 80px;
        }
        QMessageBox QPushButton:hover {
            background-color: #2980b9;
        }
    """)
    
    login_window = LoginWindow()
    
    if login_window.exec() == QDialog.DialogCode.Accepted:
        main_window = MainWindow(login_window.fat_system)
        main_window.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    main()