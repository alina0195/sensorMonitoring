from fastapi import FastAPI
import random
from time import sleep
from pydantic import BaseModel

limits={
    'presiune': {"min":1,"max":30},
    'tensiune': {'min':190,"max":280},
    'curent': {'min':0,'max':800}
}



class SetMinMaxRequest(BaseModel):
    senzorName: str
    minVal: int
    maxVal: int

app=FastAPI()

@app.get('/')
def read_root():
    global limits
    print('Reading from root')
    p = random.randint(limits['presiune']['min'],limits['presiune']['max'])
    v = random.randint(limits['tensiune']['min'],limits['tensiune']['max'])
    c =random.randint(limits['curent']['min'],limits['curent']['max'])
    return {'Presiune':p, 'Tensiune':v, 'Curent':c }


@app.post('/minmax')
def set_minmax(minMaxReq: SetMinMaxRequest):
    print('Reading from minmax request')
    print(minMaxReq.senzorName)
    print(minMaxReq.minVal)
    print(minMaxReq.maxVal)    
    if(minMaxReq.senzorName):
        limits[minMaxReq.senzorName]['min'] = minMaxReq.minVal
        limits[minMaxReq.senzorName]['max'] = minMaxReq.maxVal
    return minMaxReq


read_root()