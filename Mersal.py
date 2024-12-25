import sqlite3
import streamlit as st

# إعداد قاعدة البيانات
def initialize_database():
    conn = sqlite3.connect('Mersal.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS correspondences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL,
        sender_receiver TEXT NOT NULL,
        date TEXT NOT NULL,
        status TEXT NOT NULL,
        expected_response_date TEXT,
        notes TEXT
    )
    ''')
    conn.commit()
    conn.close()

# إضافة مراسلة جديدة
def add_correspondence(subject, sender_receiver, date, status, expected_response_date, notes):
    conn = sqlite3.connect('Mersal.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO correspondences (subject, sender_receiver, date, status, expected_response_date, notes)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (subject, sender_receiver, date, status, expected_response_date, notes))
    conn.commit()
    conn.close()

# عرض جميع المراسلات
def view_correspondences():
    conn = sqlite3.connect('Mersal.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM correspondences')
    rows = cursor.fetchall()
    conn.close()
    return rows

# تحديث حالة المراسلة
def update_correspondence(correspondence_id, new_status, new_notes):
    conn = sqlite3.connect('Mersal.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE correspondences
    SET status = ?, notes = ?
    WHERE id = ?
    ''', (new_status, new_notes, correspondence_id))
    conn.commit()
    conn.close()

# حذف مراسلة
def delete_correspondence(correspondence_id):
    conn = sqlite3.connect('Mersal.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM correspondences WHERE id = ?', (correspondence_id,))
    conn.commit()
    conn.close()

# تطبيق Streamlit
def main():
    st.title("مرسال - إدارة المراسلات")

    menu = ["إضافة مراسلة", "عرض المراسلات", "تحديث مراسلة", "حذف مراسلة"]
    choice = st.sidebar.selectbox("القائمة", menu)

    if choice == "إضافة مراسلة":
        st.subheader("إضافة مراسلة جديدة")
        subject = st.text_input("الموضوع")
        sender_receiver = st.text_input("الجهة المرسلة/المستقبلة")
        date = st.date_input("التاريخ")
        status = st.selectbox("الحالة", ["قيد الانتظار", "منجزة"])
        expected_response_date = st.date_input("تاريخ الرد المتوقع")
        notes = st.text_area("ملاحظات")
        if st.button("إضافة"):
            add_correspondence(subject, sender_receiver, str(date), status, str(expected_response_date), notes)
            st.success("تمت إضافة المراسلة بنجاح!")

    elif choice == "عرض المراسلات":
        st.subheader("عرض جميع المراسلات")
        data = view_correspondences()
        if data:
            for row in data:
                st.write(f"رقم: {row[0]}, الموضوع: {row[1]}, الجهة: {row[2]}, التاريخ: {row[3]}, الحالة: {row[4]}, الرد المتوقع: {row[5]}, ملاحظات: {row[6]}")
        else:
            st.info("لا توجد مراسلات مسجلة.")

    elif choice == "تحديث مراسلة":
        st.subheader("تحديث حالة مراسلة")
        correspondence_id = st.number_input("رقم المراسلة", min_value=1, step=1)
        new_status = st.selectbox("الحالة الجديدة", ["قيد الانتظار", "منجزة"])
        new_notes = st.text_area("الملاحظات الجديدة")
        if st.button("تحديث"):
            update_correspondence(correspondence_id, new_status, new_notes)
            st.success("تم تحديث المراسلة بنجاح!")

    elif choice == "حذف مراسلة":
        st.subheader("حذف مراسلة")
        correspondence_id = st.number_input("رقم المراسلة", min_value=1, step=1)
        if st.button("حذف"):
            delete_correspondence(correspondence_id)
            st.warning("تم حذف المراسلة بنجاح!")

# تشغيل البرنامج
if __name__ == '__main__':
    initialize_database()
    main()
