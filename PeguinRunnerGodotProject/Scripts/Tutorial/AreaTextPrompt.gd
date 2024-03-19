'''
Script for an Area2D that provides player with text prompt on enter
@author Daniel Hibbin
'''
extends Area2D
class_name AreaTextPrompt


# Instantiate varaibles for target label and text prompt
@export var targetLabel : Label
@export var textPrompt : String


# Called every physics frame
func _physics_process(delta):
	# For every overlapping body in the area
	for body in get_overlapping_bodies():
		# If the body is the player
		if body.is_in_group("player"):
			# Update the label text
			targetLabel.text = textPrompt
