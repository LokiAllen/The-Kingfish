extends Area2D


# Allow the target state to be changed in the editor for this class
@export var targetState : Player.movementState


func _on_body_entered(body):
	if body.is_in_group("player"):
			var player : Player = body
			body.changeState(targetState)
