#-*- coding:utf-8 -*-
import os
import sys
import json
import math

class Pos:
    MLG = 111319.49079327358
    MLT = 110946.25213273457
    def __init__(self,lat,lng,name="undefined"):
        self.lat = lat
        self.lng = lng
        self.name = name
    def GetDistance(self,targetpos):
        deltalat = targetpos.lat*self.MLT-self.lat*self.MLT 
        mcos = self.MLG*math.cos(math.radians(self.lat))
        deltalong = targetpos.lng*mcos-self.lng*mcos
        return ((deltalat)**2+(deltalong)**2)**0.5
    def CalculateTimeMS(self,targetpos,speed):
        return self.GetDistance(targetpos)/speed
    def CalculateTimeKMH(self,targetpos,speed):
        return self.GetDistance(targetpos)/(speed/3.6)
    def GetTargetDegree(self,targetpos):
        return math.degrees(self.GetTargetRadian(targetpos))
    def GetTargetRadian(self,targetpos):
        x=targetpos.lat-self.lat
        y=targetpos.lng-self.lng
        deg = math.atan2(y,x)
        return deg
    def SecondToHumanReadable(self,second):
        return time.strftime("%H:%M:%S", time.gmtime(second))
    def ShowGraph(self):
        pass
class Leocode:
    def __init__(self,db_name="tr.json"):
        self.DB=db_name
        self.ZoneList = []
    def IsLoaded(self):
        return len(self.ZoneList) > 0
    def LoadDB(self):
        if(os.path.isfile(self.DB)):
            with open(self.DB,"rb") as fp:
                try:
                    data = fp.read()
                    ZoneList=json.loads(data)
                    for zone in ZoneList:
                        self.ZoneList.append(
                            Pos(
                            float(zone["lat"]),
                            float(zone["lng"]),{
                                "city":zone["city"],
                                "admin":zone["admin"]
                            }
                        ))
                    return True
                except KeyboardInterrupt,e:
                    print(e)
                    return False
        else:
            return False
    def Compass(self,degrees):
        if(-22.5<=degrees<=22.5):return "[N] North"
        elif(22.5<degrees<=67.5):return "[NE] North East"
        elif(67.5<degrees<=112.5):return "[E] East"
        elif(112.5<degrees<=157.5):return "[SE] South East"
        elif(157.5<degrees or degrees<=-157.5):return "[S] South"
        elif(-157.5<degrees<=-112.5):return "[SW] South West"
        elif(-112.5<degrees<=-67.5):return "[W] West"
        elif(-67.5<degrees<=-22.5):return "[NS] North West"
    def Query(self,lat,lng):
        if(not self.IsLoaded()):
            if(not self.LoadDB()):
                return ""
        target = Pos(lat,lng)
        distances = []
        for zone in self.ZoneList:
            distances.append(zone.GetDistance(target))
        result = self.ZoneList[min(range(len(distances)),key=distances.__getitem__)]
        degree = result.GetTargetDegree(target)
        
        distance = result.GetDistance(target)/1000.0
        result_data=result.name
        result_s = "%.2f km of %s of %s (%s)"%(
            distance,
            self.Compass(degree),
            result_data["city"].encode("utf-8"),
            result_data["admin"].encode("utf-8").upper(),
            )
        return result_s
