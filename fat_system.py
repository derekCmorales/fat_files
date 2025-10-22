import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class FATSystem:
    def __init__(self, base_dir="fat_storage"):
        self.base_dir = base_dir
        self.fat_table_file = os.path.join(base_dir, "fat_table.json")
        self.users_file = os.path.join(base_dir, "users.json")
        self.blocks_dir = os.path.join(base_dir, "blocks")
        self.current_user = None
        self._initialize_storage()
    
    def _initialize_storage(self):
        """Inicializa la estructura de almacenamiento"""
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self.blocks_dir, exist_ok=True)
        
        # Inicializar tabla FAT
        if not os.path.exists(self.fat_table_file):
            with open(self.fat_table_file, 'w') as f:
                json.dump([], f)
        
        # Inicializar usuarios con admin por defecto
        if not os.path.exists(self.users_file):
            admin_user = {
                "username": "admin",
                "password": "admin123",
                "is_admin": True
            }
            with open(self.users_file, 'w') as f:
                json.dump([admin_user], f)
    
    def login(self, username: str, password: str) -> bool:
        """Autenticar usuario"""
        users = self._load_users()
        for user in users:
            if user["username"] == username and user["password"] == password:
                self.current_user = user
                return True
        return False
    
    def logout(self):
        """Cerrar sesión"""
        self.current_user = None
    
    def create_user(self, username: str, password: str, is_admin: bool = False) -> bool:
        """Crear nuevo usuario (solo admin)"""
        if not self.current_user or not self.current_user.get("is_admin"):
            return False
        
        users = self._load_users()
        if any(u["username"] == username for u in users):
            return False
        
        users.append({
            "username": username,
            "password": password,
            "is_admin": is_admin
        })
        self._save_users(users)
        return True
    
    def get_all_users(self) -> List[Dict]:
        """Obtener lista de usuarios (solo admin)"""
        if not self.current_user or not self.current_user.get("is_admin"):
            return []
        return self._load_users()
    
    def delete_user(self, username: str) -> bool:
        """Eliminar usuario (solo admin, no puede eliminar admin)"""
        if not self.current_user or not self.current_user.get("is_admin"):
            return False
        
        if username == "admin":
            return False
        
        users = self._load_users()
        users = [u for u in users if u["username"] != username]
        self._save_users(users)
        return True
    
    def create_file(self, filename: str, content: str) -> bool:
        """Crear un nuevo archivo"""
        if not self.current_user:
            return False
        
        fat_table = self._load_fat_table()
        
        # Verificar que no exista
        if any(f["nombre"] == filename and not f["papelera"] for f in fat_table):
            return False
        
        # Segmentar contenido en bloques de 20 caracteres
        blocks = []
        block_size = 20
        for i in range(0, len(content), block_size):
            chunk = content[i:i+block_size]
            blocks.append(chunk)
        
        if not blocks:
            blocks = [""]
        
        # Crear bloques físicos
        block_files = []
        for idx, block_data in enumerate(blocks):
            block_filename = f"{filename}_block_{idx}.json"
            block_path = os.path.join(self.blocks_dir, block_filename)
            
            next_file = f"{filename}_block_{idx+1}.json" if idx < len(blocks) - 1 else None
            
            block_info = {
                "datos": block_data,
                "siguiente_archivo": next_file,
                "eof": idx == len(blocks) - 1
            }
            
            with open(block_path, 'w') as f:
                json.dump(block_info, f, indent=2)
            
            block_files.append(block_filename)
        
        # Crear entrada en FAT
        now = datetime.now().isoformat()
        fat_entry = {
            "nombre": filename,
            "ruta_inicial": block_files[0] if block_files else None,
            "papelera": False,
            "total_caracteres": len(content),
            "fecha_creacion": now,
            "fecha_modificacion": now,
            "fecha_eliminacion": None,
            "owner": self.current_user["username"],
            "permisos": {}
        }
        
        fat_table.append(fat_entry)
        self._save_fat_table(fat_table)
        return True
    
    def list_files(self, include_deleted: bool = False) -> List[Dict]:
        """Listar archivos"""
        if not self.current_user:
            return []
        
        fat_table = self._load_fat_table()
        
        if include_deleted:
            return [f for f in fat_table if f["papelera"]]
        else:
            return [f for f in fat_table if not f["papelera"]]
    
    def get_file_content(self, filename: str) -> Optional[str]:
        """Leer contenido completo del archivo"""
        if not self.current_user:
            return None
        
        fat_table = self._load_fat_table()
        file_entry = next((f for f in fat_table if f["nombre"] == filename), None)
        
        if not file_entry or file_entry["papelera"]:
            return None
        
        # Verificar permisos de lectura
        if not self._has_permission(file_entry, "lectura"):
            return None
        
        # Leer bloques concatenados
        content = ""
        current_block = file_entry["ruta_inicial"]
        
        while current_block:
            block_path = os.path.join(self.blocks_dir, current_block)
            
            if not os.path.exists(block_path):
                break
            
            with open(block_path, 'r') as f:
                block_data = json.load(f)
                content += block_data["datos"]
                
                if block_data["eof"]:
                    break
                
                current_block = block_data["siguiente_archivo"]
        
        return content
    
    def modify_file(self, filename: str, new_content: str) -> bool:
        """Modificar archivo existente"""
        if not self.current_user:
            return False
        
        fat_table = self._load_fat_table()
        file_entry = next((f for f in fat_table if f["nombre"] == filename), None)
        
        if not file_entry or file_entry["papelera"]:
            return False
        
        # Verificar permisos de escritura
        if not self._has_permission(file_entry, "escritura"):
            return False
        
        # Eliminar bloques antiguos
        self._delete_blocks(file_entry["ruta_inicial"])
        
        # Crear nuevos bloques
        blocks = []
        block_size = 20
        for i in range(0, len(new_content), block_size):
            chunk = new_content[i:i+block_size]
            blocks.append(chunk)
        
        if not blocks:
            blocks = [""]
        
        block_files = []
        for idx, block_data in enumerate(blocks):
            block_filename = f"{filename}_block_{idx}.json"
            block_path = os.path.join(self.blocks_dir, block_filename)
            
            next_file = f"{filename}_block_{idx+1}.json" if idx < len(blocks) - 1 else None
            
            block_info = {
                "datos": block_data,
                "siguiente_archivo": next_file,
                "eof": idx == len(blocks) - 1
            }
            
            with open(block_path, 'w') as f:
                json.dump(block_info, f, indent=2)
            
            block_files.append(block_filename)
        
        # Actualizar FAT
        file_entry["ruta_inicial"] = block_files[0] if block_files else None
        file_entry["total_caracteres"] = len(new_content)
        file_entry["fecha_modificacion"] = datetime.now().isoformat()
        
        self._save_fat_table(fat_table)
        return True
    
    def delete_file(self, filename: str) -> bool:
        """Mover archivo a papelera"""
        if not self.current_user:
            return False
        
        fat_table = self._load_fat_table()
        file_entry = next((f for f in fat_table if f["nombre"] == filename), None)
        
        if not file_entry or file_entry["papelera"]:
            return False
        
        # Solo el owner puede eliminar
        if file_entry["owner"] != self.current_user["username"] and not self.current_user.get("is_admin"):
            return False
        
        file_entry["papelera"] = True
        file_entry["fecha_eliminacion"] = datetime.now().isoformat()
        
        self._save_fat_table(fat_table)
        return True
    
    def recover_file(self, filename: str) -> bool:
        """Recuperar archivo de la papelera"""
        if not self.current_user:
            return False
        
        fat_table = self._load_fat_table()
        file_entry = next((f for f in fat_table if f["nombre"] == filename), None)
        
        if not file_entry or not file_entry["papelera"]:
            return False
        
        # Solo el owner puede recuperar
        if file_entry["owner"] != self.current_user["username"] and not self.current_user.get("is_admin"):
            return False
        
        file_entry["papelera"] = False
        file_entry["fecha_eliminacion"] = None
        
        self._save_fat_table(fat_table)
        return True
    
    def set_permission(self, filename: str, username: str, permission_type: str, value: bool) -> bool:
        """Establecer permisos (solo owner)"""
        if not self.current_user:
            return False
        
        fat_table = self._load_fat_table()
        file_entry = next((f for f in fat_table if f["nombre"] == filename), None)
        
        if not file_entry:
            return False
        
        # Solo el owner puede cambiar permisos
        if file_entry["owner"] != self.current_user["username"]:
            return False
        
        if username not in file_entry["permisos"]:
            file_entry["permisos"][username] = {"lectura": False, "escritura": False}
        
        file_entry["permisos"][username][permission_type] = value
        
        self._save_fat_table(fat_table)
        return True
    
    def get_file_metadata(self, filename: str) -> Optional[Dict]:
        """Obtener metadatos del archivo"""
        if not self.current_user:
            return None
        
        fat_table = self._load_fat_table()
        file_entry = next((f for f in fat_table if f["nombre"] == filename), None)
        
        return file_entry
    
    def _has_permission(self, file_entry: Dict, permission_type: str) -> bool:
        """Verificar si el usuario tiene permiso"""
        # Owner y admin tienen todos los permisos
        if file_entry["owner"] == self.current_user["username"] or self.current_user.get("is_admin"):
            return True
        
        # Verificar permisos específicos
        user_perms = file_entry["permisos"].get(self.current_user["username"], {})
        return user_perms.get(permission_type, False)
    
    def _delete_blocks(self, initial_block: str):
        """Eliminar bloques físicos"""
        current_block = initial_block
        
        while current_block:
            block_path = os.path.join(self.blocks_dir, current_block)
            
            if not os.path.exists(block_path):
                break
            
            with open(block_path, 'r') as f:
                block_data = json.load(f)
            
            next_block = block_data["siguiente_archivo"]
            os.remove(block_path)
            
            if block_data["eof"]:
                break
            
            current_block = next_block
    
    def _load_fat_table(self) -> List[Dict]:
        """Cargar tabla FAT"""
        with open(self.fat_table_file, 'r') as f:
            return json.load(f)
    
    def _save_fat_table(self, fat_table: List[Dict]):
        """Guardar tabla FAT"""
        with open(self.fat_table_file, 'w') as f:
            json.dump(fat_table, f, indent=2)
    
    def _load_users(self) -> List[Dict]:
        """Cargar usuarios"""
        with open(self.users_file, 'r') as f:
            return json.load(f)
    
    def _save_users(self, users: List[Dict]):
        """Guardar usuarios"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)