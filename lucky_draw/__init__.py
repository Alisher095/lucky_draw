import pymysql
# Ensure PyMySQL reports a compatible version so Django accepts it as MySQLdb
pymysql.version_info = (2, 2, 1, "final", 0)
pymysql.install_as_MySQLdb()
