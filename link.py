import oracledb

connection = oracledb.connect(
    user = 'GROUP15',
    password = 'mIdrROfKPu',
    dsn = oracledb.makedsn('140.117.69.60', 1521, service_name = 'ORCLPDB1')
)
cursor = connection.cursor()