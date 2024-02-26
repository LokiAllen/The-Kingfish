extends CharacterBody2D
class_name Player

const SPEED = 300.0
const jumpForce = 750.0

# Get the gravity from the project settings to be synced with RigidBody nodes.
var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")
var currentGravity = ProjectSettings.get_setting("physics/2d/default_gravity")

enum movementState {flipGravity, jumpGravity}
var currentState : movementState = movementState.jumpGravity

@onready var scoreCounter = $"../Camera2D/CanvasLayer/Control/ScoreCounter"
var score : int = 0


# Always start the player in the flipGravity movement state
func _ready():
	changeState(movementState.flipGravity)


func _physics_process(delta):
	score += 1
	# Add the gravity.
	if not is_on_floor() or not is_on_ceiling():
		velocity.y += currentGravity * delta
	
	
	# Handle movement state
	match currentState:
		movementState.flipGravity:
			if Input.is_action_just_pressed("ui_accept") and (is_on_floor() or is_on_ceiling()):
				currentGravity = -currentGravity
				velocity.y += currentGravity * delta
		movementState.jumpGravity:
			if Input.is_action_just_pressed("ui_accept"):
				velocity.y = -jumpForce

	move_and_slide()
	
	scoreCounter.text = "Score: %d" % score
	


func changeState(newState : movementState):
	currentState = newState
	print(currentState)
	if newState == movementState.jumpGravity:
		if is_on_floor() or is_on_ceiling():
			if currentGravity < 0:
				velocity.y = jumpForce * 0.5
			else:
				velocity.y = -jumpForce * 0.7
		else:
			velocity.y = velocity.y * 0.1
	
	changeGravity()


func changeGravity():
	match currentState:
		movementState.flipGravity:
			currentGravity = gravity * 3
		movementState.jumpGravity:
			currentGravity = gravity * 2


func getState():
	return currentState
