extends Area2D

@export var targetLabel : Label
@export var textPrompt : String

func _physics_process(delta):
	for body in get_overlapping_bodies():
		if body.is_in_group("player"):
			targetLabel.text = textPrompt
