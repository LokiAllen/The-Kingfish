extends Control
'''
Menu script for the Main Menu Scene 

@author Daniel Hibbin
'''

@onready var start_button = $"CanvasLayer/Main Menu/VBoxContainer/StartButton"
@onready var tutorial_button = $"CanvasLayer/Main Menu/VBoxContainer/TutorialButton"
@onready var canvas_layer = $CanvasLayer

var js = JavaScriptBridge
var my_callback = JavaScriptBridge.create_callback(_on_my_callback)

# Reference to the world scene
const WORLD = preload("res://Scenes/world.tscn")

func _ready():
	if OS.has_feature('web'):
		
		# Define the JavaScript code.
		
		
		JavaScriptBridge.eval("""
		var godotBridge = {
			callback: null,
			setCallback: function(cb) {
				this.callback = cb;
			},
			test: function(data) {
				this.callback(JSON.stringify(data));
			},
			makeRequest: function() {
				fetch('index.pck')
					.then(response => response.text())
					.then(data => {
						// Send the data back to GDScript.
						this.callback(data);
					})
					.catch(error => console.error('Error:', error));
			}
		};""", true)
		var godot_bridge = JavaScriptBridge.get_interface("godotBridge")
		godot_bridge.setCallback(my_callback)
		godot_bridge.makeRequest()
		
	else:
		print("The JavaScriptBridge singleton is NOT available")
		
		


func _on_my_callback(args) -> void:
	print(args)
	


# When the "Start Game" button is pressed, 
func _on_button_pressed():
	get_tree().change_scene_to_packed(WORLD)
