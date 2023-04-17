import mysql.connector
class DBConnection:
    '''@staticmethod
    def getConnection():
        database = mysql.connector.connect(host="localhost", user="root", passwd="Kkkk9999@", db='criminal_identification')
        return database'''

    @staticmethod
    def getConnection():
        database = mysql.connector.connect(host="criminalidentification.cloudaccess.host", user="slsqenog", passwd="393K]YJx0lIy:t",
                                           db='slsqenog')
        return database
if __name__=="__main__":
    print(DBConnection.getConnection())