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
		JavaScriptBridge.eval("""
			console.log('The JavaScriptBridge singleton is available')
		""")
		
		# Retrieve the `window.console` object.
		var console = JavaScriptBridge.get_interface("console")

		# Call the `window.console.log()` method.
		console.log("Hello, JavaScript console!")
		
		var http_request = HTTPRequest.new()
		self.add_child(http_request)

		var error = http_request.request("http://localhost:8000")
		if error == OK:
			print("Request successful!")
		else:
			print("An error occurred.")
		
	else:
		print("The JavaScriptBridge singleton is NOT available")


# When the "Start Game" button is pressed, 
func _on_button_pressed():
	get_tree().change_scene_to_packed(WORLD)
