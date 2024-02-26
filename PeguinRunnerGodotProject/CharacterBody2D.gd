extends CharacterBody2D


const SPEED = 300.0
const jumpForce = 750.0

# Get the gravity from the project settings to be synced with RigidBody nodes.
var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")
var currentGravity = ProjectSettings.get_setting("physics/2d/default_gravity")

enum movementState {flipGravity, jumpGravity}
var currentState : movementState = movementState.jumpGravity

func _ready():
	changeGravity()

func changeGravity():
	match currentState:
		movementState.flipGravity:
			currentGravity = gravity * 3
		movementState.jumpGravity:
			currentGravity = gravity * 2

func _physics_process(delta):
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

	# Handle recentering with velocity.x or position.x

	move_and_slide()
