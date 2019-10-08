import json

def verificar(m, r):
    """ Verifica el mensaje recibido por MQTT, aplicando banderas de limpieza.\n
        m: Mensaje recibido por MQTT (payload)\n
        r: Json usado para tomar las referencias de las mediciones\n
        return: Mensaje str (json) validado """
    data = toDict(m)

    rangos = r

    banderaLimpieza(data, rangos)
    
    return data
    #return toStr(data)
    
def toDict(fileBytes):
    """ Convertir un dato tipo bytes to dict.\n
        fileBytes: mensaje tipo bytes a convertir """
    fileStr = str(fileBytes.decode("utf-8"))
    return json.loads(fileStr)

def toStr(fileDict):
    """ Convertir un dato tipo dict (python object) to str (json).\n
        fileDict: mensaje tipo dict a convertir """
    strJson = json.dumps(fileDict)
    return strJson

def banderaLimpieza(data, rangos):
    """ Agrega la bandera de limpieza a cada medicion.\n
    data: Mensaje\n
    rangos: Json usado para tomar las referencias de las mediciones"""
    for d in data["mediciones"]:        
        if (d["valor"] == "null") or (d["valor"] == "NULL") or (d["valor"] == "Null"):
            d["bLimpieza"] = "ND"
        else:
            valor = float(d["valor"])
            if d["idParametro"] in rangos["limites"]:
                if (valor >= rangos["limites"][d["idParametro"]]["min"]) and (valor <= rangos["limites"][d["idParametro"]]["max"]) and (valor >= 0):
                    d["bLimpieza"] = "VA"
                elif (valor >= rangos["limites"][d["idParametro"]]["min"]) and (valor <= rangos["limites"][d["idParametro"]]["max"]) and (valor < 0):
                    d["bLimpieza"] = "VZ"
                elif (valor < rangos["limites"][d["idParametro"]]["min"]) or (valor > rangos["limites"][d["idParametro"]]["max"]):
                    d["bLimpieza"] = "IR"