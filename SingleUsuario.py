from ursina.prefabs.first_person_controller import FirstPersonController
from ursina import color

class SingleUsuario:
    _instancia = None

    def __new__(cls):
        if not cls._instancia:
            cls._instancia = FirstPersonController(model='cube', z=-10, color=color.blue, origin_y=-.5, speed=8, collider='box')
        return cls._instancia

    @classmethod
    def get(cls):
        if not cls._instancia:
            cls._instancia = cls()
        return cls._instancia
    
    