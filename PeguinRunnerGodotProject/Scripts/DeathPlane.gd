extends Area2D
'''
DeathPlane script for Area2Ds that kill the player when they go off screen

@author Daniel Hibbin
'''


# When the player enters the death plane, the plane attempts to kill the player
func _on_body_entered(body):
	if body.is_in_group("player"):
			body.kill()
