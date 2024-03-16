extends CharacterBody2D
class_name Player
'''
Player script for the Penguin Character

@author Daniel Hibbin
'''


# Define constants
const SPEED = 30.0
const JUMPFORCE = 750.0
const ROTATIONSPEED = 0.1


# Get the gravity from the project settings to be synced with RigidBody nodes.
var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")
var currentGravity = ProjectSettings.get_setting("physics/2d/default_gravity")


# Define an enum for the movement states and a variable for current state
enum movementState {flipGravity, jumpGravity}
var currentState : movementState = movementState.jumpGravity


# Define varaibles related to whether the player is alive or can be killed
var alive : bool = true
const invinsiblePhysicsFrames : int = 30
var invinsibleTimer = 0


# Reference to score and the variable counting the score
@onready var scoreCounter = $"../Camera2D/CanvasLayer/Control/ScoreCounter"
var score : int = 0


#Reference to the world scroller
@onready var worldScroller = $"../WorldScroller"


#Reference to the sprite's animation player
@onready var animationPlayer = $Penguin/AnimationPlayer
@onready var deathAnimationPlayer = $"../CanvasLayer/AnimationPlayer"


#Reference to the sprites
@onready var penguinSprite = $Penguin
@onready var wingPivot = $Penguin/WingPivot


#Reference to return button and final score label
@onready var returnButton = $"../CanvasLayer/ColorRect/VBoxContainer/ReturnButton"
@onready var finalScoreLabel = $"../CanvasLayer/ColorRect/VBoxContainer/FinalScoreLabel"


# Always start the player in the flipGravity movement state
func _ready():
	changeState(movementState.flipGravity)


# This is called every physics frame
func _physics_process(delta):
	# Handle the rotation of the player sprite
	handleRotation()
	
	
	# If alive, behave as normal
	if alive:
		# Increment the score
		score += 1
		
		
		# Apply the gravity if the player is not on floor or ceiling
		if not is_on_floor() or not is_on_ceiling():
			velocity.y += currentGravity * delta
		
		
		# If the invinsible timer is active, decrement it
		if invinsibleTimer > 0:
			invinsibleTimer -= 1
		
		
		# If player is not in the centre of the screen, move them towards the centre
		if position.x < 0:
			velocity.x = -position.x * SPEED / 256
		
		
		# Handle current movement state
		match currentState:
			movementState.flipGravity:
				# Flip player if space is pressed
				if Input.is_action_just_pressed("ui_accept") and (is_on_floor() or is_on_ceiling()):
					# Play flip animation
					if currentGravity > 0:
						animationPlayer.play("flip")
					else:
						animationPlayer.play_backwards("flip")
					# Invert gravity and apply force
					currentGravity = -currentGravity
					velocity.y += currentGravity * delta
			movementState.jumpGravity:
				# Jump if space is pressed
				if Input.is_action_just_pressed("ui_accept"):
					velocity.y = -JUMPFORCE
		
		
		# Check if there is a collision and kill the player if they're in jump state
		var collision = move_and_slide()
		if collision and currentState == movementState.jumpGravity:
			kill()
		
		
		# Update the score text
		scoreCounter.text = "Score: %d" % score


# Adjust the sprite's rotation in accordance with movement state and vertical velocity
func handleRotation():
	match currentState:
		movementState.flipGravity:
			# Lerp rotation of penguin and wing to 0 if in flip state
			penguinSprite.rotation = lerp(penguinSprite.rotation, 0.0, ROTATIONSPEED)
			wingPivot.rotation = lerp(wingPivot.rotation, 0.0, ROTATIONSPEED)
		movementState.jumpGravity:
			# Lerp rotation to 45 degrees * normalised velocity.y, 
			# causing the sprite to go up and down with jumps
			penguinSprite.rotation = lerp(penguinSprite.rotation, deg_to_rad(-45.0) * (-velocity.y / 1000), ROTATIONSPEED)
			wingPivot.rotation = lerp(wingPivot.rotation, deg_to_rad(-45.0) * (-velocity.y / 1000) * 2, ROTATIONSPEED)


# Change the state of the player to a different movement state
func changeState(newState : movementState):
	# Change state and start invincibility timer
	currentState = newState
	invinsibleTimer = invinsiblePhysicsFrames
	
	
	# If changing to the jumping state, apply force to move player away from surfaces
	if newState == movementState.jumpGravity:
		if is_on_floor() or is_on_ceiling():
			# If already on surface, apply fraction of jumping force
			if currentGravity < 0:
				velocity.y = JUMPFORCE * 0.5
			else:
				velocity.y = -JUMPFORCE * 0.7
		else:
			# If not on surface, apply jumping force in proportion to distance from centre
			var centreDistance = (position.y + 200) / 200
			velocity.y = JUMPFORCE * -centreDistance
		
		
		# If upside down, flip the penguin sprite
		if currentGravity < 0:
			animationPlayer.play_backwards("flip")
	
	
	# Change the gravity to match the current state
	changeGravity()


# Change the gravity of the player to suit the feeling of that movement state
func changeGravity():
	match currentState:
		movementState.flipGravity:
			currentGravity = gravity * 3
		movementState.jumpGravity:
			currentGravity = gravity * 2


# Get the current movement state of the player
func getState():
	return currentState


# Attempt to kill the player
func kill():
	# If the player is not invincible, kill them
	if invinsibleTimer <= 0:
		# Stop scrolling the world and end normal functionality
		worldScroller.stop()
		alive = false
		
		# Introduce death screen and set text of final score
		deathAnimationPlayer.play("endGame")
		finalScoreLabel.text = "Final Score: %d" % score
