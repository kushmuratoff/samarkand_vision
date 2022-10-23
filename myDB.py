import psycopg2
from datetime import datetime
import numpy as np
import pandas as pd
from PIL import Image

class DBHelper:
   def __init__(self):
      try:
         keepalive_kwargs = {
            "keepalives": 1,
            "keepalives_idle": 60,
            "keepalives_interval": 10,
            "keepalives_count": 5
         }
         self.conn=psycopg2.connect(database="postgres", user='sulaymonovuser', password='Ab0199797', host='213.230.107.46', port='5432',**keepalive_kwargs)
         # self.conn.autocommit = True
         self.cursor=self.conn.cursor()

      except Exception:
         print("baza boshlanishda hatolik")



   #yangi zaproslar
   def statusIkkiNol(self):
      try:
         sqlite_update_with_param = "UPDATE visitor  SET status2 = " + str(0) + ""
         # data_tuple = (str(chatId), str(Rasm),time,False)
         self.cursor.execute(sqlite_update_with_param)
         self.conn.commit()
         mavjudmi = list(pd.read_sql_query(
            "SELECT * FROM visitor", self.conn)[
                            'status2'])
         print("status2", mavjudmi)


      except Exception as ex:
         print("status2 larni 0 qilishda hato")

   def statusIkki(self):
      try:
         sqlite_update_with_param = "UPDATE visitor  SET status = status2"
         # data_tuple = (str(chatId), str(Rasm),time,False)
         self.cursor.execute(sqlite_update_with_param)
         self.conn.commit()

         mavjudmi = list(pd.read_sql_query(
            "SELECT * FROM visitor", self.conn)[
                            'status'])
         print("status ", mavjudmi)


      except Exception as ex:
         print("status2 larni 0 qilishda hato")



   def sonniOshirish(self, PerId):
      try:

         mavjudmi = list(pd.read_sql_query(
            "SELECT * FROM visitor where visitor_id=" + str(PerId) + " and status = 0", self.conn)[
                            'visitor_count'])
         if (len(mavjudmi))>0:
            print(str(PerId), mavjudmi[0], type(mavjudmi[0]))
            sqlite_insert_with_param = "UPDATE visitor  SET visitor_count = " + str(
               mavjudmi[0] + 1) + ", status2=1, status=1 where status=0 and visitor_id=" + str(PerId) + ";"
            # data_tuple = (str(chatId), str(Rasm),time,False)
            self.cursor.execute(sqlite_insert_with_param)
            self.conn.commit()
            return mavjudmi[0]+1
            # self.conn.close()
         return mavjudmi[0]
         # else:
         #    sqlite_insert_with_param = "UPDATE visitor  SET visitor_count = " + str(
         #       mavjudmi[0] + 1) + ", status2=0, status=1 where status=1 and visitor_id=" + str(PerId) + ";"
         #    # data_tuple = (str(chatId), str(Rasm),time,False)
         #    self.cursor.execute(sqlite_insert_with_param)
         #    self.conn.commit()

         # print("status_", mavjudmi)

      except Exception as ex:
         print("sonini oshirishda xato")
   def addPerson(self,age,gender,emb):
      try:

         idsi = pd.read_sql_query("select max(visitor_id) from visitor",self.conn)
         print("yangi odam idsi: ",(idsi["max"][0]))
         if idsi["max"][0]:
            sqlite_insert_with_param = "INSERT INTO visitor (visitor_name) VALUES ('Person" + str(idsi["max"][0]+1)+"');"
            # data_tuple = (str(chatId), str(Rasm),time,False)
            self.cursor.execute(sqlite_insert_with_param)
            self.conn.commit()
            # print("odam qoshildi")

            #visitga qoshish
            sqlite_insert_with_param = "INSERT INTO visit (visitor_id, visitor_age, visitor_gender,visitor_embedding) VALUES (" + str(
               idsi["max"][0] + 1) + ",'"+str(age)+"','"+str(gender)+"', '"+str(emb)+"');"
            # data_tuple = (str(chatId), str(Rasm),time,False)
            self.cursor.execute(sqlite_insert_with_param)
            self.conn.commit()
            print("vaqti qoshildi")

            self.sonniOshirish(idsi["max"][0] + 1)
            # self.conn.close()
      except Exception as error:
         print("person addda muammo borbor", error)

   def getEmbed(self):
      try:
         visit = pd.read_sql_query("select visit_id, visitor_id, visitor_embedding from visit",self.conn)
         # print(visit["visitor_embedding"])
         visit_list = visit["visitor_embedding"].to_list()
         # print(visit_list,type(visit_list))
         visit_list = [np.fromstring(xx[1:-1], dtype=np.float32, sep=' ') for xx in visit_list]
         return visit_list
         # print(visit_list)
      except Exception as ex:
         print("Embeding vektorni olishda hato: ", ex)

   def addVisit(self,idx,age,gender,emb):
      try:
         visitor_id = pd.read_sql_query("select visitor_id, visitor_embedding from visit",self.conn).iloc[idx]['visitor_id']
         # a = visit.[idx]['visitor_id']
         print("visitor_id: ", str(visitor_id))
         soni = pd.read_sql_query("select count(visitor_id) from visit where visitor_id="+str(visitor_id)+"",self.conn)
         if soni.iloc[0]['count']<10:
            sqlite_insert_with_param = "INSERT INTO visit (visitor_id, visitor_age, visitor_gender,visitor_embedding) VALUES (" + str(visitor_id) + ",'" + str(age) + "','" + str(gender) + "', '" + str(emb) + "');"
            # data_tuple = (str(chatId), str(Rasm),time,False)
            self.cursor.execute(sqlite_insert_with_param)
            self.conn.commit()

         print("visitor soni: ",soni.iloc[0]['count'])
         return self.sonniOshirish(visitor_id)


      except Exception as ex:
         print("Visitor qoshishda muammo: ",ex)

   def getPerson(self,idx):
      try:
         visits = pd.read_sql_query("select * from visit", self.conn)
         visitor_id = visits.iloc[idx][['visitor_id','visitor_age','visitor_gender']]
         print(visitor_id[0])
         # a = visit.[idx]['visitor_id']
         # print("visitor_id: ", str(visitor_id))
         info_person = pd.read_sql_query("select visitor_count from visitor where visitor_id=" + str(visitor_id[0]) + "", self.conn)
         print(info_person["visitor_count"][0],type(info_person["visitor_count"][0]))
         return info_person["visitor_count"][0], visitor_id[1],visitor_id[2]

      except Exception as ex:
         print("bazada mavjud odamni olishda xato", ex)

   def tt(self):
      mavjudmi = list(pd.read_sql_query(
         "SELECT * FROM visitor where visitor_id=" + str(52) + " and status = 1", self.conn)[
                         'visitor_count'])
      print(mavjudmi, len(mavjudmi))


ob = DBHelper()
ob.getPerson(8)
# #eski zaproslar

#    def check_user(self,number):
#          raqamlar = list(pd.read_sql_query('SELECT * FROM abituriyent_oqituvchi;', self.conn)['telefon'])
#          for i in raqamlar:
#             basenumber=i
#             if number == basenumber:
#                # self.conn.autocommit = True
#                # cursor = self.conn.cursor()
#                sql = "UPDATE ABITURIYENT_OQITUVCHI SET tasdiq = True Where telefon = '" + str(number) + "'"
#                sql1 = "UPDATE ABITURIYENT_OQITUVCHI SET tasdiq = True Where telefon = '+" + str(number) + "'"
#                self.cursor.execute(sql)
#                self.cursor.execute(sql1)
#                self.conn.commit()
#                # self.conn.close()
#                return True
#
#          return False
#
#    def chatId_set(self,raqam,idsi):
#       try:
#          # self.conn = psycopg2.connect(database="mydata", user='sulaymonovuser', password='Ab0199797', host='213.230.107.46',
#          #                         port='5432')
#          # conn.autocommit = True
#          # # print("worked")
#          # cursor = conn.cursor()
#          sql = "UPDATE ABITURIYENT_OQITUVCHI SET chatid = '"+str(idsi)+"' Where telefon = '" + str(raqam) + "'"
#          self.cursor.execute(sql)
#          self.conn.commit()
#          # self.conn.close()
#       except Exception as ex:
#          print("chatIdni bazaga yozishda muammo bor")
#
#    def check_userId(self,idsi):
#       # conn = psycopg2.connect(database="mydata", user='sulaymonovuser', password='Ab0199797', host='213.230.107.46', port='5432')
#       # conn.autocommit = True
#       # # print("worked")
#       # cursor = conn.cursor()
#       idlar = list(pd.read_sql_query("SELECT * FROM abituriyent_oqituvchi where chatid= '"+str(idsi)+"';", self.conn)['chatid'])
#       if(idlar):
#          return True
#       return False
#       # print(idlar)
#
#    def fio(self,idsi):
#       # conn = psycopg2.connect(
#       #    database="mydata", user='sulaymonovuser', password='Ab0199797', host='213.230.107.46', port='5432'
#       # )
#       # conn.autocommit = True
#       # # print("worked")
#       # cursor = conn.cursor()
#       idlar = list(
#          pd.read_sql_query("SELECT * FROM abituriyent_oqituvchi where chatid= '" + str(idsi) + "';", self.conn)['FIO'])
#       return idlar[0]
#
#
#
#    def write_img(self,chatId,Rasm,timei):
#       try:
#          sqlite_insert_with_param = "INSERT INTO abituriyent_yuborilgan_rasmlar (chatid, rasm, sanasi, tasdiq,tasdiq2, tasdiq3) VALUES ('" + str(
#             chatId) + "', '" + str(Rasm) + "','" + str(datetime.now()) + "','" + str(False) + "',"+str(0)+","+str(0)+");"
#          # data_tuple = (str(chatId), str(Rasm),time,False)
#          self.cursor.execute(sqlite_insert_with_param)
#          self.conn.commit()
#          # self.conn.close()
#
#          # df = pd.read_sql_query('SELECT * FROM abituriyent_yuborilgan_rasmlar ', conn)
#
#       except Exception as error:
#          print("Rasm yozishda muammo bor", error)
#
#    def ntVar(self,rasm,varid):
#       try:
#          sqlite_insert_with_param = "UPDATE abituriyent_yuborilgan_rasmlar  SET varid='"+str(varid)+"' where tasdiq = False and rasm = '" + str(rasm) + "';"
#          # data_tuple = (str(chatId), str(Rasm),time,False)
#          self.cursor.execute(sqlite_insert_with_param)
#          self.conn.commit()
#
#       except Exception as ex:
#          print("bazada topilmagan varding  idsi yozishda muammo ", ex)
#
#    def ntVarOlish(self,idsi):
#       try:
#          varidlar = list(pd.read_sql_query("SELECT * FROM abituriyent_yuborilgan_rasmlar where length(varid)>0 and chatid = '" + str(idsi) + "' and tasdiq = False;",self.conn)['varid'])
#          satr= ""
#          if(len(varidlar)>0):
#             for i in  range(len(varidlar)-1):
#                satr+=str(varidlar[i])+", "
#             satr+= str(varidlar[len(varidlar)-1])+"."
#             print(satr)
#          return satr
#       except Exception as ex:
#          print("mavjud bo'lmagan variant idlarni olishda mummo bor",ex)
#
#
#    def ntTalaba(self, rasm, talabaid):
#       try:
#          sqlite_insert_with_param = "UPDATE abituriyent_yuborilgan_rasmlar  SET talabaid='" + str(talabaid) + "' where tasdiq = False and rasm = '" + str(rasm) + "';"
#          # data_tuple = (str(chatId), str(Rasm),time,False)
#          self.cursor.execute(sqlite_insert_with_param)
#          self.conn.commit()
#
#       except Exception as ex:
#          print("bazada topilmagan Talabaning  idsi yozishda muammo ", ex)
#
#
#    def ntTalabaOlish(self,idsi):
#       try:
#          varidlar = list(pd.read_sql_query("SELECT * FROM abituriyent_yuborilgan_rasmlar where length(talabaid)>0 and chatid = '" + str(idsi) + "' and tasdiq = False;",self.conn)['talabaid'])
#          satr= ""
#          if(len(varidlar)>0):
#             for i in  range(len(varidlar)-1):
#                satr+=str(varidlar[i])+", "
#             satr+= str(varidlar[len(varidlar)-1])+"."
#             print(satr)
#          return satr
#       except Exception as ex:
#          print("mavjud bo'lmagan talaba idlarni olishda mummo bor",ex)
#
#
#    def ntNotDetect(self,rasm):
#       try:
#          sqlite_insert_with_param = "UPDATE abituriyent_yuborilgan_rasmlar  SET tasdiq2=" + str(1) + " where tasdiq = False and rasm = '" + str(rasm) + "';"
#          # data_tuple = (str(chatId), str(Rasm),time,False)
#          self.cursor.execute(sqlite_insert_with_param)
#          self.conn.commit()
#
#       except Exception as ex:
#          print("bazada topilmagan titulni yozishda muammo ", ex)
#
#    def ntNotDetectOlish(self, idsi):
#       try:
#          rasmlar = list(pd.read_sql_query("SELECT * FROM abituriyent_yuborilgan_rasmlar where chatid = '" + str(idsi) + "' and tasdiq = False and tasdiq2=1 ;", self.conn)['rasm'])
#          return  rasmlar
#
#       except Exception as ex:
#          print("bazada topilmagan titulni yozishda muammo ", ex)
#
#
#
#
#    def get_rasm(self,idsi):
#       # conn = psycopg2.connect(
#       #    database="mydata", user='sulaymonovuser', password='Ab0199797', host='213.230.107.46', port='5432'
#       # )
#       # conn.autocommit = True
#       # # print("worked")
#       # cursor = conn.cursor()
#       rasmlar = list(pd.read_sql_query("SELECT * FROM abituriyent_yuborilgan_rasmlar where chatid = '"+str(idsi)+"' and tasdiq = False;", self.conn)['rasm'])
#       return rasmlar
#
#    def change_status(self,idsi):
#       try:
#          # conn = psycopg2.connect(
#          #    database="mydata", user='sulaymonovuser', password='Ab0199797', host='213.230.107.46', port='5432'
#          # )
#          # conn.autocommit = True
#          # # print("worked")
#          # cursor = conn.cursor()
#          sqlite_insert_with_param = "UPDATE abituriyent_yuborilgan_rasmlar  SET tasdiq=True where tasdiq = False and chatid = '" + str(idsi) + "';"
#          # data_tuple = (str(chatId), str(Rasm),time,False)
#          self.cursor.execute(sqlite_insert_with_param)
#          self.conn.commit()
#
#
#          # df = pd.DataFrame(df)
#
#          # return df
#       except Exception as ex:
#          print("statusni ozgartirish funksiyasida hato ketyapti ", ex)
#
#
#    def get_variant_javob(self,varId):
#       # conn = psycopg2.connect(
#       #    database="mydata", user='sulaymonovuser', password='Ab0199797', host='213.230.107.46', port='5432'
#       # )
#       # conn.autocommit = True
#       # # print("worked")
#       # cursor = conn.cursor()
#       javoblar = list(pd.read_sql_query("SELECT * FROM abituriyent_variant_test_javoblari where id="+str(varId)+"", self.conn)['Javob'])
#       # print(javoblar)
#       return javoblar
#
#    def rasmSoni(self,idsi):
#       javoblar = list(pd.read_sql_query("SELECT * FROM abituriyent_yuborilgan_rasmlar where tasdiq=False and chatid='" + str(idsi) + "'", self.conn)['chatid'])
#       # print(javoblar)
#       return len(javoblar)
#
#
#    def natija_yozish(self,variantId,myscore,njavob,foizi,savedir,talabaId,idsi):
#       try:
#          mavjudmi = list(pd.read_sql_query("SELECT * FROM abituriyent_oquvchilar_malumoti where status=0 and chatid='" + str(idsi) + "' and variant_nomeri_id="+str(variantId)+" and oquvchi_id_id="+str(talabaId)+" ",self.conn)['chatid'])
#
#          if not (len(mavjudmi)>0):
#
#             sqlite_insert_with_param = "INSERT INTO abituriyent_oquvchilar_malumoti (variant_nomeri_id, togri_javoblar, notogri_javoblar, foizi, sanasi, titul_varaqasi, oquvchi_id_id, chatid, status) VALUES (" + str(
#                variantId) + ", " + str(myscore) + "," + str(njavob) + "," + str(foizi) + ",'" + str(
#                datetime.now()) + "','" + str(savedir) + "'," + str(talabaId) + "," + str(idsi) + "," + str(0) + ");"
#             # data_tuple = (str(chatId), str(Rasm),time,False)
#             self.cursor.execute(sqlite_insert_with_param)
#             self.conn.commit()
#             # self.conn.close()
#
#          # df = pd.read_sql_query('SELECT * FROM abituriyent_yuborilgan_rasmlar ', conn)
#
#       except Exception as error:
#          print("Natija yozishda muammo bor", error)
#
#
#    def natija_status(self,idsi):
#       try:
#
#          sqlite_insert_with_param = "UPDATE abituriyent_oquvchilar_malumoti  SET status = 1 where status = 0 and chatid = '" + str(idsi) + "';"
#          # data_tuple = (str(chatId), str(Rasm),time,False)
#          self.cursor.execute(sqlite_insert_with_param)
#          self.conn.commit()
#          # self.conn.close()
#
#          # df = pd.read_sql_query('SELECT * FROM abituriyent_yuborilgan_rasmlar ', conn)
#
#       except Exception as error:
#          print("oquvchi malumotlari jadvali statusni ozgartirishda muammo", error)
#
#
#    def isVariant(self,VarId):
#       try:
#          javoblar = list(pd.read_sql_query("SELECT * FROM abituriyent_variant_test_javoblari where id=" + str(VarId) + "", self.conn)['Javob'])
#          # print(javoblar)
#          if(len(javoblar)):
#             return True
#          return False
#       except Exception as ex:
#          print("Variant Id topilmadi",ex)
#
#
#    def isTalaba(self,TalId):
#       try:
#          javoblar = list(pd.read_sql_query("SELECT * FROM abituriyent_oquvchilar where id=" + str(TalId) + "", self.conn)['id'])
#          # print(javoblar)
#          if(len(javoblar)):
#             return True
#          return False
#       except Exception as ex:
#          print("Talabani mavjudligini tekshirshda hatolik",ex)
#
#
#    def isExist(self,idsi):
#       try:
#          mavjudmi = list(pd.read_sql_query("SELECT * FROM abituriyent_tg_hisobot where chatid='" + str(idsi) + "' and status = 0",self.conn)['id'])
#          # print(javoblar)
#          if (len(mavjudmi)):
#             return mavjudmi[0]
#          return 0
#
#       except Exception as ex:
#          print("Hsiobot mavjudligni aniqlashda muammo bor")
#
#    def changeStHisobot(self,idsi):
#       try:
#          sqlite_insert_with_param = "UPDATE abituriyent_tg_hisobot  SET status = 1 where status = 0 and chatid = '" + str(idsi) + "';"
#          # data_tuple = (str(chatId), str(Rasm),time,False)
#          self.cursor.execute(sqlite_insert_with_param)
#          self.conn.commit()
#          # self.conn.close()
#
#          # df = pd.read_sql_query('SELECT * FROM abituriyent_yuborilgan_rasmlar ', conn)
#
#       except Exception as error:
#          print("Hisobot tgning statusini o'zgartishda muammo bor", error)
#
#
#    def addHisobot(self,idsi):
#       try:
#          mavjudmi = self.isExist(idsi)
#          if not mavjudmi:
#             sqlite_insert_with_param = "INSERT INTO abituriyent_tg_hisobot (chatid, notdetect, samevar, samestudent, allimg, wrongstudent, status, wrongvar) VALUES (" + str(idsi) +","+str(0)+","+str(0)+","+str(0)+","+str(0)+","+str(0)+","+str(0)+","+str(0)+");"
#             # data_tuple = (str(chatId), str(Rasm),time,False)
#             self.cursor.execute(sqlite_insert_with_param)
#             self.conn.commit()
#             # self.conn.close()
#       except Exception as error:
#          print("Hisobot yozishda muammo bor", error)
#
#
#    def addNotDetect(self,idsi):
#       try:
#          mavjudmi = list(pd.read_sql_query("SELECT * FROM abituriyent_tg_hisobot where chatid='" + str(idsi) + "' and status = 0",self.conn)['notdetect'])
#          if (len(mavjudmi)):
#             print(mavjudmi[0],type(mavjudmi[0]))
#             sqlite_insert_with_param = "UPDATE abituriyent_tg_hisobot  SET notdetect = "+str(mavjudmi[0]+1)+" where status = 0 and chatid = '" + str(idsi) + "';"
#             # data_tuple = (str(chatId), str(Rasm),time,False)
#             self.cursor.execute(sqlite_insert_with_param)
#             self.conn.commit()
#             # self.conn.close()
#
#          # df = pd.read_sql_query('SELECT * FROM abituriyent_yuborilgan_rasmlar ', conn)
#
#       except Exception as error:
#          print("Hisobot tgga not detect update qilishda muammo bor", error)
#
#
#    def addAllImg(self,idsi,soni):
#       try:
#          mavjudmi = list(pd.read_sql_query("SELECT * FROM abituriyent_tg_hisobot where chatid='" + str(idsi) + "' and status = 0",self.conn)['allimg'])
#          if (len(mavjudmi)):
#             print(mavjudmi[0],type(mavjudmi[0]))
#             sqlite_insert_with_param = "UPDATE abituriyent_tg_hisobot  SET allimg = "+str(soni)+" where status = 0 and chatid = '" + str(idsi) + "';"
#             # data_tuple = (str(chatId), str(Rasm),time,False)
#             self.cursor.execute(sqlite_insert_with_param)
#             self.conn.commit()
#             # self.conn.close()
#
#          # df = pd.read_sql_query('SELECT * FROM abituriyent_yuborilgan_rasmlar ', conn)
#
#       except Exception as error:
#          print("Hisobot tgga allImg update qilishda muammo bor", error)
#
#    def wrongVar(self,idsi):
#       try:
#          mavjudmi = list(pd.read_sql_query("SELECT * FROM abituriyent_tg_hisobot where chatid='" + str(idsi) + "' and status = 0",self.conn)['wrongvar'])
#          if (len(mavjudmi)):
#             print(mavjudmi[0],type(mavjudmi[0]))
#             sqlite_insert_with_param = "UPDATE abituriyent_tg_hisobot  SET wrongvar = "+str(mavjudmi[0]+1)+" where status = 0 and chatid = '" + str(idsi) + "';"
#             # data_tuple = (str(chatId), str(Rasm),time,False)
#             self.cursor.execute(sqlite_insert_with_param)
#             self.conn.commit()
#             # self.conn.close()
#
#          # df = pd.read_sql_query('SELECT * FROM abituriyent_yuborilgan_rasmlar ', conn)
#
#       except Exception as error:
#          print("Hisobot tgga wrongwar update qilishda muammo bor", error)
#
#
#
#    def wrongTalaba(self,idsi):
#       try:
#          mavjudmi = list(pd.read_sql_query("SELECT * FROM abituriyent_tg_hisobot where chatid='" + str(idsi) + "' and status = 0",self.conn)['wrongstudent'])
#          if (len(mavjudmi)):
#             print(mavjudmi[0],type(mavjudmi[0]))
#             sqlite_insert_with_param = "UPDATE abituriyent_tg_hisobot  SET wrongstudent = "+str(mavjudmi[0]+1)+" where status = 0 and chatid = '" + str(idsi) + "';"
#             # data_tuple = (str(chatId), str(Rasm),time,False)
#             self.cursor.execute(sqlite_insert_with_param)
#             self.conn.commit()
#             # self.conn.close()
#
#          # df = pd.read_sql_query('SELECT * FROM abituriyent_yuborilgan_rasmlar ', conn)
#
#       except Exception as error:
#          print("Hisobot tgga wrongstudent update qilishda muammo bor", error)
#
#
#    def getTgHisobot(self,idsi):
#       allImg = list(pd.read_sql_query("SELECT * FROM abituriyent_tg_hisobot where chatid='" + str(idsi) + "' and status = 0",self.conn)['allimg'])
#       NotDetect = list(pd.read_sql_query("SELECT * FROM abituriyent_tg_hisobot where chatid='" + str(idsi) + "' and status = 0",self.conn)['notdetect'])
#       wrongVar = list(pd.read_sql_query("SELECT * FROM abituriyent_tg_hisobot where chatid='" + str(idsi) + "' and status = 0",self.conn)['wrongvar'])
#       wrongStudent = list(pd.read_sql_query("SELECT * FROM abituriyent_tg_hisobot where chatid='" + str(idsi) + "' and status = 0",self.conn)['wrongstudent'])
#
#       return allImg[0],NotDetect[0],wrongVar[0],wrongStudent[0]
#
#
#    def getVarIdlar(self,idsi):
#       varidlar = list(pd.read_sql_query("select variant_nomeri_id from abituriyent_oquvchilar_malumoti where chatid='"+str(idsi)+"' and status=0 GROUP BY variant_nomeri_id HAVING COUNT(variant_nomeri_id)>1",self.conn)['variant_nomeri_id'])
#       print(varidlar)
#       my_satr=""
#       for varId in varidlar:
#          idlar = list(pd.read_sql_query("select oquvchi_id_id from abituriyent_oquvchilar_malumoti where chatid='"+str(idsi)+"' and status=0 AND variant_nomeri_id="+str(varId)+"",self.conn)['oquvchi_id_id'])
#          my_satr = "TALABA(lar) "
#          for i in range(len(idlar) - 1):
#             my_satr += str(idlar[i])+", "
#          my_satr+=str(idlar[len(idlar) - 1])+ " ->  VARIANT - "+str(varId)+" ni yechgan.\n"
#
#       return my_satr
#
#    def getStudentIdlar(self,idsi):
#       varidlar = list(pd.read_sql_query("select oquvchi_id_id from abituriyent_oquvchilar_malumoti where chatid='"+str(idsi)+"' and status=0 GROUP BY oquvchi_id_id HAVING COUNT(oquvchi_id_id)>1",self.conn)['oquvchi_id_id'])
#       my_satr=""
#       for varId in varidlar:
#          idlar = list(pd.read_sql_query("select variant_nomeri_id from abituriyent_oquvchilar_malumoti where chatid='"+str(idsi)+"' and status=0 AND oquvchi_id_id="+str(varId)+"",self.conn)['variant_nomeri_id'])
#          my_satr="TALABA(lar) - "+str(varId)+" -> VARIANT - "
#          for i in range(len(idlar)-1):
#             my_satr+=str(idlar[i])+", "
#          my_satr+=str(idlar[len(idlar)-1])+" ni yechgan."
#
#       return my_satr
#
#    def yakunlashBir(self,idsi):
#       try:
#          mavjudmi = list(pd.read_sql_query("SELECT * FROM abituriyent_yuborilgan_rasmlar where chatid='" + str(idsi) + "' and tasdiq = False and tasdiq3 = 0",self.conn)['tasdiq'])
#          if (len(mavjudmi)>0):
#             return len(mavjudmi)
#
#          return 0
#
#          # df = pd.read_sql_query('SELECT * FROM abituriyent_yuborilgan_rasmlar ', conn)
#
#       except Exception as error:
#          print("yakunlashni birinchi holida xatolik bor", error)
#
#
#    def finishQilish(self,idsi):
#       try:
#          mavjudmi = list(pd.read_sql_query("SELECT * FROM abituriyent_yuborilgan_rasmlar where chatid='" + str(idsi) + "' and tasdiq = True and tasdiq3 = 0",self.conn)['tasdiq'])
#          if (len(mavjudmi)>0):
#             return len(mavjudmi)
#
#          return 0
#
#          # df = pd.read_sql_query('SELECT * FROM abituriyent_yuborilgan_rasmlar ', conn)
#
#       except Exception as error:
#          print("yakunlashda xatolik bor", error)
#
#
#    def yakunlashUpdate(self,idsi):
#       try:
#          mavjudmi = list(pd.read_sql_query("SELECT * FROM abituriyent_yuborilgan_rasmlar where chatid='" + str(idsi) + "' and tasdiq = True and tasdiq3=0",self.conn)['tasdiq'])
#          if (len(mavjudmi)):
#
#             sqlite_insert_with_param = "UPDATE abituriyent_yuborilgan_rasmlar  SET tasdiq3 = "+str(1)+" where tasdiq = True and chatid = '" + str(idsi) + "';"
#             # data_tuple = (str(chatId), str(Rasm),time,False)
#             self.cursor.execute(sqlite_insert_with_param)
#             self.conn.commit()
#             # self.conn.close()
#
#          # df = pd.read_sql_query('SELECT * FROM abituriyent_yuborilgan_rasmlar ', conn)
#
#       except Exception as error:
#          print("yakunlashni update qilishda muammo bor", error)
#
#
#    def izoh_yozish(self,idsi):
#       try:
#          varidlar = list(pd.read_sql_query("select variant_nomeri_id from abituriyent_oquvchilar_malumoti where chatid='" + str(idsi) + "' and status=0 GROUP BY variant_nomeri_id HAVING COUNT(variant_nomeri_id)>1", self.conn)['variant_nomeri_id'])
#          print(varidlar)
#          my_satr = ""
#          for varId in varidlar:
#             idlar = list(pd.read_sql_query("select oquvchi_id_id from abituriyent_oquvchilar_malumoti where chatid='" + str(idsi) + "' and status=0 AND variant_nomeri_id=" + str(varId) + "", self.conn)['oquvchi_id_id'])
#
#             for i in range(len(idlar)):
#                my_satr="Bu varinatni "
#                for j in range(len(idlar)):
#                   if i==j:
#                      continue
#                   my_fio = list(pd.read_sql_query("select * from abituriyent_oquvchilar where id="+str(idlar[j])+"", self.conn)['Fish'])
#                   my_satr+= str(my_fio[0])+" "
#                my_satr+="yechgan."
#                print(my_satr)
#                sqlite_insert_with_param = "UPDATE abituriyent_oquvchilar_malumoti  SET izoh = '" + str(my_satr) + "' where chatid = '"+str(idsi)+"' and status=0 and  variant_nomeri_id=" + str(varId) + " and oquvchi_id_id=" + str(idlar[i]) + ";"
#                # data_tuple = (str(chatId), str(Rasm),time,False)
#                self.cursor.execute(sqlite_insert_with_param)
#                self.conn.commit()
#
#
#          #       my_satr += str(idlar[i]) + ", "
#          #    my_satr += str(idlar[len(idlar) - 1]) + " ->  VARIANT - " + str(varId) + " ni yechgan.\n"
#          #
#          # return my_satr
#       except Exception as ex:
#          print("Izoh yozishda xatolik bo'ldi: ", ex)
#
#
#    def soniAcces(self, idsi):
#       try:
#          mavjudmi = list(pd.read_sql_query("SELECT * FROM abituriyent_yuborilgan_rasmlar where chatid='" + str(idsi) + "' and tasdiq3=0", self.conn)['tasdiq3'])
#          if (len(mavjudmi)):
#             return len(mavjudmi)
#          else:
#             return 0
#       except Exception as error:
#          print("yakunlashni update qilishda muammo bor", error)
#
#    def getExcel(self, idsi):
#       try:
#          #note status 0 ga o'zgarishi kerak
#          mavjudmi = pd.read_sql_query(" select * from abituriyent_oquvchilar_malumoti as a inner join abituriyent_oquvchilar as b on a.oquvchi_id_id= b.id where a.status=0 and a.chatid='"+str(idsi)+"';", self.conn)
#          nomer= [item for item in range(1,len(mavjudmi)+1)]
#          # print(nomer)
#          mavjudmi['nomer'] = nomer
#          mavjudmi['Umumiy_savol'] = pd.to_numeric(mavjudmi['togri_javoblar']) + pd.to_numeric(mavjudmi['notogri_javoblar'])
#
#          mydata = mavjudmi[['nomer', 'Fish','oquvchi_id_id','variant_nomeri_id','Umumiy_savol','togri_javoblar','notogri_javoblar','foizi','sanasi']]
#          # print(mavjudmi.columns)
#          # print
#          mydata.columns = ['Tartib raqami', 'FISH', 'TALABA ID', 'VARIANT ID','Umumiy savollar',"To'g'ri javoblar","Noto'g'ri javoblar","Umumiy ball","Topshirgan sana"]
#
#          # mydata.to_excel("/home/administrator/database/media/natijalar/" + "MarksData.xlsx",index=False)
#
#          # print(mavjudmi)
#          return mydata
#       except Exception as error:
#          print("yakunlashni update qilishda muammo bor", error)
#          return pd.DataFrame()
#
#
#    def setPdf(self, idsi,file):
#       try:
#          #note status 0 ga o'zgarishi kerak
#          mavjudmi = list(pd.read_sql_query(" select * from abituriyent_oquvchilar_malumoti where status=0 and chatid='"+str(idsi)+"';", self.conn)["titul_varaqasi"])
#          # mydata.to_excel("/home/administrator/database/media/natijalar/" + "MarksData.xlsx",index=False)
#          # magelist = glob.glob('rasmlar/*.jpg')
#          # print(mavjudmi)
#          if len(mavjudmi):
#             im = Image.open("/home/administrator/database/media/"+mavjudmi[0])
#             image_list = []
#             # imagelist is the list with all image filenames
#             for i in range(1, len(mavjudmi)):
#                image_list.append(Image.open("/home/administrator/database/media/"+mavjudmi[i]))
#
#             im.save(r"/home/administrator/database/media/natijalar/myPdf/"+file+"", save_all=True, append_images=image_list)
#             return True
#             # print(mavjudmi)
#          return False
#       except Exception as error:
#          print("yakunlashni update qilishda muammo bor", error)
#          return False
#          # return pd.DataFrame()
#
#
# # ob = DBHelper()
# # ob.setPdf("127296547","samar.pdf")
#
#
# #select * from abituriyent_oquvchilar_malumoti as a inner join abituriyent_oquvchilar as b on a.oquvchi_id_id= b.id where a.status=0 and a.chatid='798645375'
