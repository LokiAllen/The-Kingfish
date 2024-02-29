extends Control
'''
Menu script for the Main Menu Scene 

@author Daniel Hibbin
'''


# Reference to the world scene
const WORLD = preload("res://Scenes/world.tscn")


# When the "Start Game" button is pressed, 
func _on_button_pressed():
	get_tree().change_scene_to_packed(WORLD)
