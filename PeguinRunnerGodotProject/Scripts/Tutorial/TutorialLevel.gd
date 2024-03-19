'''
Script that moves the tutorial level
@author Daniel Hibbin
'''
extends Node2D
class_name TutorialLevel


# Define variable for speed
@export var speed : float = 380.0


# Called every physics frame
func _physics_process(delta):
	# Move the level to the left according to speed and time between physics frames
	position.x -= speed * delta
