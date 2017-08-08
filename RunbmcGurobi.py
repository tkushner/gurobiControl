import bmcGurobi
import os
import openpyxl as xl
#run all the bmcGurobi.py scripts for various windows
# os.system("python bmcGurobi.py 300 30win120.csv 0.4427 0.5991 -3.4710 30 30 -14.439 14.439 5.154")
# os.system("python bmcGurobi.py 300 30win180.csv 0.2659 0.7625 -3.5694 30 30 -19.975 19.975 7.912")
# os.system("python bmcGurobi.py 300 30win300.csv 0.1390 0.8877 -3.7537 30 30 -19.454 19.454 8.714")
# os.system("python bmcGurobi.py 300 45win120.csv 0.5831 0.5548 -12.3819 45 45 -9.435 9.435 2.962")
# os.system("python bmcGurobi.py 300 45win180.csv 0.4709 0.6317 -11.0545 45 45 -19.864 19.864 6.993")
# os.system("python bmcGurobi.py 300 45win300.csv 0.2966 0.7797 -9.5391 45 45 -22.106 22.106 9.809")
# os.system("python bmcGurobi.py 300 60win180.csv 0.5081 0.6090 -10.7458 60 60 -14.371 14.371 5.142")
# os.system("python bmcGurobi.py 300 60win300.csv 0.3668 0.7123 -9.8962 60 60 -23.177 23.177 10.007")
# os.system("python bmcGurobi.py 300 120win300.csv 0.4740 0.6105 -9.8247 120 120 -12.128 12.128 4.880")

# #NEW RUNS bc old didn't have correct residuals
# os.system("python bmcGurobi.py 300 30win120.csv 0.4427 0.5991 -3.4710 30 30 -21.3737 21.3737 -0.3503")
# os.system("python bmcGurobi.py 300 30win180.csv 0.2659 0.7625 -3.5694 30 30 -29.7956 29.7956 -0.8365")
# os.system("python bmcGurobi.py 300 30win300.csv 0.1390 0.8877 -3.7537 30 30 -32.7504 32.7504 -1.1986")
# os.system("python bmcGurobi.py 300 45win120.csv 0.5831 0.5548 -12.3819 45 45 -11.4839 11.4839 -0.0824")
# os.system("python bmcGurobi.py 300 45win180.csv 0.4709 0.6317 -11.0545 45 45 -27.0285 27.0285 -0.6019")
# os.system("python bmcGurobi.py 300 45win300.csv 0.2966 0.7797 -9.5391 45 45 -37.9523 37.9523 -1.5014")
# os.system("python bmcGurobi.py 300 60win180.csv 0.5081 0.6090 -10.7458 60 60 -19.2875 19.2875 -0.2701")
# os.system("python bmcGurobi.py 300 60win300.csv 0.3668 0.7123 -9.8962 60 60 -40.4967 40.4967 -1.4879")
# os.system("python bmcGurobi.py 300 120win300.csv 0.4740 0.6105 -9.8247 120 120 -19.6818 19.6818 -0.3030")



#runs by cluster:
# os.system("python bmcGurobi.py 300 30win120_clust1.csv 0.3989 0.6483 -3.8070 30 30 -14.439 14.439 5.154")
# os.system("python bmcGurobi.py 300 30win120_clust2.csv 0.4776 0.5738 -3.4145 30 30 -14.439 14.439 5.154")
# os.system("python bmcGurobi.py 300 30win120_clust3.csv 0.4464 0.5802 -3.2218 30 30 -14.439 14.439 5.154")

# os.system("python bmcGurobi.py 300 45win120_clust1.csv 0.5454 0.5840 -9.9177 30 30 -14.439 14.439 5.154")
# os.system("python bmcGurobi.py 300 45win120_clust2.csv 0.6260 0.5340 -13.2130 30 30 -14.439 14.439 5.154")
# os.system("python bmcGurobi.py 300 45win120_clust3.csv 0.5726 0.5499 -13.7511 30 30 -14.439 14.439 5.154")

def loadParameters():
    allSessions = {}
    sessionSpreadSheet='./PSO3Sessions.xlsx'
    wb=xl.load_workbook(sessionSpreadSheet)
    sh=wb.get_sheet_by_name('Sheet1')
    # Run through all the rows of the sheet
    n = len(list(sh.rows))
    for j in range(2,n+1): # note range(a,b) in Python includes a but excludes b
        cellID = str(j)    # convert j into a string
        sID = sh['A'+cellID].value
        patientID = sh['B'+cellID].value
        sType = sh['C'+cellID].value
        sess = SessionData(sID,patientID,sType)
        allSessions[sID] = sess
    return allSessions

def main(argv):
    if len(argv) < 3:
        print('Usage: python ', sys.argv[0], '[Depth to Explore]  [Output file]')
    d = int(sys.argv[1])
    oFile = open(sys.argv[2], 'a')

    for depths in range(0, d, 10):
        g = GRBEncoder(depths)
        g.setup()
        g.add_glucose_equation()
        g.solve_for_glucose(oFile)
    print('DONE')
    oFile.close()

if __name__ == '__main__':
    main(sys.argv)
