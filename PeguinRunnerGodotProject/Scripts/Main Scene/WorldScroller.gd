extends Node2D
'''
WorldScroller script for the scrolling of the game world

@author Daniel Hibbin
'''


# List of chunks for the flipping movement state
const flipChunks : Array[Resource] = [
	preload("res://Scenes/Chunks/FlipChunks/flipChunk1.tscn"),
	preload("res://Scenes/Chunks/FlipChunks/flipChunk2.tscn"),
	preload("res://Scenes/Chunks/FlipChunks/flipChunk2 (2).tscn")
]


# List of chunks for the jumping movement state
const jumpChunks : Array[Resource] = [
	preload("res://Scenes/Chunks/JumpChunks/jumpChunk1.tscn"),
	preload("res://Scenes/Chunks/JumpChunks/jumpChunk2.tscn"),
	preload("res://Scenes/Chunks/JumpChunks/jumpChunk3.tscn"),
	preload("res://Scenes/Chunks/JumpChunks/jumpChunk4.tscn"),
	preload("res://Scenes/Chunks/JumpChunks/jumpChunk5.tscn")
]


# List of chunks to transition the player into the flip movement state
const flipTransitionChunks : Array[Resource] = [
	preload("res://Scenes/Chunks/TransitionChunks/testStartFlip.tscn")
]


# List of chunks to transition the player into the jump movement state
const jumpTransitionChunks : Array[Resource] = [
	preload("res://Scenes/Chunks/TransitionChunks/testStartJump.tscn")
]

# Reference to chunks that are safe to spawn the player in
const startingChunk : Resource = preload("res://Scenes/Chunks/testChunk2.tscn")


# Varaibles for handling the chunks
var rootChunkPosition = Vector2(0,0)
var chunkWidth = 512
var currentChunks : Array[TileMap]


# Speed of chunk movement and chance of transition
var speed : float = 380.0
const MAXSPEED : float = 410.0
const ACCELERATION : float = 0.5
var transitionChance : float = 0.25


# Current target state for chunks current being spawned in
var targetMovementState : Player.movementState = Player.movementState.flipGravity


# Boolean for if the player is dead, this is set to true on start in the tutorial level
@export var dead : bool = false


# References to parent of background objects and foreground objects
@onready var foreground = $Foreground
@onready var backgroundAnimation = $Background2/AnimationPlayer
var renderDistance = 3


# Called when the node enters the scene tree for the first time.
func _ready():
	# Start scrolling background
	backgroundAnimation.play("scroll")
	
	# Create new chunks on game start
	if !dead:
		rootChunkPosition.x = -chunkWidth * renderDistance
		for i in range(0, renderDistance*2):
			var newChunk = flipChunks.pick_random() 
			if rootChunkPosition.x > chunkWidth:
				newChunk = addChunk(flipChunks.pick_random())
			else:
				newChunk = addChunk(startingChunk)
			newChunk.position = rootChunkPosition
			rootChunkPosition.x += chunkWidth


# Adds a chunk to the foreground and list of chunks
func addChunk(targetChunk : Resource):
	var newChunk = targetChunk.instantiate()
	foreground.add_child(newChunk)
	currentChunks.append(newChunk)
	return newChunk


# Called every physics frame
func _physics_process(delta):
	# If the player isn't dead, perform the scrolling of the world and background
	if !dead:		
		# Set the root chunk position to the first chunk of the current chunks
		rootChunkPosition.x = currentChunks[0].position.x
		speed += ACCELERATION * delta
		speed = max(speed, MAXSPEED)
		
		# Move the chunk positions according to the speed and time between physics frames
		for chunk in currentChunks:
			chunk.position.x -= speed * delta
		
		
		# If the oldest chunk is off screen by more than the width of a chunk
		if rootChunkPosition.x < -chunkWidth * 2:
			# Remove the oldest chunk and adjust the rootChunkPosition
			foreground.remove_child(currentChunks[0])
			currentChunks = currentChunks.slice(1, len(currentChunks))
			rootChunkPosition = currentChunks[0].position
			
			
			# Create a new chunk, choosing a transition chunk or a normal chunk
			var newChunk
			if isChunkTransition():
				# If transitioning, flip the target state and add a transition to that state
				if targetMovementState == Player.movementState.flipGravity:
					newChunk = addChunk(jumpTransitionChunks.pick_random())
					targetMovementState = Player.movementState.jumpGravity
				else:
					newChunk = addChunk(flipTransitionChunks.pick_random())
					targetMovementState = Player.movementState.flipGravity
			else:
				# Otherwise get a new chunk for the current movement state
				if targetMovementState == Player.movementState.flipGravity:
					newChunk = addChunk(flipChunks.pick_random())
				else:
					newChunk = addChunk(jumpChunks.pick_random())
			
			
			# Set the position of the new chunk to be 1 chunk in front of the previously added chunk
			newChunk.position.x = currentChunks[len(currentChunks)-2].position.x + chunkWidth 


# Returns true if it is time to transition to a new movement state
func isChunkTransition():
	# Uses transitionChnace to create a new integer in random range, if 1, the scroller will transition
	# to a new state
	if randi_range(1, 1/transitionChance) == 1:
		return true
	else:
		return false


# Stop scrolling the world
func stop():
	dead = true
