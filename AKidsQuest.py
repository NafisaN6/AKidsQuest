import random
import simplegui

# Global Variables
score = 0
win_score = 10
lose_score = -3
actions = ["Plant seeds from the garden", "Recycle trash", "Clean up the neighborhood", "Pick up water from the well", "Filter the water", "Cook food for your mom", "Use your bike instead of a car", "Use your car", "Don't recycle trash", "Don't pick up water from the well"]

# Animation States
animation_state = None
player_position = [50, 200]  # Starting position of the player
target_position = [50, 200]   # Target position for animation
trash_index = 0  # Index to track which trash to collect
cleaning_animation = False  # Flag for cleaning animation

# Task Locations
task_locations = {
    0: (300, 400),  # Plant seeds (Garden)
    1: (350, 350),  # Recycle trash (Litter)
    2: (100, 350),  # Clean up (Neighborhood)
    3: (420, 250),  # Pick up water (Well)
    4: (300, 300),  # Filter water (Kitchen)
    5: (260, 300),  # Cook food (House)
    6: (150, 400),  # Use bike (Bike)
    7: (50, 400),   # Use car (off-screen)
    8: (50, 350),   # Don't recycle (off-screen)
    9: (400, 300)   # Don't pick up water (off-screen)
}

# Trash Locations
trash_locations = [
    (150, 320),  # Trash 1
    (250, 350),  # Trash 2
    (370, 400),  # Trash 3
    (480, 380)   # Trash 4
]
picked_trash = []  # List to track collected trash

# Game Functions
def start_game():
    global score, animation_state, player_position, picked_trash, trash_index, cleaning_animation
    score = 0
    animation_state = None
    player_position = [50, 200]  # Reset player position
    picked_trash = []  # Reset picked trash
    trash_index = 0  # Reset trash index
    cleaning_animation = False  # Reset cleaning animation flag
    update_gui()

def perform_action(action_index):
    global score, animation_state, target_position, trash_index, cleaning_animation
    message = ""

    if action_index < len(actions):
        if action_index == 2:  # Clean up the neighborhood
            trash_index = 0  # Reset trash index for cleanup
            cleaning_animation = True  # Start cleaning animation
            update_gui("Cleaning up the neighborhood!")
        elif action_index in [0, 1, 3, 4, 5, 6]:  # Actions that earn points
            score += 1
            message = f"You did a good thing: {actions[action_index]}! Points: +1"
            target_position = task_locations[action_index]
            animation_state = (actions[action_index], 'good')
        else:  # Actions that lose points
            score -= 1
            message = f"Oh no! You've made a mistake: {actions[action_index]}! Points: -1"
            target_position = task_locations[action_index]
            animation_state = (actions[action_index], 'bad')

        update_gui(message)

def collect_trash():
    global player_position, score, trash_index, cleaning_animation
    if trash_index < len(trash_locations):
        target_position = trash_locations[trash_index]
        player_position[0], player_position[1] = target_position  # Move to trash
        picked_trash.append(target_position)  # Mark trash as picked
        score += 1  # Award points for picking up trash
        trash_index += 1  # Move to the next trash
        update_gui("You cleaned up some trash! +1 point!")
    else:
        cleaning_animation = False  # Stop cleaning animation when all trash is picked
        update_gui("All trash has been cleaned up!")

def random_event():
    global score
    if random.random() < 0.5:  # 50% chance for a random event
        score -= 1
        message = "Oh no! Your bike tires popped and you had to use your car! -1 point!"
    else:
        score += 1
        message = "A nice old lady decided to help you water your garden! +1 point!"

    update_gui(message)

def update_gui(message=""):
    message_label.set_text(message)
    score_label.set_text(f"Score: {score}")

    if score >= win_score:
        message_label.set_text("Congratulations! You helped your mom! You win!")
        disable_buttons()
    elif score <= lose_score:
        message_label.set_text("Oh no! You've caused too much pollution. Game Over!")
        disable_buttons()

def enable_buttons():
    for i, button in enumerate(action_buttons):
        button.set_text(actions[i])  # Reset button text to original actions

def disable_buttons():
    for button in action_buttons:
        button.set_text("Game Over")  # Indicate the game is over
    restart_button.set_text("Restart Game")  # Show restart option

def restart_game():
    start_game()  # Restart the game
    enable_buttons()  # Reset button states

# Animation function
def draw(canvas):
    global animation_state, player_position, target_position, trash_index, cleaning_animation

    # Draw solid blue sky
    canvas.draw_polygon([(0, 0), (700, 0), (700, 300), (0, 300)], 1, "Blue", "LightBlue")

    # Draw static clouds (as 3 larger circles in a triangular shape)
    canvas.draw_circle((70, 50), 20, 1, "White", "White")  # Cloud 1, Circle 1
    canvas.draw_circle((85, 80), 20, 1, "White", "White")  # Cloud 1, Circle 2
    canvas.draw_circle((55, 80), 20, 1, "White", "White")  # Cloud 1, Circle 3

    canvas.draw_circle((170, 30), 20, 1, "White", "White")  # Cloud 2, Circle 1
    canvas.draw_circle((185, 60), 20, 1, "White", "White")  # Cloud 2, Circle 2
    canvas.draw_circle((155, 60), 20, 1, "White", "White")  # Cloud 2, Circle 3

    canvas.draw_circle((270, 70), 20, 1, "White", "White")  # Cloud 3, Circle 1
    canvas.draw_circle((285, 100), 20, 1, "White", "White")  # Cloud 3, Circle 2
    canvas.draw_circle((255, 100), 20, 1, "White", "White")  # Cloud 3, Circle 3

    canvas.draw_circle((420, 40), 20, 1, "White", "White")  # Cloud 4, Circle 1
    canvas.draw_circle((435, 70), 20, 1, "White", "White")  # Cloud 4, Circle 2
    canvas.draw_circle((405, 70), 20, 1, "White", "White")  # Cloud 4, Circle 3

    canvas.draw_circle((570, 10), 20, 1, "White", "White")  # Cloud 5, Circle 1
    canvas.draw_circle((585, 40), 20, 1, "White", "White")  # Cloud 5, Circle 2
    canvas.draw_circle((555, 40), 20, 1, "White", "White")  # Cloud 5, Circle 3

    # Draw green ground
    canvas.draw_polygon([(0, 300), (700, 300), (700, 600), (0, 600)], 1, "Green", "LightGreen")

    # Draw a trash bin for recycling
    canvas.draw_polygon([(350, 360), (370, 360), (370, 400), (350, 400)], 1, "Black", "Gray")  # Bin body
    canvas.draw_polygon([(345, 355), (375, 355), (375, 360), (345, 360)], 1, "Black", "DarkGray")  # Lid

    # Draw trash pieces that are not picked up
    for trash in trash_locations:
        if trash not in picked_trash:
            canvas.draw_circle(trash, 10, 1, "Brown", "LightCoral")  # Trash pieces

    # Well
    canvas.draw_polygon([(400, 250), (440, 250), (440, 300), (400, 300)], 1, "Brown", "LightBlue")
    canvas.draw_line((420, 250), (420, 200), 5, "Black")  # Well handle
    canvas.draw_circle((420, 275), 20, 1, "Black", "Gray")  # Bucket

    # Kitchen
    canvas.draw_polygon([(250, 300), (350, 300), (350, 350), (250, 350)], 1, "Brown", "LightYellow")
    # Draw stove using polygons
    canvas.draw_polygon([(260, 310), (290, 310), (290, 340), (260, 340)], 1, "Black", "DarkGray")  # Stove

    # Draw houses
    canvas.draw_polygon([(100, 250), (150, 250), (150, 300), (100, 300)], 1, "Brown", "Tan")  # House 1
    canvas.draw_polygon([(180, 250), (230, 250), (230, 300), (180, 300)], 1, "Brown", "Tan")  # House 2

    # Bike
    canvas.draw_circle((150, 400), 15, 1, "Black", "Blue")
    canvas.draw_circle((150, 400), 5, 1, "Black", "Black")

    # Draw player
    canvas.draw_circle(player_position, 15, 2, "Black", "Red")

    # Animate player movement when cleaning
    if cleaning_animation and trash_index < len(trash_locations):
        target_position = trash_locations[trash_index]
        # Move towards the trash location
        if player_position[0] < target_position[0]:
            player_position[0] += 2  # Move right
        elif player_position[0] > target_position[0]:
            player_position[0] -= 2  # Move left
        if player_position[1] < target_position[1]:
            player_position[1] += 2  # Move down
        elif player_position[1] > target_position[1]:
            player_position[1] -= 2  # Move up

        # Check if the player has reached the trash
        if abs(player_position[0] - target_position[0]) < 2 and abs(player_position[1] - target_position[1]) < 2:
            collect_trash()  # Collect trash when reached

    # Animate other actions (if any)
    if animation_state:
        if player_position[0] < target_position[0]:
            player_position[0] += 2  # Move right
        elif player_position[0] > target_position[0]:
            player_position[0] -= 2  # Move left
        if player_position[1] < target_position[1]:
            player_position[1] += 2  # Move down
        elif player_position[1] > target_position[1]:
            player_position[1] -= 2  # Move up

        # Check if the player has reached the target
        if abs(player_position[0] - target_position[0]) < 2 and abs(player_position[1] - target_position[1]) < 2:
            animation_state = None  # Stop animation when task is complete

# Create the SimpleGUI Frame
frame = simplegui.create_frame("A Kid's Quest", 700, 600)

# Create Labels
score_label = frame.add_label("Score: 0")
message_label = frame.add_label("")

# Create Action Buttons
action_buttons = []
for i in range(len(actions)):
    button = frame.add_button(actions[i], lambda index=i: perform_action(index))
    action_buttons.append(button)

# Random Event Button
frame.add_button("Random Event", random_event)

# Start Game Button
frame.add_button("Start Game", start_game)

# Restart Game Button
restart_button = frame.add_button("Restart Game", restart_game)

# Set up the draw handler
frame.set_draw_handler(draw)

# Start the Frame
start_game()
frame.start()
