'''
DeathButton script for the button that is displayed when the player dies
@author Daniel Hibbin
'''
extends Button
class_name DeathButton


# Define target scene that can be changed in the editor
@export var targetScene : Resource = preload("res://Scenes/menu.tscn")


# When the death button is pressed, the target scene is opened
func _on_pressed():
	get_tree().change_scene_to_packed(targetScene)
