def Linear(AQIhigh, AQIlow, Conchigh, Conclow, Concentration):
    Conc = float(Concentration)
    a = ((Conc-Conclow) / (Conchigh-Conclow)) * (AQIhigh - AQIlow) + AQIlow
    linear=Math.round(a)
    return linear


def AQIPM25(Concentration):
    Conc = float(Concentration)
    AQI = 0
    c = (Math.floor(10 * Conc)) / 10
    if (c >= 0 and c < 12.1):
        AQI = Linear(50, 0, 12, 0, c)
    elif (c >= 12.1 and c < 35.5):
        AQI = Linear(100, 51, 35.4, 12.1, c)
    elif (c >= 35.5 and c < 55.5):
        AQI = Linear(150, 101, 55.4, 35.5, c)
    elif (c >= 55.5 and c < 150.5):
        AQI = Linear(200, 151, 150.4, 55.5, c)
    elif (c >= 150.5 and c < 250.5):
        AQI = Linear(300, 201, 250.4, 150.5, c)
    elif (c >= 250.5 and c < 350.5):
        AQI = Linear(400, 301, 350.4, 250.5, c)
    elif (c >= 350.5 and c < 500.5):
        AQI = Linear(500, 401, 500.4, 350.5, c)
    else:
        AQI = -999
    return AQI



def AQIPM10(Concentration):
    Conc = float(Concentration)
    AQI = 0
    c=Math.floor(Conc)
    if (c >= 0 and c < 55):
        AQI = Linear(50, 0, 54, 0, c)
    elif (c >= 55 and c < 155):
        AQI = Linear(100, 51, 154, 55, c)
    elif (c >= 155 and c < 255):
        AQI = Linear(150, 101, 254, 155, c)
    elif (c >= 255 and c < 355):
        AQI = Linear(200, 151, 354, 255, c)
    elif (c >= 355 and c < 425):
        AQI = Linear(300, 201, 424, 355, c)
    elif (c >= 425 and c < 505):
        AQI = Linear(400, 301, 504, 425, c)
    elif (c >= 505 and c < 605):
        AQI = Linear(500, 401, 604, 505, c)
    else:
        AQI = -999
    return AQI


def AQICO(Concentration):
    Conc = float(Concentration)
    AQI = 0
    c = (Math.floor(10 * Conc)) / 10
    if (c >= 0 and c < 4.5):
        AQI = Linear(50, 0, 4.4, 0, c)
    elif (c >= 4.5 and c < 9.5):
        AQI = Linear(100, 51, 9.4, 4.5, c)
    elif (c >= 9.5 and c < 12.5):
        AQI = Linear(150, 101, 12.4, 9.5, c)
    elif (c >= 12.5 and c < 15.5):
        AQI = Linear(200, 151, 15.4, 12.5, c)
    elif (c >= 15.5 and c < 30.5):
        AQI = Linear(300, 201, 30.4, 15.5, c)
    elif (c >= 30.5 and c < 40.5):
        AQI = Linear(400, 301, 40.4, 30.5, c)
    elif (c >= 40.5 and c < 50.5):
        AQI = Linear(500, 401, 50.4, 40.5, c)
    else:
        AQI = -999
    return AQI


def AQISO21hr(Concentration):
    Conc = float(Concentration)
    AQI = 0
    c=Math.floor(Conc)
    if (c >= 0 and c < 36):
        AQI = Linear(50, 0, 35, 0, c)
    elif (c >= 36 and c < 76):
        AQI = Linear(100, 51, 75, 36, c)
    elif (c >= 76 and c < 186):
        AQI = Linear(150, 101, 185, 76, c)
    elif (c >= 186 and c <=304):
        AQI = Linear(200, 151, 304, 186, c)
    elif (c >= 304 and c <=604):
        AQI = -999
    else:
        AQI = -999
    return AQI


def AQISO224hr(Concentration):
    Conc = float(Concentration)
    AQI = 0
    c=Math.floor(Conc)
    if (c >= 0 and c <=304):
        AQI = "SO224hrmessage"
    elif (c >= 304 and c < 605):
        AQI = Linear(300, 201, 604, 305, c)
    elif (c >= 605 and c < 805):
        AQI = Linear(400, 301, 804, 605, c)
    elif (c >= 805 and c <=1004):	
        AQI = Linear(500, 401, 1004, 805, c)
    else:
        AQI = -99
    return AQI


def AQIOzone8hr(Concentration):
    Conc = float(Concentration)
    AQI = 0
    c = (Math.floor(Conc))/1000
    if (c >= 0 and c < .055):
        AQI = Linear(50, 0, 0.054, 0, c)
    elif (c >= .055 and c < .071):
        AQI = Linear(100, 51, .070, .055, c)
    elif (c >= .071 and c < .086):
        AQI = Linear(150, 101, .085, .071, c)
    elif (c >= .086 and c < .106):
        AQI = Linear(200, 151, .105, .086, c)
    elif (c >= .106 and c < .201):
        AQI = Linear(300, 201, .200, .106, c)
    elif (c >= .201 and c < .605):
        AQI = "O3message"
    else:
        AQI = -99
    return AQI



def AQIOzone1hr(Concentration):
    Conc = float(Concentration)
    AQI = 0
    c = (Math.floor(Conc))/1000
    if (c >= 0 and c <=.124):
        AQI = "O31hrmessage"
    elif (c >= .125 and c < .165):
        AQI = Linear(150, 101, .164, .125, c)
    elif (c >= .165 and c < .205):
        AQI = Linear(200, 151, .204, .165, c)
    elif (c >= .205 and c < .405):
        AQI = Linear(300, 201, .404, .205, c)
    elif (c >= .405 and c < .505):
        AQI = Linear(400, 301, .504, .405, c)
    elif (c >= .505 and c < .605):
        AQI = Linear(500, 401, .604, .505, c)
    else:
        AQI = -99
    return AQI


def AQINO2(Concentration):
    Conc = float(Concentration)
    AQI = 0
    c = (Math.floor(Conc))/1000
    if (c >= 0 and c < .054):
        AQI = Linear(50, 0, .053, 0, c)
    elif (c >= .054 and c < .101):
        AQI = Linear(100, 51, .100, .054, c)
    elif (c >= .101 and c < .361):
        AQI = Linear(150, 101, .360, .101, c)
    elif (c >= .361 and c < .650):
        AQI = Linear(200, 151, .649, .361, c)
    elif (c >= .650 and c < 1.250):
        AQI = Linear(300, 201, 1.249, .650, c)
    elif (c >= 1.250 and c < 1.650):
        AQI = Linear(400, 301, 1.649, 1.250, c)
    elif (c >= 1.650 and c <= 2.049):
        AQI = Linear(500, 401, 2.049, 1.650, c)
    else:
        AQI = -99
    return AQI


def AQICategory(AQIndex):
    AQI = float(AQIndex)
    AQICategory = ""
    if (AQI <= 50):
        AQICategory = "Good"
    elif (AQI > 50 and AQI <= 100):
        AQICategory = "Moderate"
    elif (AQI > 100 and AQI <= 150):
        AQICategory = "Unhealthy for Sensitive Groups"
    elif (AQI > 150 and AQI <= 200):
        AQICategory = "Unhealthy"
    elif (AQI > 200 and AQI <= 300):
        AQICategory = "Very Unhealthy"
    elif (AQI > 300 and AQI <= 400):
        AQICategory = "Hazardous"
    elif (AQI > 400 and AQI <= 500):
        AQICategory = "Hazardous"
    else:
        AQICategory = "Out of Range"
    return AQICategory
