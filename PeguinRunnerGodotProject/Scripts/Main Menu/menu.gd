'''
Menu script for the Main Menu Scene 
@author Daniel Hibbin
'''
extends Control
class_name CustomGameMenu


# Define references to all necessary objects in the main menu scene
@onready var coinsLabel = $"CanvasLayer/Main Menu/VBoxContainer2/HBoxContainer/Coins Label"
@onready var playableLabel = $"CanvasLayer/Main Menu/VBoxContainer2/HBoxContainer/Playable Label"
@onready var startButton = $"CanvasLayer/Main Menu/VBoxContainer/StartButton"
@onready var audioStreamPlayer = $AudioStreamPlayer
@onready var titleAnimaiton = $"CanvasLayer/Main Menu/VBoxContainer2/Title/AnimationPlayer"


# Reference to the world and tutorial scenes
const WORLD = preload("res://Scenes/world.tscn")
const TUTORIAL = preload("res://Scenes/tutorial/tutorial.tscn")


# Called when the node enters the scene tree for the first time
func _ready():
	# Play the animation for the title text
	titleAnimaiton.play("title")


# Called every frame
func _process(delta):
	# If running in a browser
	if OS.has_feature('web'):
		# Get coin count from server and set the label text
		var coins = GameManager.getCoinCount()
		coinsLabel.text = "Coins: %d" % coins
		
		# If the player has more than 5 coins
		if coins >= 5:
			# Update the label and allow them to start the game
			playableLabel.text = "You can play for 5 coins!"
			startButton.disabled = false
		else:
			# Otherwise, update the label and do not allow them to start
			playableLabel.text = "You can't play. :("
			startButton.disabled = true
	
	# If the audio stream doesn't start for whatever reason, start it
	if audioStreamPlayer.playing == false:
		audioStreamPlayer.play()


# When the "Start Game" button is pressed, change to the world scene
func onStartButtonPressed():
	get_tree().change_scene_to_packed(WORLD)


#When the "Play Tutorial" button is pressed, change to the tutorial scene
func onTutorialButtonPressed():
	get_tree().change_scene_to_packed(TUTORIAL)
