'''
DeathButton script for the button that is displayed when the player dies
@author Daniel Hibbin
'''
extends Button
class_name DeathButton


# Define path to target scene that can be changed in the editor
@export var targetScene : String = "res://Scenes/menu.tscn"
# Note: a path string is used instead of a resource because a resource would cause a recursive dependency


# When the death button is pressed, the target scene is opened
func onButtonPressed():
	get_tree().change_scene_to_file(targetScene)
