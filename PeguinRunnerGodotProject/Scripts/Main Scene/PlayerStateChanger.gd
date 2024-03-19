extends Area2D
'''
PlayerStateChanger script for changing the player state when they enter an Area2D

@author Daniel Hibbin
'''


# Allow the target state to be changed in the editor for this class
@export var targetState : Player.movementState
@onready var animationPlayer = $AnimationPlayer
@onready var arrowPolygon = $arrows

func _ready():
	animationPlayer.play("scrollup")
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
