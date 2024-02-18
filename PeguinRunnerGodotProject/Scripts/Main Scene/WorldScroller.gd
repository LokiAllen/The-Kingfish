extends Node2D

const TEST_CHUNK = preload("res://Scenes/Chunks/testChunk.tscn")

var rootChunkPosition = Vector2(0,0)
var chunkWidth = 17 * 2 * 70
var currentChunks : Array[TileMap]

# Called when the node enters the scene tree for the first time.
func _ready():
	for i in range(0,3):
		var newChunk = addChunk()
		newChunk.position = rootChunkPosition
		rootChunkPosition.x += chunkWidth

func addChunk():
	var newChunk = TEST_CHUNK.instantiate()
	add_child(newChunk)
	currentChunks.append(newChunk)
	return newChunk

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	rootChunkPosition.x = currentChunks[0].position.x
	print(currentChunks)
	if rootChunkPosition.x < -chunkWidth:
		remove_child(currentChunks[0])
		currentChunks = currentChunks.slice(1, len(currentChunks))
		var newChunk = addChunk()
		newChunk.position.x = currentChunks[len(currentChunks)-1].position.x + chunkWidth
	
	for chunk in currentChunks:
		chunk.position.x -= 1000 * delta
