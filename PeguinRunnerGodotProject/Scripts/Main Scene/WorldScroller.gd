'''
WorldScroller script for the endless scrolling of the game world
@author Daniel Hibbin
'''
extends Node2D
class_name WorldScroller


# Define constant lists of all chunk types, using the getPackedScenesInDirectory() function doesn't
# work in the browser
const FLIP_CHUNKS : Array[Resource] = [
	preload("res://Scenes/Chunks/FlipChunks/flipChunk1.tscn"),
	preload("res://Scenes/Chunks/FlipChunks/flipChunk2.tscn"),
	preload("res://Scenes/Chunks/FlipChunks/flipChunk2 (2).tscn")
]

const JUMP_CHUNKS : Array[Resource] = [
	preload("res://Scenes/Chunks/JumpChunks/jumpChunk1.tscn"),
	preload("res://Scenes/Chunks/JumpChunks/jumpChunk2.tscn"),
	preload("res://Scenes/Chunks/JumpChunks/jumpChunk3.tscn"),
	preload("res://Scenes/Chunks/JumpChunks/jumpChunk4.tscn"),
	preload("res://Scenes/Chunks/JumpChunks/jumpChunk5.tscn")
]
const FLIP_TRANSITION_CHUNKS : Array[Resource] = [
	preload("res://Scenes/Chunks/FlipTransitionChunks/testStartFlip.tscn")
]
const JUMP_TRANSITION_CHUNKS : Array[Resource] = [
	preload("res://Scenes/Chunks/JumpTransitionChunks/testStartJump.tscn")
]


# Reference to chunks that are safe to spawn the player in
const STARTING_CHUNK : Resource = preload("res://Scenes/Chunks/testChunk2.tscn")


# Varaibles for handling the chunks
var rootChunkPosition = Vector2(0,0)
const CHUNK_WIDTH = 512
var currentChunks : Array[TileMap]


# Speed of chunk movement variables and chance of transition
var speed : float = 380.0
const MAX_SPEED : float = 410.0
const ACCELERATION : float = 0.5
var transitionChance : float = 0.2


# Current target state for chunks current being spawned in
var targetMovementState : Player.movementState = Player.movementState.flipGravity


# Boolean for if the player is dead, this is set to true on start in the tutorial level
@export var dead : bool = false


# References to foreground and to animation player that scrolls the background texture
@onready var foreground = $Foreground
@onready var backgroundAnimation = $Background2/AnimationPlayer


# Varaible defining render distance of chunks
var renderDistance = 3


# Called when the node enters the scene tree for the first time.
func _ready():
	# Start scrolling background
	backgroundAnimation.play("scroll")
	
	# Create new chunks on game start, if not started as dead
	if !dead:
		# Set the starting position according to the renderdistance
		rootChunkPosition.x = -CHUNK_WIDTH * renderDistance
		
		# Iterating through the render distance, spawn in chunks
		for i in range(0, renderDistance*2):
			var newChunk
			# If the chunk is ahead of the player, spawn in a flip chunk, otherwise spawn in a starting chunk
			if rootChunkPosition.x > CHUNK_WIDTH:
				newChunk = addChunk(FLIP_CHUNKS.pick_random())
			else:
				newChunk = addChunk(STARTING_CHUNK)
			# Set the position of the new chunk and increment the root position
			newChunk.position = rootChunkPosition
			rootChunkPosition.x += CHUNK_WIDTH


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
		speed = max(speed, MAX_SPEED)
		
		# Move the chunk positions according to the speed and time between physics frames
		for chunk in currentChunks:
			chunk.position.x -= speed * delta
		
		
		# If the oldest chunk is off screen by more than the width of a chunk
		if rootChunkPosition.x < -CHUNK_WIDTH * 2:
			# Remove the oldest chunk and adjust the rootChunkPosition
			foreground.remove_child(currentChunks[0])
			currentChunks = currentChunks.slice(1, len(currentChunks))
			rootChunkPosition = currentChunks[0].position
			
			
			# Create a new chunk, choosing a transition chunk or a normal chunk
			var newChunk
			if isChunkTransition():
				# If transitioning, flip the target state and add a transition to that state
				if targetMovementState == Player.movementState.flipGravity:
					newChunk = addChunk(JUMP_TRANSITION_CHUNKS.pick_random())
					targetMovementState = Player.movementState.jumpGravity
				else:
					newChunk = addChunk(FLIP_TRANSITION_CHUNKS.pick_random())
					targetMovementState = Player.movementState.flipGravity
			else:
				# Otherwise get a new chunk for the current movement state
				if targetMovementState == Player.movementState.flipGravity:
					newChunk = addChunk(FLIP_CHUNKS.pick_random())
				else:
					newChunk = addChunk(JUMP_CHUNKS.pick_random())
			
			
			# Set the position of the new chunk to be 1 chunk in front of the previously added chunk
			newChunk.position.x = currentChunks[len(currentChunks)-2].position.x + CHUNK_WIDTH 


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


# Function that gets all of the packed scenes in a given directory
func getPackedScenesInDirectory(path : String):
	# Open the directory and define the array of packed scenes
	var dir = DirAccess.open(path)
	var packedSceneArray : Array[Resource] = []
	
	# If the directory was opened, parse through its contents
	if dir:
		# Begin parsing through the contents
		dir.list_dir_begin()
		var fileName = dir.get_next()
		
		# Whilst parsing has not finished, continue parsing
		while fileName != "":
			# If the current file is not a directory, append it to the array of packed scenes
			if !dir.current_is_dir():
				packedSceneArray.append(load(path+"/"+fileName))
			# Get the next file
			fileName = dir.get_next()
	else:
		# Otherwise print an error message to the console
		print("Error has occured trying to access the path")
	
	# Return the array of packed scenes
	return packedSceneArray
