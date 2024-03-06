extends Control
'''
Menu script for the Main Menu Scene 

@author Daniel Hibbin
'''

@onready var start_button = $"CanvasLayer/Main Menu/VBoxContainer/StartButton"
@onready var tutorial_button = $"CanvasLayer/Main Menu/VBoxContainer/TutorialButton"
@onready var canvas_layer = $CanvasLayer

# Reference to the world scene
const WORLD = preload("res://Scenes/world.tscn")

func _ready():
	if OS.has_feature('web'):
		
		var http_request = HTTPRequest.new()
		self.add_child(http_request)
		
		JavaScriptBridge.eval("""
			console.log('Javascript bridge is functional')
		""")
		
		print(IP.get_local_addresses())
		
		var custom_headers = [
			"Access-Control-Allow-Origin: *"
		]
		
		var error = http_request.request("http://localhost:8000/game/index.pck")
		if error == OK:
			print("Request successful!")
		else:
			print("An error occurred.")
		
	else:
		print("The JavaScriptBridge singleton is NOT available")


# When the "Start Game" button is pressed, 
func _on_button_pressed():
	get_tree().change_scene_to_packed(WORLD)
