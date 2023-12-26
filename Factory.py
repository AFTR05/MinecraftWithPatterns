
from NPCs import NpcType, MobFactoryCreator
from ursina.shaders import lit_with_shadows_shader
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from SingleUsuario import SingleUsuario
from NPCs import MobFactoryCreator
from ursina.prefabs.ursfx import ursfx

#cambio de prueba de instalacion de git

def pause_input(key):
    if key == 'tab':    # press tab to toggle edit/play mode
        editor_camera.enabled = not editor_camera.enabled

        player.visible_self = editor_camera.enabled
        player.cursor.enabled = not editor_camera.enabled
        gun.enabled = not editor_camera.enabled
        mouse.locked = not editor_camera.enabled
        editor_camera.position = player.position

        application.paused = editor_camera.enabled



def update():
    if held_keys['left mouse']:
        shoot()

def shoot():
    if not gun.on_cooldown:
        # print('shoot')
        gun.on_cooldown = True
        gun.muzzle_flash.enabled=True
        ursfx([(0.0, 0.0), (0.1, 0.9), (0.15, 0.75), (0.3, 0.14), (0.6, 0.0)], volume=0.5, wave='noise', pitch=random.uniform(-13,-12), pitch_change=-12, speed=3.0)
        invoke(gun.muzzle_flash.disable, delay=.05)
        invoke(setattr, gun, 'on_cooldown', False, delay=.15)
        if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'hp'):
            mouse.hovered_entity.hp -= 10
            mouse.hovered_entity.blink(color.red)


app = Ursina()
random.seed(0)
Entity.default_shader = lit_with_shadows_shader
ground = Entity(model='plane', collider='box', scale=64, texture='grass', texture_scale=(4,4))

editor_camera = EditorCamera(enabled=False, ignore_paused=True)
player = SingleUsuario.get()
player.collider = BoxCollider(player, Vec3(0,1,0), Vec3(1,2,1))
gun = Entity(model='cube', parent=camera, position=(.5,-.25,.25), scale=(.3,.2,1), origin_z=-.5, color=color.black, on_cooldown=False)
gun.muzzle_flash = Entity(parent=gun, z=1, world_scale=.5, model='quad', color=color.yellow, enabled=False)
shootables_parent = Entity()
mouse.traverse_target = shootables_parent   

sun = DirectionalLight()
sun.look_at(Vec3(1,-1,-1))
Sky()
    


pause_handler = Entity(ignore_paused=True, input=pause_input)
esqueletos = [MobFactoryCreator.create_mob(NpcType.HOSTIL, player, shootables_parent, position=player.position + Vec3(random.uniform(10, 20), 0, random.uniform(10, 20))) for _ in range(4)]
pollos = [MobFactoryCreator.create_mob(NpcType.PASIVO, player, shootables_parent, position=(random.uniform(-8, 8), 0, random.uniform(-8, 8))) for x in range(4)]

    

app.run()



