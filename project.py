import sqlite3 

from datetime import datetime

now = datetime.now()

    
def update_table(cursor,sqliteconnection,table,update_data):
    
    ###UPDATE ΚΑΝΩ ΣΤΙΣ ΠΡΟΣΩΡΙΝΕΣ ΕΚΘΕΣΕΙΣ(ΗΜΕΡΟΜΗΝΙΕΣ) ΚΑΙ ΑΝΤΙΓΡΑΦΑ(ΤΙΜΕΣ)
    if (table=="1"):#ΕΚΘΕΣΗ
        [id_temp_exhibition,start_date,closing_date]=update_data.split(',')
        sql= "UPDATE Temp_exhibition SET start_date=?,closing_date=? WHERE id_temp_exhibition=?"
        cursor.execute(sql,(start_date,closing_date,int(id_temp_exhibition)))
    
        
    elif (table=="2"):#ΑΝΤΙΓΡΑΦΟ
        [id_painting,price]=update_data.split(',')
        sql="UPDATE Copy SET price=? WHERE id_painting=?"
        cursor.execute(sql,(price,int(id_painting)))
    
    

def insert_into_table(cursor,sqliteconnection,table,insert_data):
    if (table=="1"):#ΕΙΣΙΤΗΡΙΟ
        sql= "INSERT INTO Ticket(id_ticket,duration,price,date_of_print) VALUES(?,?,?,?);"  
        if len(insert_data.split(','))==4:
            [id_ticket,duration,price,date_of_print]=insert_data.split(',')
            cursor.execute(sql,(insert_data.split(',')))
            typetick= input("Τύπος εισιτηρίου: (1)Προσωρινής Εκθεσης (2)Μόνιμης Έκθεσης (3)Και τα δύο:\n")
            if(typetick=="1"):
                cursor.execute("SELECT id_temp_exhibition FROM Temp_exhibition WHERE start_date<date('now') AND closing_date>date('now') ")
                result=cursor.fetchall()
                print(result)
                id_exhibition=result[0][0]
                sql="INSERT INTO Ticket_Temp(id_ticket_temp,id_exhibition) VALUES(?,?);"
                cursor.execute(sql,(int(id_ticket),int(id_exhibition))) 
            elif(typetick=="2"):
                cursor.execute("SELECT id_perm_exhibition FROM Perm_exhibition")
                result=cursor.fetchall()
                id_exhibition=result[0][0]
                sql="INSERT INTO Ticket_Perm(id_ticket_perm,id_exhibition) VALUES(?,?);"
                cursor.execute(sql,(int(id_ticket),int(id_exhibition)))
            elif(typetick=="3"):
                #ΕΝΑΣ ΑΡΙΘΜΟΣ ΕΙΣΙΤΗΡΙΟΥ ΚΑΙ ΣΤΙΣ ΔΥΟ ΕΚΘΕΣΕΙΣ
                cursor.execute("SELECT id_temp_exhibition FROM Temp_exhibition WHERE start_date<date('now') AND closing_date>date('now')")
                result=cursor.fetchall()
                id_exhibition=result[0][0]
                sql="INSERT INTO Ticket_Temp(id_ticket_temp,id_exhibition) VALUES(?,?);"
                cursor.execute(sql,(int(id_ticket),int(id_exhibition)))
                cursor.execute("SELECT id_perm_exhibition FROM Perm_exhibition")
                result=cursor.fetchall()
                id_exhibition=result[0][0]
                sql="INSERT INTO Ticket_Perm(id_ticket_perm,id_exhibition) VALUES(?,?);"
                cursor.execute(sql,(int(id_ticket),int(id_exhibition)))
            else: print("Invalid")
                            
    elif(table=="2"):#ΕΚΘΕΣΗ
        #Η μόνη έκθεση που μπορούμε να προσθέσουμε ειναι ειναι προσωρινή η οποία αλλάζει
        #ο πινακασ exhibition θα περιέχει όλες τις εκθέσεις με τα ονοματά τους
        [id_temp_exhibition,start_date,closing_date,name_of_exhibition]=insert_data.split(',')
        sql="INSERT INTO Exhibition(id_exhibition,name_of_exhibition) VALUES(?,?)"
        cursor.execute(sql,(int(id_temp_exhibition),name_of_exhibition)) 
        
        sql= "INSERT INTO Temp_exhibition(id_temp_exhibition,start_date,closing_date) VALUES(?,?,?)"
        cursor.execute(sql,(int(id_temp_exhibition),start_date,closing_date))
    
       
    elif(table=="3"):#ΠΙΝΑΚΑΣ
        sql= "INSERT INTO Painting(id_painting,title,dimensions,price,artist,movement,year,process_of_painting) VALUES(?,?,?,?,?,?,?,?)"
        [id_painting,title,dimensions,price,artist,movement,year,process_of_painting]=insert_data.split(',')
        cursor.execute("SELECT id_painting FROM Painting WHERE title= ?" ,(title,))
        exists= cursor.fetchall()
        if len(exists)==0:
            #o pinakas den uparxei kai ton prosthetoume
            cursor.execute(sql,(int(id_painting),title,dimensions,price,artist,movement,year,process_of_painting))

            #Elegxw an uparxei o artist
            cursor.execute("SELECT First_Last_name FROM Artist WHERE First_Last_name= ?" ,(artist,))
            existsart= cursor.fetchall()
            if len(existsart)==0:
                #den uparxei o artist ton prosthetw
                sql= "INSERT INTO Artist(First_Last_name,nationality,active_period) VALUES(?,?,?)"
                artist_data=input("Artist: (First_Last_name, nationality, active_period):")
                if(len(artist_data.split(","))==3):
                    cursor.execute(sql,(artist_data.split(',')))
                else:print("Δεν έγινε η καταχώρηση του Artist")
                result=input("Δώστε τον αναγνωριστικό αριθμό της έκθεσης που θα υπάρχει ο πίνακας: ")
                id_exhibition= int(result)
                sql= "INSERT INTO presents(id_exhibition,id_painting) VALUES(?,?)"
                cursor.execute(sql,(id_exhibition,int(id_painting)))
                   
            
        else:
            print("exists")

    elif(table=="4"):#ΑΝΤΙΓΡΑΦΟ
        sql= "INSERT INTO Copy(id_painting,title_of_painting,number_of_copies,price) VALUES(?,?,?,?)"
        [id_painting,number_of_copies,price]=insert_data.split(",")
        cursor.execute("SELECT id_painting FROM Copy WHERE id_painting=?",(id_painting,))
        exists=cursor.fetchall()
        if len(exists)==0:#den uparxoun alla copies tou sugkekrimenou pinaka
            cursor.execute("SELECT title FROM Painting WHERE id_painting=?",(id_painting,))
            result=cursor.fetchall()
            title_of_painting=result[0][0]
            
            cursor.execute(sql,(int(id_painting),title_of_painting,int(number_of_copies),price))
        else:#uparxei to sugk copy
            cursor.execute("SELECT number_of_copies FROM Copy WHERE id_painting=?",(id_painting,))
            result=cursor.fetchall()
            new_number=result[0][0]+int(number_of_copies)
            cursor.execute("UPDATE Copy SET number_of_copies=? WHERE id_painting=?",(new_number,id_painting))
                  
        
    elif(table=="5"):#ΑΓΟΡΑ
        sql= "INSERT INTO Purchase(receipt,date_of_purchase,title_of_painting,total_price) VALUES(?,?,?,?)"
        [receipt,id_painting]=insert_data.split(",")
        date_of_purchase=now.strftime("%m/%d/%Y")
        cursor.execute("SELECT number_of_copies FROM Copy WHERE id_painting=?",(id_painting,))
        num=cursor.fetchall()
        if(num==0 or num==[]):
            print("ΔΕΝ ΥΠΑΡΧΟΥΝ ΔΙΑΘΕΣΙΜΑ ΑΝΤΙΓΡΑΦΑ")
        else:
            
            cursor.execute("SELECT title_of_painting,price FROM Copy WHERE id_painting=?",(id_painting,))
            result=cursor.fetchall()
            title_of_painting=result[0][0]
            price=result[0][1]
            cursor.execute("UPDATE Copy SET number_of_copies=number_of_copies-1 WHERE id_painting=?",(id_painting,))
            cursor.execute(sql,(int(receipt),date_of_purchase,title_of_painting,price))
        


def delete(cursor,sqliteconnection,table,deldata):
    if(table=="1"):#ΕΙΣΙΤΗΡΙΟ
        sql="DELETE FROM Ticket WHERE id_ticket=?"
        cursor.execute(sql,(deldata,))
        sql="DELETE FROM Ticket_Temp WHERE id_ticket_temp=?"
        cursor.execute(sql,(deldata,))
        sql="DELETE FROM Ticket_Perm WHERE id_ticket_perm=?"
        cursor.execute(sql,(deldata,))
    elif(table=="2"):#ΕΚΘΕΣΗ
        sql="DELETE FROM Exhibition WHERE id_exhibition=?"
        cursor.execute(sql,(deldata,))
        sql="DELETE FROM Temp_exhibition WHERE id_temp_exhibition=?"
        cursor.execute(sql,(deldata,))
        sql="DELETE FROM Perm_exhibition WHERE id_perm_exhibition=?"
        cursor.execute(sql,(deldata,))
    elif(table=="3"):#ΠΙΝΑΚΑΣ
        sql="DELETE FROM Painting WHERE id_painting=?"
        cursor.execute(sql,(deldata,))
        sql="DELETE FROM Copy WHERE id_painting=?"
        cursor.execute(sql,(deldata,))
        sql="DELETE FROM presents WHERE id_painting=?"
        cursor.execute(sql,(deldata,))
    elif(table=="4"):#ΑΝΤΙΓΡΑΦΟ
        sql="DELETE FROM Copy WHERE id_painting=?"
        cursor.execute(sql,(deldata,))
    elif(table=="5"):#ΑΓΟΡΑ
        sql="DELETE FROM Purchase WHERE receipt=?"
        cursor.execute(sql,(deldata,))

def show2(cursor,result):
    column=[col[0] for col in cursor.description]
    for c in column:
        print(c,end=',')       
    for res in result:
        print("\n")
        for each in res:
            print(each, end='\t')
    print("\n")
    
    
   
def show(cursor,sqliteconnection,table):#1)ΕΙΣΙΤΗΡΙΟ 2)ΕΚΘΕΣΗ 3)ΠΙΝΑΚΑΣ 4)ΑΝΤΙΓΡΑΦΟ 5)ΑΓΟΡΑ 6)ΚΑΛΛΙΤΕΧΝΗΣ
    if(table=="3"):
        cursor.execute("SELECT * FROM Painting")
    elif(table=="1"):
        cursor.execute("SELECT * FROM Ticket")
    elif(table=="2"):
        cursor.execute("SELECT * FROM Exhibition")
    elif(table=="4"):
        cursor.execute("SELECT * FROM Copy")
    elif(table=="5"):
        cursor.execute("SELECT * FROM Purchase")
    elif(table=="6"):
        cursor.execute("SELECT * FROM Artist")
    result=cursor.fetchall()
    show2(cursor,result)
        



def main():
    
    
    sqliteconnection= sqlite3.connect('database.db')
    cursor = sqliteconnection.cursor()
    print("Database created and Successfully Connected to SQLite\n\n")
    print("Ομάδα Χρηστών 44 Eφαρμογή πινακοθήκης")
        
    while(True):
        request=input("\nΔιαθέσιμες Λειτουργίες:\n1)Εισαγωγή Δεδομένων\n2)Αλλαγή Δεδομένων\
                    \n3)Διαγραφή Δεδομένων\n4)Εμφάνιση Δεδομένων\n5)Ερωτήματα SQL\n6)Έξοδος\nΕπιλέξτε μια απο τις παραπάνω λειτουργίες(1-6) : ")
    ######################################################################################################
        if(request=="1"):
            #insert
            table=input("\nΕπιλέξτε Πίνακα:\n1)ΕΙΣΙΤΗΡΙΟ\n2)ΕΚΘΕΣΗ\n3)ΠΙΝΑΚΑΣ\n4)ΑΝΤΙΓΡΑΦΟ\n5)ΑΓΟΡΑ\nΕπιλογή: ")
            
            if (table=="1"):#ΕΙΣΙΤΗΡΙΟ
                cursor.execute("SELECT MAX(id_ticket) FROM Ticket ")
                result= cursor.fetchall()
                id_ticket=result[0][0]+1
                insert_data= str(id_ticket)+(",")+input("{ΔΙΑΡΚΕΙΑ,ΤΙΜΗ}:")+(",")+ now.strftime("%m/%d/%Y")
                if (len((insert_data).split(","))!=4):
                    print("Δεν έγινε η καταχώρηση")
                    continue
                
            elif(table=="2"):#ΕΚΘΕΣΗ
                cursor.execute("SELECT MAX(id_temp_exhibition) FROM Temp_exhibition ")
                result=cursor.fetchall()
                id_temp_exhibition= result[0][0]+1
                insert_data=str(id_temp_exhibition)+(',')+input("{start_date,closing_date,name_of_exhibition}:")
                if(len(insert_data.split(","))!=4):
                    print("Δεν έγινε η καταχώρηση")
                    continue
            elif(table=="3"):#ΠΙΝΑΚΑΣ
                #βρισκω το τελευταίο id_painting για να συνεχίσω απο εκεί την καταχώρηση
                cursor.execute("SELECT MAX(id_painting) FROM Painting  ")
                result= cursor.fetchall()
                id_painting=result[0][0]+1
                insert_data=str(id_painting)+(",")+input("{title,dimentions,price,artist}:")+(",")+input("{movement,year,process_of_painting}:")
                if(len(insert_data.split(","))!=8):
                    print("Δεν έγινε η καταχώρηση")
                    continue
            elif(table=="4"):#ΑΝΤΙΓΡΑΦΟ
                insert_data=input("{id_painting,number_of_copies,price}:")
                if(len(insert_data.split(","))!=3):
                    print("Δεν έγινε η καταχώρηση")
                    continue
            elif(table=="5"):#ΑΓΟΡΑ
                cursor.execute("SELECT MAX(receipt) FROM Purchase  ")
                result= cursor.fetchall()
                receipt=result[0][0]+1
                insert_data=str(receipt)+(",")+input("{id_painting}:")
                if(len(insert_data.split(","))!=2):
                    print("Δεν έγινε η καταχώρηση")
                    continue
                
                               
                
            insert_into_table(cursor,sqliteconnection,table,insert_data)
            sqliteconnection.commit()
        ######################################################################################################
        elif(request=="2"):
            #update
            table=input("\nΕπιλέξτε πίνακα:\n1)ΕΚΘΕΣΗ(αλλαγή ημερομηνιών προσωρινής έκθεσης)\n2)ΑΝΤΙΓΡΑΦΟ(αλλαγή τιμών)\nΕπιλογή: ")
            if(table=="1"):#ΕΚΘΕΣΗ
                update_data=input("Δώστε τον ανγνωριστικό αριθμό έκθεσης και τις νέες ημερομηνίες{id_temp_exhibition,start_date,closing_date}:")
                if(len(update_data.split(","))!=3):
                    print("Δεν έγινε η αλλαγή")
                    continue
            elif(table=="2"):#ΑΝΤΙΓΡΑΦΟ
                update_data=input("Δώστε τον αναγνωριστικό αριθμό του πίνακα που έχει το αντίγραφο και την νέα τιμή{id_painting,price}:")
                if(len(update_data.split(","))!=2):
                    print("Δεν έγινε η αλλαγή")
                    continue
            update_table(cursor,sqliteconnection,table,update_data)  
            sqliteconnection.commit()
            
        ######################################################################################################
        elif (request=="3"):
            #delete
            table=input("Επιλέξτε που θα θέλατε να γίνει διαγραφή:\n1)ΕΙΣΙΤΗΡΙΟ\n2)ΕΚΘΕΣΗ\n3)ΠΙΝΑΚΑΣ\n4)ΑΝΤΙΓΡΑΦΟ\n5)ΑΓΟΡΑ\nΕπιλογή: ")
            if(table=="1"):#ΕΙΣΙΤΗΡΙΟ
                deldata=input("Δώστε τον αναγνωριστικό αριθμό εισιτηρίου που θα θέλατε να διαγραφεί:")
            elif(table=="2"):#ΕΚΘΕΣΗ
                deldata=input("Δώστε τον αναγνωριστικό αριθμό της έκθεσης που θα θέλατε να διαγραφεί:")
            elif(table=="3"):#ΠΙΝΑΚΑΣ
                deldata=input("Δώστε τον αναγνωριστικό αριθμό του πίνακα που θα θέλατε να διαγραφεί:")
            elif(table=="4"):#ΑΝΤΙΓΡΑΦΟ
                deldata=input("Δώστε τον αναγνωριστικό αριθμό πινακα που έχει αντίγραφα και θα θέλατε να διαγραφεί:")
            elif(table=="5"):#ΑΓΟΡΑ
                deldata=input("Δώστε τον αναγνωριστικό αριθμό απόδειξης αγοράς που θα θέλατε να διαγραφεί:")

            delete(cursor,sqliteconnection,table,deldata)
            sqliteconnection.commit()

        ######################################################################################################     
        elif (request=="4"):
            #show
            table=input("Επιλέξτε Πίνακα:\n1)ΕΙΣΙΤΗΡΙΟ\n2)ΕΚΘΕΣΗ\n3)ΠΙΝΑΚΑΣ\n4)ΑΝΤΙΓΡΑΦΟ\n5)ΑΓΟΡΑ\n6)ΚΑΛΛΙΤΕΧΝΗΣ\nΕπιλογή: ")
            show(cursor,sqliteconnection,table)
        ######################################################################################################
        elif (request=="5"):
            res=input("ΕΡΩΤΗΜΑΤΑ SQL:\n1)ΕΜΦΑΝΙΣΕ ΤΟΥΣ ΤΙΤΛΟΥΣ ΟΛΩΝ ΤΩΝ ΠΙΝΑΚΩΝ ΠΟΥ ΥΠΡΑΧΟΥΝ ΣΤΗΝ ΠΙΝΑΚΟΘΗΚΗ ΚΑΘΩΣ ΚΑΙ ΤΟΝ ΚΑΛΛΙΤΕΧΝΗ ΠΟΥ ΤΟΥΣ ΔΗΜΙΟΥΡΓΗΣΕ\n\
2)ΕΜΦΑΝΙΣΕ ΤΟΝ ΑΡΙΘΜΟ ΤΩΝ ΕΙΣΙΤΗΡΙΩΝ ΠΟΥ ΕΧΟΥΝ ΕΚΔΟΘΕΙ ΣΤΙΣ 01/15/2022\n\
3)ΕΜΦΑΝΙΣΕ ΤΟΥΣ ΤΙΤΛΟΥΣ ΟΛΩΝ ΤΩΝ ΠΙΝΑΚΩΝ ΠΟΥ ΕΧΕΙ Η ΠΡΟΣΩΡΙΝΗ ΕΚΘΕΣΗ\n\
4)ΕΜΦΑΝΙΣΕ ΤΗΝ ΠΡΟΣΩΡΙΝΗ ΕΚΘΕΣΗ ΠΟΥ ‘’ΤΡΕΧΕΙ’’ ΑΥΤΗ ΤΗΝ ΠΕΡΙΟΔΟ\n\
5)ΕΜΦΑΝΙΣΕ ΠΟΣΑ ΑΝΤΙΓΡΑΦΑ ΤΟΥ ΠΙΝΑΚΑ MONA LISA ΕΧΟΥΝ ΑΓΟΡΑΣΤΕΙ\n\
6)ΕΜΦΑΝΙΣΕ ΠΟΣΑ ΕΙΣΙΤΗΡΙΑ ΕΚΔΟΘΗΚΑΝ ΓΙΑ ΤΗΝ ΜΟΝΙΜΗ ΕΚΘΕΣΗ\nΕπιλογή: ")
            if(res=="1"):
                cursor.execute("SELECT title,artist FROM Painting")

            elif(res=="2"):
                cursor.execute("SELECT count(id_ticket) FROM Ticket WHERE date_of_print='01/15/2022'")
            elif(res=="3"):
                cursor.execute("SELECT p.title FROM Temp_exhibition, Exhibition as e,presents as pr, Painting as p WHERE id_temp_exhibition=e.id_exhibition AND pr.id_exhibition=e.id_exhibition AND pr.id_painting=p.id_painting")
            elif(res=="4"):
                cursor.execute("SELECT name_of_exhibition FROM Temp_exhibition, Exhibition as e WHERE id_temp_exhibition=e.id_exhibition AND start_date<date('now') AND closing_date>date('now')")
            elif(res=="5"):
                cursor.execute("SELECT count(title_of_painting) FROM Purchase WHERE title_of_painting='Mona Lisa'")
            elif(res=="6"):
                cursor.execute("SELECT count(id_ticket_perm) FROM Ticket_Perm")
            result=cursor.fetchall()
            show2(cursor,result)
        elif(request=="6"):
            #exit
            break
            return 1
        
        else: print("Invalid")
    cursor.close()
    sqliteconnection.close()

if __name__=='__main__':

    main()

   
        


