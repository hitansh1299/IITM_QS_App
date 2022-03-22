import sqlite3
from datetime import datetime, timedelta
import json
import random
moods_string = '''
    {
    "HAPPY":[{
    "Joyous" : "1f602",
    "Excited" : "1f973",
    "Connected" : "1f970",
    "Animated" : "1f92a",
    "Playful" : "1f609"
    },"rgba(255,235,42,0.4)"],
    
    "SAD":[{
    "Embarrassed" : "1f62c",
    "Isolated" : "1f614",
    "Heartbroken" : "1f494",
    "Guilty" : "1f92d",
    "Apathetic" : "1f61e"
    },"rgba(42,59,144,0.4)"],
    
    "ANGRY":[{
    "Hurt" :"1f915",
    "Frustrated" : "1f92c",
    "Disgusted" : "1f92e",
    "Angry" : "1f621",
    "Hateful" : "1f612"
    },"rgba(184,47,47,0.4)"],
    
    "FEAR":[{
    "Controlled" : "1f616",
    "Confused" : "1f914",
    "Anxious" : "1f630",
    "Overwhelmed" : "1f97a",
    "Helpless" : "2639-fe0f"
    },"rgba(70,36,76,0.4)"],
    
    "LOVED":[{
    "Content" : "1f60c",
    "Affectionate" : "1f618",
    "Cherished" : "1f604",
    "Compassionate" : "1f917",
    "Calm" : "1f607"
    },"rgba(255, 85, 157, 0.4)"],
    
    "MOTIVATED":[{
    "Aware" : "1f4a1",
    "Confident" :"1f60e",
    "Empowered" : "1f4aa",
    "Appreciated" : "1f4af",
    "Worthy" : "1f4b0"
    },"rgba(63, 168, 64, 0.4)"]
    }
    '''
moods = json.loads(moods_string)
def get_time(string):
    return datetime.fromisoformat(string).strftime("%a, %d %b, %Y, %H:%M")




if __name__ == '__main__':
    date = datetime(2022, 1, 1)
    mood = dict(moods)
    while date < datetime(2023, 1, 1):
        gen_mood = list(mood.keys())[random.randint(0, 5)]
        spec_mood = list(mood[gen_mood][0].keys())[random.randint(0, 4)]
        conn = sqlite3.connect("users.db")
        conn.execute("INSERT INTO Moods VALUES (?,?,?,?,?)", (
            "hitansh1299@gmail.com",
            str(date.isoformat()),
            gen_mood,
            spec_mood,
            ""
        ))
        conn.commit()

        date += timedelta(days=1)

