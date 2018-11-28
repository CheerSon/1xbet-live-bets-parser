import sys
import requests
try:
	from Onexbet_lib import *
	from Onexbet_lib import Verbose as v
except ImportError:
	EchoError("Error on lib import. Check lib existence.") #get us to know that there is no Onexbet_lib out there.
	sys.exit()

__OneXbetLiveLink = "https://1xtkyp.host/ru/live/" # defines the link to the live bets of 1xbet.
__GateLink = "http://127.0.0.1:8000/receive_data" # defines gate link where script will send data per bet.
__AuthKey = "12345678"
__TimeOutTime = 2 # defines time in mins how much time script will wait before the next request
__Kontora = "OneXbet"
__Sports_Array = ["Football", "Ice-Hockey", "Basketball", "Volleyball", "Baseball", "Tennis", "Table-Tennis"]
# why '__' before variable names? - It means that this is a global variable, so it will be easier to declare new variables within funcs and also it would be helpful to clearly understand where this variable located in the code.

#args: -D(DebugOutput); -V(EchoVerbose)
def FormatForJson(team1_name, team2_name, _1coeff, _2coeff, _1xcoeff, _2xcoeff, _xcoeff, _12coeff, _namesp, _link):
	json = {"auth": __AuthKey,
		  "kontora": __Kontora,
		  "sport": _namesp,
		  "url": _link,
		  "team1": team1_name,
		  "team2": team2_name,
		  "team1_koef": {
			"team_win": _1coeff,
			"team_draw": _1xcoeff
		  },
		  "team2_koef": {
			"team_win": _2coeff,
			"team_draw": _2xcoeff
		  },
		  "general": {
			"draw": _xcoeff,
			"t1t2": _12coeff
		  }
		}
	return json
def SendJsonToGate(json):
	try:
		httpResp = requests.post(__GateLink, json=json)
		v.EchoDebug(str(httpResp.status_code))
	except:
		v.EchoError("Error achieved on gate requesting!")
		pass
def MainRoutine():
	v.EchoVerbose("Script started successfuly!")
	v.EchoDebug("Entered MainRoutine!")
	while True:
		page = get_page(__OneXbetLiveLink)
		v.EchoVerbose("Got the page!")
		events = Get_C_events(page)
		v.EchoVerbose("Count of bets on the page: " + str(len(events)))
		for x in range(0, len(events)):
			if ValidateDiv(events[x]) == True:
				names = Get_Name_of_Sport(events[x])	
				json = FormatForJson(names[0], names[1], Get_Coeff(events[x], "1"), Get_Coeff(events[x], "2"), Get_Coeff(events[x], "1x"), Get_Coeff(events[x], "2x"), Get_Coeff(events[x], "x"), Get_Coeff(events[x], "12"), Get_Sport_Type(events[x],__Sports_Array), Get_Event_Link(events[x]))
				SendJsonToGate(json)
				v.EchoDebug(str(json))
			else:
				v.EchoWarning("Got broken div! Skipping it!")
		v.EchoVerbose("All sent! Waiting " + str(__TimeOutTime) + " min(s).")
		time.sleep(__TimeOutTime*60)
if __name__ == "__main__":
	if len(sys.argv) == 1:
		print("This script supports arguments! Argument list: -V(will show additional info in the console) -D(will show debug info)")
	MainRoutine()