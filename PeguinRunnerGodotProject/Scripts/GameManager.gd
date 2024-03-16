extends Node

var js = JavaScriptBridge
var my_callback = JavaScriptBridge.create_callback(djangoCallback)
var django_bridge : JavaScriptObject

var javascript_bridge_body = """
var djangoBridge = {
	callback: null,
	setCallback: function(cb) {
		this.callback = cb;
	},
	getUserData: function() {
		fetch('data/user')
			.then(response => response.text())
			.then(data => {
				// Send the data back to GDScript.
				this.callback(JSON.stringify(data));
			})
			.catch(error => console.error('Error:', error));
	},
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
	getCookieValue: function(name) {
		const regex = new RegExp(`(^| )${name}=([^;]+)`)
		const match = document.cookie.match(regex)
		if (match) {
			return match[2]
		}
	}
};"""

var sessionUserData : Dictionary = {"coins" : -1, "highscore" : -1, "cumulativeScore" : -1}
var serverUserData : Dictionary = {"coins" : -1, "highscore" : -1, "cumulativeScore" : -1}


# Called when the node enters the scene tree for the first time.
func _ready():
	if OS.has_feature('web'):
		JavaScriptBridge.eval(javascript_bridge_body, true)
		django_bridge = JavaScriptBridge.get_interface("djangoBridge")
		django_bridge.setCallback(my_callback)
		django_bridge.getUserData()
		
		print("Django bridge has been established")
	else:
		print("The JavaScriptBridge singleton is NOT available")


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass


func setHighScore(score):
	sessionUserData["highscore"] = score


func getCoinCount():
	return sessionUserData["coins"]


func pushSessionData():
	print("pushing to server")
	var csrfToken = django_bridge.getCookieValue("csrftoken")
	
	sessionUserData["coins"] -= 5
	
	if sessionUserData["highscore"] > 0:
		sessionUserData["cumulativeScore"] = sessionUserData["highscore"] + serverUserData["cumulativeScore"]
		if serverUserData["highscore"] > sessionUserData["highscore"]:
			sessionUserData["highscore"] = serverUserData["highscore"]
	
	
	
	django_bridge.setUserData(csrfToken, sessionUserData["coins"], sessionUserData["highscore"], 
		sessionUserData["cumulativeScore"])
	print("pushed to server")
	

func djangoCallback(args):
	var jsonParser = JSON.new()
	
	var cleanedInfo = jsonParser.parse_string(args[0])
	var newUserInfo = jsonParser.parse_string(cleanedInfo)
	
	for key in serverUserData.keys():
		serverUserData[key] = newUserInfo[key]
	
	sessionUserData = serverUserData
	
