extends Button
# DeathButton script for the button that is displayed when the player dies


# When the death button is pressed, the menu scene is opened
func _on_pressed():
	get_tree().change_scene_to_file("res://Scenes/menu.tscn")
