extends Node2D

const TEST_CHUNK = preload("res://Scenes/Chunks/testChunk2.tscn")

var rootChunkPosition = Vector2(0,0)
var chunkWidth = 16 * 2 * 16
var currentChunks : Array[TileMap]
var speed : float = 400.0
const chunkTime : float = 0.5
var chunkWaitTimer : float = 0.0

# Called when the node enters the scene tree for the first time.
func _ready():
	for i in range(0,10):
		var newChunk = addChunk()
		newChunk.position = rootChunkPosition
		rootChunkPosition.x += chunkWidth


func addChunk():
	var newChunk = TEST_CHUNK.instantiate()
	add_child(newChunk)
	currentChunks.append(newChunk)
	return newChunk


func _physics_process(delta):
	rootChunkPosition.x = currentChunks[0].position.x
	
	print(len(currentChunks))
	
	for chunk in currentChunks:
		chunk.position.x -= speed * delta
	
	if rootChunkPosition.x < -chunkWidth:
		remove_child(currentChunks[0])
		currentChunks = currentChunks.slice(1, len(currentChunks))
		rootChunkPosition = currentChunks[0].position
		var newChunk = addChunk()
		newChunk.position.x = currentChunks[len(currentChunks)-2].position.x + chunkWidth
