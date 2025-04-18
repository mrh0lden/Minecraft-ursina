from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# Player setup
player = FirstPersonController(gravity=1)
player.height = 2              # Makes the player 2 blocks tall
player.y = 1                   # Feet stand on top of blocks
player.camera_pivot.y = 1.62   # Eye level above blocks (like Minecraft)

Sky()

# Invisible base floor to catch falling players
floor = Entity(
    model='plane', color=color.green, scale=(100, 1, 100),
    position=(0, -1, 0), collider='box', visible=False
)

# Build a world of grass blocks
boxes = []
for i in range(20):
    for j in range(20):
        box = Entity(
            model='cube', color=color.white, position=(j, 0, i),
            texture='grass.png', parent=scene, origin_y=0.5,
            collider='box'
        )
        boxes.append(box)

# Block types and selection
block_types = ['grass.png', 'stone.png', 'plank.png', 'obsidian.png', 'netherrack.png']
selected_block = 0

# Show selected block type (top-left)
block_text = Text(text='Block: Grass', position=window.top_left, scale=1.2, origin=(-0.5, 0.5))

# Show version (top-center)
version_text = Text(text='alpha 2025w16m4', origin=(0, 0), position=(0, 0.45), scale=1.5)

def input(key):
    global selected_block

    # Switch between block types with number keys
    if key == '1': selected_block = 0
    if key == '2': selected_block = 1
    if key == '3': selected_block = 2
    if key == '4': selected_block = 3
    if key == '5': selected_block = 4

    block_name = block_types[selected_block].split('.')[0].capitalize()
    block_text.text = f'Block: {block_name}'

    # Block placement and removal
    for box in boxes:
        if box.hovered:
            if key == 'left mouse down':
                new_box = Entity(
                    model='cube',
                    color=color.white,
                    position=box.position + mouse.normal,
                    texture=block_types[selected_block],
                    parent=scene,
                    origin_y=0.5,
                    collider='box'
                )
                boxes.append(new_box)
            if key == 'right mouse down':
                boxes.remove(box)
                destroy(box)

def update():
    # Reset player if they fall below world
    if player.y < -5:
        player.position = (10, 5, 10)

app.run()
