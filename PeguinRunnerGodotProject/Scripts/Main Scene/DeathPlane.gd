'''
DeathPlane script for Area2Ds that kill the player when they go off screen
@author Daniel Hibbin
'''
extends Area2D
class_name DeathPlane


# When the player enters the death plane, the plane attempts to kill the player
func onBodyEntered(body):
	if body.is_in_group("player"):
		body.kill()
