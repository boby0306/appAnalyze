
from program import analysis,weighting
import csv

# if __name__ == "__main__":
#     nameSLM = ("iOS", "NL52")
#     namedB  = ("ambient", "37", "40", "45", "50", "60", "70", "80")
#     for slm in nameSLM:
#         caliFile = "./data/" + slm + "_Cali.wav"
#         cali     = analysis.getCaliPower(caliFile)
#         forCSV = []
#         for dB in namedB:
#             print(dB)
#             fileName = "./data/" + slm + "_" + dB + "dB.wav"
#             bandEne  = analysis.analyze_allBandEne(fileName)
#             banddB   = analysis.ene2dB(bandEne, cali)
#             tmp = [dB + "dB"]
#             tmp.extend(list(map(lambda i: i, banddB)))
#             forCSV.append(tmp)
#         csvName = "./result/" + slm + "analyze.csv"
#         with open(csvName, "a", newline='') as f:
#             writer = csv.writer(f)
#             writer.writerows(forCSV)

if __name__ == "__main__":
    nameSLM = ("iOS", "NL52")
    namedB  = ("ambient", "37", "40", "45", "50", "60", "70", "80")
    for slm in nameSLM:
        caliFile = "./data/" + slm + "_Cali.wav"
        cali     = analysis.getCaliPower(caliFile)
        forCSV = []
        for dB in namedB:
            print(dB)
            fileName = "./data/" + slm + "_" + dB + "dB.wav"
            Apower = analysis.get_APower(fileName)
            dBA    = analysis.ene2dB(Apower, cali)
            tmp = [dB + "dB"]
            tmp.append(dBA)
            forCSV.append(tmp)
        csvName = "./result/" + slm + "_AdB.csv"
        with open(csvName, "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(forCSV)

#
# from program.by3OctBand import fList,rangeDic
#
# if __name__ == "__main__":
#     sos, IRLen = analysis.mk_passFilt(rangeDic[25][0], rangeDic[25][1], 48000.0)
#     analysis.mk_fGraph(sos)
#     sos, IRLen = analysis.mk_passFilt(rangeDic[1000][0], rangeDic[1000][1], 48000.0)
#     analysis.mk_fGraph(sos)
#     sos, IRLen = analysis.mk_passFilt(rangeDic[10000][0], rangeDic[10000][1], 48000.0)
#     analysis.mk_fGraph(sos)