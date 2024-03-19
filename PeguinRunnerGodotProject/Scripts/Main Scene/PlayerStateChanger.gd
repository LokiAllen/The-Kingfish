'''
PlayerStateChanger script for changing the player state when they enter an Area2D
@author Daniel Hibbin
'''
extends Area2D
class_name PlayerStateChanger


# Allow the target state to be changed in the editor for this class
@export var targetState : Player.movementState


# Define references to the animation player and the polygon with the arrow texture
@onready var animationPlayer = $AnimationPlayer
@onready var arrowPolygon = $arrows


# Called when the node enters the scene tree for the first time.
func _ready():
	# Play the srcolling animation
	animationPlayer.play("scrollup")
	
	# Rotate the texture depending on the target rotation of this instance
	match targetState:
		Player.movementState.flipGravity:
			arrowPolygon.texture_rotation = PI
		Player.movementState.jumpGravity:
			arrowPolygon.texture_rotation = 0


# When the player enters this Area2D, change the state to the target state
func _on_body_entered(body):
	if body.is_in_group("player"):
		var player : Player = body
		body.changeState(targetState)
