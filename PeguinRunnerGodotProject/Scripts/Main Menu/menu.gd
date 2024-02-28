extends Control

const WORLD = preload("res://Scenes/world.tscn")

func _on_button_pressed():
	get_tree().change_scene_to_packed(WORLD)
