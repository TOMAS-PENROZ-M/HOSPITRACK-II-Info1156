# recepcionista/validation.py

import re
import logging
from datetime import datetime
from tkinter import messagebox
from typing import Dict, Any, Tuple, List

logger = logging.getLogger("recepcionista.validation")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class ValidationError(Exception):
    """Excepción para errores de validación."""
    def __init__(self, messages: List[str]):
        super().__init__("; ".join(messages))
        self.messages = messages


class FormValidator:
    """
    Valida datos de formularios principales en la vista de recepcionista,
    mostrando mensajes de error mediante messagebox y registrando los eventos.
    """

    TITLE_MIN_LENGTH = 5
    TITLE_MAX_LENGTH = 100
    DESCRIPTION_MIN_LENGTH = 10
    DESCRIPTION_MAX_LENGTH = 1000
    USERNAME_REGEX = re.compile(r"^[A-Za-z0-9_]{3,30}$")
    PASSWORD_MIN_LENGTH = 8
    PASSWORD_MAX_LENGTH = 128

    def __init__(self):
        self.errors: List[str] = []

    def reset(self):
        """Reinicia la lista de errores."""
        self.errors = []

    def validate_title(self, title: str) -> bool:
        """Valida el título de una solicitud."""
        if title is None:
            self.errors.append("El título no puede estar vacío.")
            return False
        title = title.strip()
        length = len(title)
        if length < self.TITLE_MIN_LENGTH:
            self.errors.append(
                f"El título debe tener al menos {self.TITLE_MIN_LENGTH} caracteres."
            )
            return False
        if length > self.TITLE_MAX_LENGTH:
            self.errors.append(
                f"El título no puede exceder {self.TITLE_MAX_LENGTH} caracteres."
            )
            return False
        return True

    def validate_description(self, description: str) -> bool:
        """Valida la descripción de una solicitud."""
        if description is None:
            self.errors.append("La descripción no puede estar vacía.")
            return False
        description = description.strip()
        length = len(description)
        if length < self.DESCRIPTION_MIN_LENGTH:
            self.errors.append(
                f"La descripción debe tener al menos {self.DESCRIPTION_MIN_LENGTH} caracteres."
            )
            return False
        if length > self.DESCRIPTION_MAX_LENGTH:
            self.errors.append(
                f"La descripción no puede exceder {self.DESCRIPTION_MAX_LENGTH} caracteres."
            )
            return False
        # Comprueba si contiene etiquetas HTML peligrosas
        if re.search(r"<\s*script\b", description, re.IGNORECASE):
            self.errors.append("La descripción contiene código HTML no permitido.")
            return False
        return True

    def validate_priority(self, priority: Any) -> bool:
        """Valida el valor de prioridad."""
        allowed = {"Baja", "Media", "Alta"}
        if priority not in allowed:
            self.errors.append(f"Prioridad inválida: {priority}.")
            return False
        return True

    def validate_user_credentials(self, username: str, password: str) -> bool:
        """
        Valida formato de nombre de usuario y contraseña
        utilizados en el formulario de login.
        """
        # Username
        if not username:
            self.errors.append("El nombre de usuario es obligatorio.")
        elif not self.USERNAME_REGEX.match(username):
            self.errors.append(
                "El nombre de usuario solo puede contener letras, números y guiones bajos, 3-30 caracteres."
            )
        # Password
        if not password:
            self.errors.append("La contraseña es obligatoria.")
        else:
            length = len(password)
            if length < self.PASSWORD_MIN_LENGTH:
                self.errors.append(
                    f"La contraseña debe tener al menos {self.PASSWORD_MIN_LENGTH} caracteres."
                )
            if length > self.PASSWORD_MAX_LENGTH:
                self.errors.append(
                    f"La contraseña no puede exceder {self.PASSWORD_MAX_LENGTH} caracteres."
                )
        return not self.errors

    def validate_form(self, data: Dict[str, Any]) -> None:
        """
        Valida un formulario genérico de solicitud. 
        Lanza ValidationError con lista de mensajes si hay errores.
        """
        self.reset()
        title = data.get("titulo")
        desc = data.get("descripcion")
        prio = data.get("prioridad")

        self.validate_title(title)
        self.validate_description(desc)
        # prioridad es optativa en este formulario
        if prio is not None:
            self.validate_priority(prio)

        if self.errors:
            logger.warning(f"Errores de validación: {self.errors}")
            raise ValidationError(self.errors)

    def show_errors(self, parent_title: str = "Error de Validación") -> None:
        """
        Muestra todos los errores acumulados en un messagebox.
        """
        if not self.errors:
            return
        msg = "\n".join(self.errors)
        messagebox.showerror(parent_title, msg)
        logger.debug("Mostrando mensaje de error al usuario.")

    def validate_and_show(self, data: Dict[str, Any]) -> bool:
        """
        Atajo: valida y muestra errores si los hay.
        Retorna True si es válido, False si hubo errores.
        """
        try:
            self.validate_form(data)
            return True
        except ValidationError as ve:
            self.show_errors()
            return False


# Ejemplo de uso directo (solo para pruebas manuales)
if __name__ == "__main__":
    validator = FormValidator()

    # Caso válido
    data_ok = {"titulo": "Consulta general", "descripcion": "Quisiera información sobre mis citas.", "prioridad": "Media"}
    valid = validator.validate_and_show(data_ok)
    print("Validación OK:", valid)

    # Caso con errores
    data_err = {"titulo": "A", "descripcion": "<script>alert(1)</script>", "prioridad": "Critica"}
    valid2 = validator.validate_and_show(data_err)
    print("Validación OK:", valid2)
