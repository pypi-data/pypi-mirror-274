import pykd
from cjtool.stl import *
from cjtool.common import *
import pyperclip as pc
import argparse
import json
import time

def print_edo(msg):
    print(f"{bcolors.OKBLUE}{msg}{bcolors.ENDC}")

def print_shape(msg):
    print(f"{bcolors.OKGREEN}{msg}{bcolors.ENDC}")

def getEdoInfo(edoId) -> str:
    stringVar = malloc_string("")
    Void = pykd.typeInfo("Void")
    functype = pykd.defineFunction(Void, pykd.callingConvention.NearC)
    functype.append("argret", pykd.baseTypes.VoidPtr)
    functype.append("id", pykd.baseTypes.Int8B)
    printEdoPtr = pykd.typedVar("GFCCommon!getEdo")
    pykd.callFunctionByAddr(
        functype, printEdoPtr.getAddress(), stringVar.getAddress(), edoId)
    value = string(stringVar.getAddress())
    return str(value)


def getEdoInfoJson(edoId) -> json:
    jsonStr = getEdoInfo(edoId)
    return json.loads(jsonStr)


def getShape(edoId) -> str:
    stringVar = malloc_string("")
    Void = pykd.typeInfo("Void")
    functype = pykd.defineFunction(Void, pykd.callingConvention.NearC)
    functype.append("argret", pykd.baseTypes.VoidPtr)
    functype.append("id", pykd.baseTypes.Int8B)
    printEdoWPtr = pykd.typedVar("GFCCommon!getShape")
    pykd.callFunctionByAddr(
        functype, printEdoWPtr.getAddress(), stringVar.getAddress(), edoId)
    value = string(stringVar.getAddress())
    return str(value)


def main():
    parser = argparse.ArgumentParser(description="Input the edoid")
    parser.add_argument("edoid", type=int, help="The GFY Edo Id")
    parser.add_argument("--gfy4", "-4", action="store_true",
                        help="Set the process to be GFY4")
    args = parser.parse_args()
    edoid = args.edoid

    process_name = "GFY4" if args.gfy4 else "GFYDeepen"

    ext = pykd.isWindbgExt()
    try:
        if not ext:
            pykd.initialize()
            pid = getProcessByName(f"{process_name}.exe")
            if pid == 0:
                print(f"The app {process_name}.exe is not found")
                exit()

            pykd.attachProcess(pid)

        # 下行的代码，bp不能省去，否则pykd.go就不返回了
        bp = pykd.setBp(pykd.getOffset(
            f'{process_name}!GMPMainForm::eventFilter'))
        ret = pykd.go()
        if ret == pykd.executionStatus.Break:
            edoInfo = getEdoInfoJson(edoid)
            print(f"{edoInfo['description']} {edoInfo['typeName']}({edoInfo['elementType']}) {edoInfo['subTypeName']}({edoInfo['elementSubType']})\n")

            sorted_properties = sorted(edoInfo['properties'], key=lambda x: x['orderNum'])
            for index, prop in enumerate(sorted_properties):
                prn = print if prop['publicFlag'] == 1 else print_edo
                prn(f"{index:02}. {prop['description']}({prop['code']}, {prop['dataType']})\t{prop['value']}")

            szShape = edoInfo["shape"]
            print_shape(f"\n{szShape}")
            pc.copy(szShape)

            time.sleep(0.1)
            szBody = edoInfo["body"]
            if szBody:
                print_shape(f"\n{szShape}")
                pc.copy(szBody)

    except Exception as errtxt:
        print(errtxt)
    finally:
        if not ext:
            pykd.detachAllProcesses()


if __name__ == "__main__":
    main()
