extends Button

@export var SCENE = preload("res://Scenes/menu.tscn")

func enable():
	disabled = false


func _on_pressed():
	get_tree().change_scene_to_packed(SCENE)
