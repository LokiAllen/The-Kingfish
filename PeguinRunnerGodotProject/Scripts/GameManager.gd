'''
Game Manager script for tracking high score and intefacing with Django
@author Daniel Hibbin
'''
extends Node


# Define js callback function and js object used to interface with django
var jsCallBack = JavaScriptBridge.create_callback(djangoCallback)
var djangoBridge : JavaScriptObject


# Define the javascript code used to interface with /game/data/user
const JAVASCRIPT_BRIDGE_BODY = """
var djangoBridge = {
	//Reference to the callback function in Godot
	callback: null,
	
	//Function to set the callback function of the djangoBridge
	setCallback: function(cb) {
		this.callback = cb;
	},
	
	//Function to get the user data from the game/data/user view
	getUserData: function() {
		fetch('data/user')
			.then(response => response.text())
			.then(data => {
				// Send the data back to GDScript.
				this.callback(JSON.stringify(data));
			})
			.catch(error => console.error('Error:', error));
	},
	
	//Function to set the user data in the game/data/user view
	setUserData: function(token, coins, highscore, cumulativeScore) {
		fetch('data/user/', {
				method: "POST", 
				credentials: 'same-origin',
				headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': token,
				},
				body: JSON.stringify({
					"coins": coins,
					"highscore": highscore,
					"cumulativeScore": cumulativeScore,
				})
			})
			.then(response => response.text())
			.then(data => {})
			.catch(error => console.error('Error:', error));
	},
	
	//Function to get cookies, used to get the CSRFToken of the current session
	getCookieValue: function(name) {
		const regex = new RegExp(`(^| )${name}=([^;]+)`)
		const match = document.cookie.match(regex)
		if (match) {
			return match[2]
		}
	}
};"""


# Initialise dictionaries to store the json data from the server and the current session
var sessionUserData : Dictionary = {"coins" : -1, "highscore" : -1, "cumulativeScore" : -1}
var serverUserData : Dictionary = {"coins" : -1, "highscore" : -1, "cumulativeScore" : -1}


# Called when the node enters the scene tree for the first time
func _ready():
	# If the game is running in a browser
	if OS.has_feature('web'):
		# Create the django bridge
		JavaScriptBridge.eval(JAVASCRIPT_BRIDGE_BODY, true)
		djangoBridge = JavaScriptBridge.get_interface("djangoBridge")
		
		# Set the callback for the djangoBridge object and get the user data from the server
		djangoBridge.setCallback(jsCallBack)
		djangoBridge.getUserData()


# Set highscore of current session
func setHighScore(score):
	# Update the highscore for the current session
	sessionUserData["highscore"] = score


# Get highscore of current session
func getCoinCount():
	# Return the coin count for the current session
	return sessionUserData["coins"]


# Send the session data to the server
func pushSessionData():
	# Get the CSRFToken 
	var csrfToken = djangoBridge.getCookieValue("csrftoken")
	
	# Decrement the number of coins in the user's account by 5
	sessionUserData["coins"] -= 5
	
	# If the highscore has been updated during gameplay
	if sessionUserData["highscore"] != serverUserData["highscore"]:
		# Update the cumulative score by adding the user highscore
		sessionUserData["cumulativeScore"] += sessionUserData["highscore"]
		
		# If the session highscore is not better than that user's best score
		if serverUserData["highscore"] > sessionUserData["highscore"]:
			# Replace the highscore with the highscore from the server
			sessionUserData["highscore"] = serverUserData["highscore"]
	
	# Send the session data to the server
	djangoBridge.setUserData(csrfToken, sessionUserData["coins"], sessionUserData["highscore"], 
		sessionUserData["cumulativeScore"])


# Godot function that is called by the djangoBridge JavaScript Object
func djangoCallback(args):
	# Clean the info and turn it into a dictionary
	# Note: for some reason the first call returns a cleaned string without any slash characters
	#		and the second call actually returns a dictionary that can be used, I dont know why
	var cleanedInfo = JSON.parse_string(args[0])
	var newUserInfo = JSON.parse_string(cleanedInfo)
	
	# For every key that we can update using the API defined for game/data/user
	for key in serverUserData.keys():
		# Set the server value to the value just retrieved from the server
		serverUserData[key] = newUserInfo[key]
	
	# Make the session data start off using the server data
	sessionUserData = serverUserData
	
