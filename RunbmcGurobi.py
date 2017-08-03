import os
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


#runs by cluster:
os.system("python bmcGurobi.py 300 30win120_clust1.csv 0.3989 0.6483 -3.8070 30 30 -14.439 14.439 5.154")
os.system("python bmcGurobi.py 300 30win120_clust2.csv 0.4776 0.5738 -3.4145 30 30 -14.439 14.439 5.154")
os.system("python bmcGurobi.py 300 30win120_clust3.csv 0.4464 0.5802 -3.2218 30 30 -14.439 14.439 5.154")
