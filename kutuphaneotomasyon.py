import mysql.connector
from datetime import datetime, timedelta


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sqldatabase123",
    database="kutuphanedatabase"
)


cursor = db.cursor()


def add_book():
    title = input("Kitap Adını Giriniz: ")
    author = input("Yazarın Adını Giriniz: ")
    
    query = "INSERT INTO books (title, author, status) VALUES (%s, %s, %s)"
    values = (title, author, "available")
    cursor.execute(query, values)
    db.commit()
    print("Kitap başarılı bir şekilde eklendi.")


def add_patron():
    name = input("Öğrenci Adını Gir: ")
    email = input("Öğrenci E-Posta Adrsini Gir: ")
    
    query = "INSERT INTO patrons (name, email) VALUES (%s, %s)"
    values = (name, email)
    cursor.execute(query, values)
    db.commit()
    
    
    cursor.execute("SELECT LAST_INSERT_ID()")
    patron_id = cursor.fetchone()[0]
    
    print("Öğrenci Profili Oluşturuldu.")
    print("Profil IDsi:", patron_id)
    print() 


def display_available_books():
    cursor.execute("SELECT id, title, author FROM books WHERE status = 'available'")
    available_books = cursor.fetchall()
    
    if available_books:
        print("Erişilebilir Kitaplar:")
        for book in available_books:
            book_id, title, author = book
            print(f"ID: {book_id}, İsim: {title}, Yazar: {author}")
    else:
        print("Erişilebilir Kitap Bulunmamaktadır.")
    print()  


def borrow_book():
    book_id = input("İstediğiniz Kitabın IDsini Yazınız: ")
    patron_id = input("Öğrenci Profil IDnizi Yazınız: ")
    borrowed_date = input("Ödünç Aldığınız Tarihi Giriniz (GG-AA-YYYY): ")
    
   
    borrowed_date = datetime.strptime(borrowed_date, "%d-%m-%Y").strftime("%Y-%m-%d")
    
  
    due_date = (datetime.strptime(borrowed_date, "%Y-%m-%d") + timedelta(weeks=2)).strftime("%Y-%m-%d")
    
   
    cursor.execute("SELECT status FROM books WHERE id = %s", (book_id,))
    status = cursor.fetchone()[0]
    
    if status == "available":
        query = "INSERT INTO borrowings (book_id, patron_id, borrowed_date, due_date) VALUES (%s, %s, %s, %s)"
        values = (book_id, patron_id, borrowed_date, due_date)
        cursor.execute(query, values)
        borrowing_id = cursor.lastrowid 
        cursor.execute("UPDATE books SET status = 'borrowed' WHERE id = %s", (book_id,))
        db.commit()
        print("Kitap Ödünç Alındı.")
        print("Lütfen Kitabı 2 Hafta İçerisinde İade Ediniz.")
        print("Kitabınızın Ödünç IDsi:", borrowing_id)
    else:
      
        cursor.execute("""
            SELECT patrons.name, borrowings.borrowed_date, borrowings.due_date
            FROM borrowings
            INNER JOIN patrons ON patrons.id = borrowings.patron_id
            WHERE borrowings.book_id = %s
        """, (book_id,))
        result = cursor.fetchone()
        patron_name = result[0]
        borrowed_date = result[1]
        due_date = result[2]
        print(f"Kitap {patron_name} isimli öğrenci tarafından ödünç alınmıştır.")
        print(f"Ödünç Alınan Tarih: {borrowed_date}")
        print(f"İade Edileceği Tarih: {due_date}")


def return_book():
    borrowing_id = int(input("Ödünç Alma IDsini Giriniz: "))
    returned_date = input("İade Edildiği Tarihi Giriniz (GG-AA-YYYY): ")
    
    
    returned_date = datetime.strptime(returned_date, "%d-%m-%Y").strftime("%Y-%m-%d")
    
    query = "UPDATE borrowings SET returned_date = %s WHERE id = %s"
    values = (returned_date, borrowing_id)
    
    cursor.execute(query, values)
    
    cursor.execute("SELECT book_id FROM borrowings WHERE id = %s", (borrowing_id,))
    book_id = cursor.fetchone()[0]
    cursor.execute("UPDATE books SET status = 'available' WHERE id = %s", (book_id,))
    
    db.commit()
    print("Kitap İade Edildi.")




while True:
    print("Kütüphane Otomatına Hoşgeldiniz")
    print("1. Kitap Ekle")
    print("2. Profil Ekle")
    print("3. Kitapları Listele")
    print("4. Kitap Ödünç Al")
    print("5. Kitap Teslim Et")
    print("6. Çıkış")
    
    choice = input("Seçeneğinizi Giriniz: ")
    
    if choice == "1":
        add_book()
    elif choice == "2":
        add_patron()
    elif choice == "3":
        display_available_books()
    elif choice == "4":
        borrow_book()
    elif choice == "5":
        return_book()
    elif choice == "6":
        break
    else:
        print("Yanlış Seçim. Lütfen Tekrar Deneyiniz.")
    
    print()  


db.close()
