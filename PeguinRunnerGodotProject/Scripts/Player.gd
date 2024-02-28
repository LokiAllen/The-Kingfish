extends CharacterBody2D
class_name Player

const SPEED = 300.0
const jumpForce = 750.0
const ROTATIONSPEED = 0.1

# Get the gravity from the project settings to be synced with RigidBody nodes.
var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")
var currentGravity = ProjectSettings.get_setting("physics/2d/default_gravity")

enum movementState {flipGravity, jumpGravity}
var currentState : movementState = movementState.jumpGravity

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


func _physics_process(delta):
	handleRotation()
	
	if alive:
		score += 1
		# Add the gravity.
		if not is_on_floor() or not is_on_ceiling():
			velocity.y += currentGravity * delta
		
		if invinsibleTimer > 0:
			invinsibleTimer -= 1
		
		# Handle movement state
		match currentState:
			movementState.flipGravity:
				if Input.is_action_just_pressed("ui_accept") and (is_on_floor() or is_on_ceiling()):
					if currentGravity > 0:
						animationPlayer.play("flip")
					else:
						animationPlayer.play_backwards("flip")
						
					currentGravity = -currentGravity
					velocity.y += currentGravity * delta
			movementState.jumpGravity:
				if Input.is_action_just_pressed("ui_accept"):
					velocity.y = -jumpForce
		
		
		var collision = move_and_slide()
		if collision and currentState == movementState.jumpGravity:
			kill()
		
		
		scoreCounter.text = "Score: %d" % score


func handleRotation():
	match currentState:
		movementState.flipGravity:
			penguinSprite.rotation = lerp(penguinSprite.rotation, 0.0, ROTATIONSPEED)
			wingPivot.rotation = lerp(wingPivot.rotation, 0.0, ROTATIONSPEED)
		movementState.jumpGravity:
			penguinSprite.rotation = lerp(penguinSprite.rotation, deg_to_rad(-45.0) * (-velocity.y / 1000), ROTATIONSPEED)
			wingPivot.rotation = lerp(wingPivot.rotation, deg_to_rad(-45.0) * (-velocity.y / 1000) * 2, ROTATIONSPEED)
			#if velocity.y < 0:
				#sprite.rotation = lerp(sprite.rotation, deg_to_rad(-35.0), ROTATIONSPEED)
			#else:
				#sprite.rotation = lerp(sprite.rotation, deg_to_rad(35.0), ROTATIONSPEED)


func changeState(newState : movementState):
	currentState = newState
	
	invinsibleTimer = invinsiblePhysicsFrames
	
	if newState == movementState.jumpGravity:
		if is_on_floor() or is_on_ceiling():
			if currentGravity < 0:
				velocity.y = jumpForce * 0.5
			else:
				velocity.y = -jumpForce * 0.7
		else:
			var centreDistance = (position.y + 200) / 200
			velocity.y = jumpForce * -centreDistance
		
		if currentGravity < 0:
			animationPlayer.play_backwards("flip")
	
	changeGravity()


func changeGravity():
	match currentState:
		movementState.flipGravity:
			currentGravity = gravity * 3
		movementState.jumpGravity:
			currentGravity = gravity * 2


func getState():
	return currentState


func kill():
	if invinsibleTimer <= 0:
		worldScroller.stop()
		alive = false
		deathAnimationPlayer.play("endGame")
		#returnButton.enable()
		finalScoreLabel.text = "Final Score: %d" % score
