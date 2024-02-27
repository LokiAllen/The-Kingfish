extends Node2D

const flipChunks : Array[Resource] = [
	preload("res://Scenes/Chunks/FlipChunks/flipChunk1.tscn")
]

const jumpChunks : Array[Resource] = [
	preload("res://Scenes/Chunks/JumpChunks/jumpChunk1.tscn")
]

const flipTransitionChunks : Array[Resource] = [
	preload("res://Scenes/Chunks/TransitionChunks/testStartFlip.tscn")
]

const jumpTransitionChunks : Array[Resource] = [
	preload("res://Scenes/Chunks/TransitionChunks/testStartJump.tscn")
]

const startingChunk : Resource = preload("res://Scenes/Chunks/testChunk2.tscn")

var rootChunkPosition = Vector2(0,0)
var chunkWidth = 16 * 2 * 16
var currentChunks : Array[TileMap]
var speed : float = 400.0
var transitionChance : float = 0.25

var targetMovementState : Player.movementState = Player.movementState.flipGravity
var dead : bool = false

# Called when the node enters the scene tree for the first time.
func _ready():
	
	
	for i in range(0,3):
		var newChunk = addChunk(startingChunk)
		newChunk.position = rootChunkPosition
		rootChunkPosition.x += chunkWidth


func addChunk(targetChunk : Resource):
	var newChunk = targetChunk.instantiate()
	add_child(newChunk)
	currentChunks.append(newChunk)
	return newChunk


func _physics_process(delta):
	rootChunkPosition.x = currentChunks[0].position.x
	
	if !dead:
		for chunk in currentChunks:
			chunk.position.x -= speed * delta
	
	if rootChunkPosition.x < -chunkWidth:
		remove_child(currentChunks[0])
		currentChunks = currentChunks.slice(1, len(currentChunks))
		rootChunkPosition = currentChunks[0].position
		
		
		var newChunk
		if isChunkTransition():
			if targetMovementState == Player.movementState.flipGravity:
				newChunk = addChunk(jumpTransitionChunks.pick_random())
				targetMovementState = Player.movementState.jumpGravity
			else:
				newChunk = addChunk(flipTransitionChunks.pick_random())
				targetMovementState = Player.movementState.flipGravity
		else:
			if targetMovementState == Player.movementState.flipGravity:
				newChunk = addChunk(flipChunks.pick_random())
			else:
				newChunk = addChunk(jumpChunks.pick_random())
				
		
		
		newChunk.position.x = currentChunks[len(currentChunks)-2].position.x + chunkWidth


func isChunkTransition():
	if randi_range(1, 1/transitionChance) == 1:
		return true
	else:
		return false


func stop():
	dead = true
