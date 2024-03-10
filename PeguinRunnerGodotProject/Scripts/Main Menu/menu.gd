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
var django_bridge : JavaScriptObject

# Reference to the world scene
const WORLD = preload("res://Scenes/world.tscn")

func _ready():
	if OS.has_feature('web'):
		
		# Define the JavaScript code.
		
		
		JavaScriptBridge.eval("""
		var djangoBridge = {
			callback: null,
			setCallback: function(cb) {
				this.callback = cb;
			},
			getUserData: function() {
				fetch('data/user')
					.then(response => response.text())
					.then(data => {
						// Send the data back to GDScript.
						this.callback(JSON.stringify(data));
					})
					.catch(error => console.error('Error:', error));
			},
			setUserData: function(jsonbody) {
				fetch('data/user/', {
						method: "POST", 
						credentials: 'same-origin',
						headers: {
							'Content-Type': 'application/json',
							'X-CSRFToken': "MwPgaUTEi49bSl5IGx4EkyueGV9mBKel",
						},
						body: JSON.stringify({
							"coins": 0,
							"highscore": 0,
							"cumulativeScore": 0,
						})
					})
					.then(response => response.text())
					.then(data => {})
					.catch(error => console.error('Error:', error));
			}
		};""", true)
		django_bridge = JavaScriptBridge.get_interface("djangoBridge")
		django_bridge.setCallback(my_callback)
		django_bridge.getUserData()
		
		
	else:
		print("The JavaScriptBridge singleton is NOT available")


func _on_my_callback(args) -> void:
	var jsonParser = JSON.new()
	print(jsonParser.parse_string(args[0]))
	
	jsonParser.parse(args[0])
	var userInfo = jsonParser.data
	print(typeof(userInfo))
	print(userInfo)
	
	JavaScriptBridge.eval("console.log(document.cookie)")
	django_bridge.setUserData(jsonParser.parse_string(args[0]))
	




# When the "Start Game" button is pressed, 
func _on_button_pressed():
	get_tree().change_scene_to_packed(WORLD)
