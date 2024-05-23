from enum import Enum
from typing import Generator
import yaml

# unDumped = [{'TIMESTEP':int, 'NUMBER OF ATOMS':int, 'BOX BOUNDS':dict, 'ATOMS':[dict specific to dump style]}]
# grid unDumped = 

class Modes(Enum):
    TIME = 1
    NUM = 2
    BOUNDS = 3
    ATOM = 4
    DIM = 5
    GRID_S = 6
    GRID_C = 7


def read_classic(file: str) -> Generator[dict[str:any], None, None]:
    """Generator object that yields one frame of the file at a time for classic style lammp dump files"""

    unDumped = {}
    loopCount = 0

    with open(file, "r") as myfile:
        for line in myfile:
            loopCount += 1
            if "TIMESTEP" in line:
                loopCount = 0
                mode = Modes.TIME
                checkLoop = loopCount
                unDumped = {"ATOMS": []}
            if mode == Modes.TIME and (loopCount - checkLoop) == 1:
                unDumped["TIMESTEP"] = int(line)
            if "NUMBER OF ATOMS" in line:
                mode = Modes.NUM
                checkLoop = loopCount
            if mode == Modes.NUM and (loopCount - checkLoop) == 1:
                unDumped["NUMBER OF ATOMS"] = int(line)
                frameLength = int(line)
            if "BOX BOUNDS" in line:
                mode = Modes.BOUNDS
                checkLoop = loopCount
                unDumped["BOX BOUNDS"] = {"x": [], "y": [], "z": []}
            if mode == Modes.BOUNDS and (loopCount - checkLoop) == 1:
                unDumped["BOX BOUNDS"]["x"] = line.split()
            if mode == Modes.BOUNDS and (loopCount - checkLoop) == 2:
                unDumped["BOX BOUNDS"]["y"] = line.split()
            if mode == Modes.BOUNDS and (loopCount - checkLoop) == 3:
                unDumped["BOX BOUNDS"]["z"] = line.split()
            if "ITEM: ATOMS" in line:
                mode = Modes.ATOM
                checkLoop = loopCount
                lengthCheck = 0
                v_line = line.split()
            if mode == Modes.ATOM and (loopCount - checkLoop) >= 1:
                lengthCheck += 1
                s_line = line.split()
                paraCount = 0
                atomDict = {}
                for para in v_line:
                    if para != "ATOMS" and para != "ITEM:":
                        atomDict[para] = s_line[paraCount]
                        paraCount += 1
                unDumped["ATOMS"].append(atomDict)
            if mode == Modes.ATOM and lengthCheck == frameLength and unDumped:
                yield unDumped


def read_yaml(file: str) -> Generator[dict[str:any], None, None]:
    """Generator object that yields one frame of the file at a time for yaml style lammp dump files"""
    unDumped = {}
    with open(file, "r") as yams:
        for line in yaml.safe_load_all(yams):
            unDumped["TIMESTEP"] = line["timestep"]
            unDumped["NUMBER OF ATOMS"] = line["natoms"]
            unDumped["BOX BOUNDS"] = {}
            unDumped["BOX BOUNDS"]["x"] = line["box"][0]  
            unDumped["BOX BOUNDS"]["y"] = line["box"][1]
            unDumped["BOX BOUNDS"]["z"] = line["box"][2]
            unDumped["ATOMS"] = []
            paraList = line["keywords"]
            for val in range(len(line["data"])):
                atomDict = {}
                paraNum = 0
                for para in paraList:
                    atomDict[para] = line["data"][val][paraNum]
                    paraNum += 1
                unDumped["ATOMS"].append(atomDict)
            yield unDumped


def read_grid(file: str) -> Generator[dict[str:any], None, None]:
    """Generator object that yields one frame at a time from grid style dumps"""

    unDumped = {}
    loopCount = 0
    gridID = 1
    frameLength = 0
    frameCount = 0
    
    with open(file, "r") as myfile:
        for line in myfile:
            loopCount += 1
            if frameCount < 2:
                frameLength += 1
            if "TIMESTEP" in line:
                frameCount += 1
                mode = Modes.TIME
                checkLoop = loopCount
            if mode == Modes.TIME and (loopCount - checkLoop) == 1:
                unDumped["TIMESTEP"] = int(line)
            if "BOX BOUNDS" in line:
                mode = Modes.BOUNDS
                checkLoop = loopCount
                unDumped["BOX BOUNDS"] = {"x": [], "y": [], "z": []}
            if mode == Modes.BOUNDS and (loopCount - checkLoop) == 1:
                unDumped["BOX BOUNDS"]["x"] = line.split()
            if mode == Modes.BOUNDS and (loopCount - checkLoop) == 2:
                unDumped["BOX BOUNDS"]["y"] = line.split()
            if mode == Modes.BOUNDS and (loopCount - checkLoop) == 3:
                unDumped["BOX BOUNDS"]["z"] = line.split()
            if "DIMENSION" in line:
                mode = Modes.DIM
                checkLoop = loopCount
            if mode == Modes.DIM and (loopCount - checkLoop) == 1:
                unDumped["DIMENSION"] = int(line)
            if "GRID SIZE" in line:
                mode = Modes.GRID_S
                checkLoop = loopCount
            if mode == Modes.GRID_S and (loopCount - checkLoop) == 1:
                unDumped["GRID SIZE"] = line.split() 
            if "GRID CELLS" in line:
                mode = Modes.GRID_C
                checkLoop = loopCount
                gridName = line.split()[3] u
                unDumped[gridName] = {}
                gridID = 1
            if mode == Modes.GRID_C and (loopCount - checkLoop) >= 1:
                unDumped[gridName][gridID] = line
                gridID += 1
            if frameCount > 1 and unDumped and (loopCount - frameLength) % (gridID + 10) == 0:
                yield unDumped
            

def read_dump(file, tpe=None):
    """return a generator object"""
    if tpe == "yaml":
        return read_yaml(file)
    elif tpe == "classic":
        return read_classic(file)
    elif tpe == "grid":
        return read_grid(file)  
    elif tpe == None:
        if ".yaml" in file:
            return read_yaml(file)
        elif ".lammpstrj" in file:
            return read_classic(file)
        elif ".grid" in file:
            return read_grid(file)
        else:
            raise Exception("Unsupported File Type") 


def read_whole_dump(file: str, tpe=None) -> list[dict[str:any]]:
    """read the entire file into an unDumped data structure"""
    if tpe == "yaml":
        return list(read_yaml(file))
    elif tpe == "classic":
        return list(read_classic(file))
    elif tpe == "grid":
        return list(read_grid(file))  
    elif tpe == None:
        if ".yaml" in file:
            return list(read_yaml(file))
        elif ".lammpstrj" in file:
            return list(read_classic(file))
        elif ".grid" in file:
            return list(read_grid(file))
        else:
            raise Exception("Unsupported File Type") 
    

