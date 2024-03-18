extends Node2D

var speed : float = 380.0



func _physics_process(delta):
	position.x -= speed * delta
