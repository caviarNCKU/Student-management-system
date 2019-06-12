from PyQt5 import QtWidgets, uic, QtCore
import os
import sys
import mysql.connector as mdb
path = os.getcwd()
qtCreatorFile = path + os.sep + "ui" + os.sep + "Main_Window.ui"  # 設計好的ui檔案路徑
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)   # 讀入用Qt Designer設計的GUI layout


class MainUi(QtWidgets.QMainWindow, Ui_MainWindow):  # Python的多重繼承 MainUi 繼承自兩個類別

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.btn_srh.clicked.connect(self.DBconnection)
        self.comboBox.addItem('查詢學生資料')
        self.comboBox.addItem('查詢學生及其工作場所(SELECT-FROM-WHERE)')
        self.comboBox.addItem('註冊學生資料(INSERT)')
        self.comboBox.addItem('刪除學生資料(DELETE)')
        self.comboBox.addItem('更新學生資料(UPDATE)')
        self.comboBox.addItem('查詢此年級(IN)')
        self.comboBox.addItem('查詢非此年級(NOT IN)')
        self.comboBox.addItem('查詢是否存有此年級(EXISTS)')
        self.comboBox.addItem('查詢是否不存有此年級(NOT EXISTS)')
        self.comboBox.addItem('學生總數(COUNT)')
        self.comboBox.addItem('年級總和(SUM)')
        self.comboBox.addItem('學生家長最大年齡(男女)(MAX)')
        self.comboBox.addItem('學生家長最小年齡(男女)(MIN)')
        self.comboBox.addItem('學生家長平均年齡(AVG)')
        self.comboBox.addItem('學生家長年齡超過？歲(HAVING)')
        self.comboBox.addItem('MYSQL')
        self.comboBox.activated[str].connect(self.onActivated)


    def onActivated(self, text):
        global select
        select = text

    def showTable(self, cur):
        attr_names = [i[0] for i in cur.description]
        num_attr = len(cur.description)
        self.tableWidget.setColumnCount(num_attr)
        self.tableWidget.setHorizontalHeaderLabels(attr_names)

        result = cur.fetchall()
        self.tableWidget.setRowCount(0)
        for row_num, row_data in enumerate(result):
            self.tableWidget.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                self.tableWidget.setItem(row_num, col_num, QtWidgets.QTableWidgetItem(str(col_data)))    

    def DBconnection(self):
        db = mdb.connect(user='root',password='',host='localhost',database='studentDB')
        try:
            # SELECT * FROM WHERE               
            if(select == '查詢學生資料'):
                self.label_result.setText('查詢結果')
                cur = db.cursor()
                sql = "SELECT * FROM STUDENT"              
                cur.execute(sql)
                self.showTable(cur)
                cur.close

            elif(select == '查詢學生及其工作場所(SELECT-FROM-WHERE)'):
                self.label_result.setText('查詢結果')
                cur = db.cursor()
                sql = "SELECT STUDENT.Name,DEPARTMENT.Dname FROM STUDENT inner join PT_At on PT_At.STUDENT_Student_id = STUDENT.Student_id inner join DEPARTMENT on DEPARTMENT.Department_id = PT_At.DEPARTMENT_Department_id WHERE Dname = %s"              
                query = (self.textEdit.toPlainText(), )              
                cur.execute(sql, query) 
                self.showTable(cur)
                cur.close

            # INSERT
            elif(select == '註冊學生資料(INSERT)'):
                self.label_result.setText('註冊成功')
                cur = db.cursor()
                Name = self.le_Name.text()
                SSN = self.le_SSN.text()
                Email = self.le_Email.text()
                Phone = self.le_Phone.text()
                Address = self.le_Addr.text()
                Bdate = self.le_Bdate.text()
                val = (Name, SSN, Email, Phone, Address, Bdate)
                sql = "INSERT INTO STUDENT (Student_id, Name, SSN, Email, Phone, Address, Bdate) VALUES (DEFAULT, %s, %s, %s, %s, %s, %s)"                          
                cur.execute(sql, val)
                db.commit() #Update table
                cur.close

            # DELETE
            elif(select == '刪除學生資料(DELETE)'):
                self.label_result.setText('刪除成功')
                cur = db.cursor()
                sql = "DELETE FROM STUDENT WHERE Name = %s"
                query = (self.textEdit.toPlainText(), )              
                cur.execute(sql, query)                    
                db.commit() #Update table
                cur.close

            # UPDATE
            elif(select == '更新學生資料(UPDATE)'):
                self.label_result.setText('更新成功')
                cur = db.cursor()
                sql = "UPDATE STUDENT SET SSN = %s, Email = %s, Phone = %s, Address = %s, Bdate = %s WHERE Name = %s"
                Name = self.textEdit.toPlainText()
                SSN = self.le_SSN.text()
                Email = self.le_Email.text()
                Phone = self.le_Phone.text()
                Address = self.le_Addr.text()
                Bdate = self.le_Bdate.text()
                val = (SSN, Email, Phone, Address, Bdate, Name)            
                cur.execute(sql, val)                    
                db.commit() #Update table
                cur.close

            #IN
            elif(select == '查詢此年級(IN)'):
                self.label_result.setText('查詢結果')
                cur = db.cursor()
                sql = "SELECT * FROM STUDENT WHERE Student_id IN (SELECT Student_id FROM STUDENT WHERE Grade = %s)"           
                query = (self.textEdit.toPlainText(), )              
                cur.execute(sql, query)                                   
                self.showTable(cur)
                cur.close

            # NOT IN
            elif(select == '查詢非此年級(NOT IN)'):
                self.label_result.setText('查詢結果')
                cur = db.cursor()
                sql = "SELECT * FROM STUDENT WHERE Student_id NOT IN (SELECT Student_id FROM STUDENT WHERE Grade = %s)"           
                query = (self.textEdit.toPlainText(), )              
                cur.execute(sql, query)                                   
                self.showTable(cur)
                cur.close

            # EXIST
            elif(select == '查詢是否存有此年級(EXISTS)'):
                self.label_result.setText('查詢結果')
                cur = db.cursor()
                sql = "SELECT Name FROM STUDENT WHERE EXISTS (SELECT Student_id FROM STUDENT WHERE Grade = %s)"           
                query = (self.textEdit.toPlainText(), )              
                cur.execute(sql, query)                                   
                self.showTable(cur)
                cur.close

            # NOT EXIST
            elif(select == '查詢是否不存有此年級(NOT EXISTS)'):
                self.label_result.setText('查詢結果')
                cur = db.cursor()
                sql = "SELECT * FROM STUDENT WHERE NOT EXISTS (SELECT Student_id FROM STUDENT WHERE Grade = %s)"           
                query = (self.textEdit.toPlainText(), )              
                cur.execute(sql, query)                                   
                self.showTable(cur)
                cur.close

            # COUNT 
            elif(select == '學生總數(COUNT)'):
                self.label_result.setText('查詢結果')
                cur = db.cursor()
                sql = "SELECT COUNT(*) FROM STUDENT"                        
                cur.execute(sql)                                   
                self.showTable(cur)
                cur.close
            # SUM
            elif(select == '年級總和(SUM)'):
                self.label_result.setText('查詢結果')
                cur = db.cursor()
                sql = "SELECT SUM(Grade) FROM STUDENT"                        
                cur.execute(sql)                                   
                self.showTable(cur)
                cur.close
            # MAX
            elif(select == '學生家長最大年齡(男女)(MAX)'):
                self.label_result.setText('查詢結果')
                cur = db.cursor()
                sql = "SELECT PARENT.NAME, PARENT.Sex, PARENT.Age  FROM PARENT INNER JOIN ( SELECT sex, MAX(Age) max_age FROM PARENT GROUP BY sex  ) t ON Parent.Sex = t.Sex AND Parent.Age = t.max_age"                       
                cur.execute(sql)                                   
                self.showTable(cur)
                cur.close
            # MIN
            elif(select == '學生家長最小年齡(男女)(MIN)'):
                self.label_result.setText('查詢結果')
                cur = db.cursor()
                sql = "SELECT PARENT.NAME, PARENT.Sex, PARENT.Age  FROM PARENT INNER JOIN ( SELECT sex, Min(Age) max_age FROM PARENT GROUP BY sex  ) t ON Parent.Sex = t.Sex AND Parent.Age = t.max_age"                       
                cur.execute(sql)                                   
                self.showTable(cur)
                cur.close
            # AVG
            elif(select == '學生家長平均年齡(AVG)'):
                self.label_result.setText('查詢結果')
                cur = db.cursor()
                sql = "SELECT AVG(Age) FROM PARENT"                        
                cur.execute(sql)                                   
                self.showTable(cur)
                cur.close

            # HAVING
            elif(select == '學生家長年齡超過？歲(HAVING)'):

                self.label_result.setText('查詢結果')
                cur = db.cursor()
                sql = "SELECT STUDENT.Name, PARENT.Name, MAX(PARENT.Age) FROM STUDENT inner join Child_Of on Child_Of.STUDENT_Student_id = STUDENT.Student_id inner join PARENT on PARENT.Parent_id = Child_Of.PARENT_Parent_id GROUP BY  STUDENT.Name, PARENT.Name HAVING MAX(PARENT.Age) > %s;"                        
                query = (self.textEdit.toPlainText(), )              
                cur.execute(sql, query)                                                   
                self.showTable(cur)

                cur.close

            # MYSQL
            elif(select == 'MYSQL'):
                try:
                    self.label_result.setText('指令成功')
                    query = self.textEdit.toPlainText()
                    cur = db.cursor()
                    cur.execute(query)
                    self.showTable(cur)
                    cur.close
                except:
                    self.label_result.setText('指令失敗')


        except:
                self.label_result.setText('查詢結果')
                cur = db.cursor()
                sql = "SELECT * FROM STUDENT"             
                cur.execute(sql)
                self.showTable(cur)
                cur.close                      