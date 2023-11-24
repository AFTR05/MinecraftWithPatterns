from enum import Enum,auto
from ursina import Entity
from abc import ABC, abstractmethod
from ursina.prefabs.health_bar import HealthBar
from ursina import *
from ursina.shaders import lit_with_shadows_shader


class NpcFactory(ABC):
    @abstractmethod
    def get_mob(self):
        pass

class MobFactoryCreator:
    @staticmethod
    def create_mob(npc_type, player, shootables_parent, position=None):
        if npc_type == NpcType.HOSTIL:
            return Esqueleto(shootables_parent, player, position=position)
        elif npc_type == NpcType.PASIVO:
            return Pollo(shootables_parent, player, position=position)



class NpcType(Enum):
    PASIVO = auto()
    HOSTIL = auto()

class NPC(Entity, NpcFactory):
    def __init__(self, model, **kwargs):
        super().__init__(model=model, **kwargs)

    def get_mob(self):
        pass


class Pollo(NPC):
    def __init__(self, shootables_parent, player, **kwargs):
        super().__init__(model='sphere', parent=shootables_parent, scale_y=0.5, origin_y=-0.25, color=color.yellow, collider='box', **kwargs)
        self.health_bar = Entity(parent=self, y=1.2, model='cube', color=color.green, world_scale=(1.5, .1, .1))
        self.max_hp = 50
        self.hp = self.max_hp
        self.player = player

    def update(self):
        player=self.player
        dist = distance_xz(player.position, self.position)
        if dist > 40:
            return
        self.health_bar.alpha = max(0, self.health_bar.alpha - time.dt)
        self.look_at_2d(player.position, 'y')

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value
        if value <= 0:
            destroy(self)
            return
        self.health_bar.world_scale_x = self.hp / self.max_hp * 1.5
        self.health_bar.alpha = 1

    def get_mob(self):
        return self

    def get_mob(self):
        return self
    
class Esqueleto(NPC):
    def __init__(self, shootables_parent, player, **kwargs):
        super().__init__(model='cube', parent=shootables_parent, scale_y=2, origin_y=-0.5, color=color.white, collider='box', **kwargs)
        self.health_bar = Entity(parent=self, y=1.2, model='cube', color=color.red, world_scale=(1.5, .1, .1))
        self.max_hp = 100
        self.hp = self.max_hp
        self.player = player

    def update(self):
        player=self.player
        dist = distance_xz(player.position, self.position)
        if dist > 40:
            return

        self.health_bar.alpha = max(0, self.health_bar.alpha - time.dt)

        self.look_at_2d(player.position, 'y')
        hit_info = raycast(self.world_position + Vec3(0, 1, 0), self.forward, 30, ignore=(self,))
        if hit_info.entity == player:
            if dist > 2:
                self.position += self.forward * time.dt * 5

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value
        if value <= 0:
            destroy(self)
            return

        self.health_bar.world_scale_x = self.hp / self.max_hp * 1.5
        self.health_bar.alpha = 1

    def get_mob(self):
        return self