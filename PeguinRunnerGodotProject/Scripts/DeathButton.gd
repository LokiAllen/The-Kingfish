extends Button


func _process(delta):
	print(disabled)


func _on_pressed():
	get_tree().change_scene_to_file("res://Scenes/menu.tscn")


func _on_button_pressed():
	print("bozo")
