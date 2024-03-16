extends Control
'''
Menu script for the Main Menu Scene 

@author Daniel Hibbin
'''

@onready var coinsLabel = $"CanvasLayer/Main Menu/VBoxContainer2/HBoxContainer/Coins Label"
@onready var playableLabel = $"CanvasLayer/Main Menu/VBoxContainer2/HBoxContainer/Playable Label"
@onready var startButton = $"CanvasLayer/Main Menu/VBoxContainer/StartButton"

@onready var audioStreamPlayer = $AudioStreamPlayer
@onready var titleAnimaiton = $"CanvasLayer/Main Menu/VBoxContainer2/Title/AnimationPlayer"


# Reference to the world scene
const WORLD = preload("res://Scenes/world.tscn")
const TUTORIAL = preload("res://Scenes/tutorial.tscn")

func _ready():
	titleAnimaiton.play("title")


func _process(delta):
	if OS.has_feature('web'):
		var coins = GameManager.getCoinCount()
		coinsLabel.text = "Coins: %d" % coins
		if coins >= 5:
			playableLabel.text = "You can play!"
			startButton.disabled = false
		else:
			playableLabel.text = "You can't play. :("
			startButton.disabled = true
	
	if audioStreamPlayer.playing == false:
		audioStreamPlayer.play()
	


# When the "Start Game" button is pressed, 
func _on_startButton_pressed():
	get_tree().change_scene_to_packed(WORLD)


#When the "Play Tutorial" button is pressed
func _on_tutorialButton_pressed():
	get_tree().change_scene_to_packed(TUTORIAL)
