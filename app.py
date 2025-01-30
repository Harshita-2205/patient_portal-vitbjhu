import streamlit as st
from firebase_config import auth, storage
from mysql_connection import get_connection
import uuid

# Helper functions
def login_user(aadhar_no, password):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT name FROM patients WHERE aadhar_no = %s AND password = %s"
    cursor.execute(query, (aadhar_no, password))
    result = cursor.fetchone()
    conn.close()
    return result

def register_user(name, aadhar_no, mobile_no, password):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO patients (name, aadhar_no, mobile_no, password) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(query, (name, aadhar_no, mobile_no, password))
        conn.commit()
        conn.close()
        return True
    except:
        conn.rollback()
        conn.close()
        return False

def upload_document(aadhar_no, file):
    doc_id = str(uuid.uuid4())
    firebase_path = f"documents/{doc_id}.pdf"
    storage.child(firebase_path).put(file)
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO documents (aadhar_no, doc_id, doc_name) VALUES (%s, %s, %s)"
    cursor.execute(query, (aadhar_no, doc_id, file.name))
    conn.commit()
    conn.close()
    return doc_id

# Streamlit App
st.title("Patient Portal")

menu = st.sidebar.selectbox("Menu", ["Login", "Signup", "Home"])

if menu == "Login":
    st.subheader("Login")
    aadhar_no = st.text_input("Aadhar Number")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = login_user(aadhar_no, password)
        if user:
            st.success(f"Welcome, {user[0]}!")
            st.session_state["user"] = aadhar_no
        else:
            st.error("Invalid credentials")

if menu == "Signup":
    st.subheader("Signup")
    name = st.text_input("Name")
    aadhar_no = st.text_input("Aadhar Number")
    mobile_no = st.text_input("Mobile Number")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if register_user(name, aadhar_no, mobile_no, password):
            st.success("Registration successful. Please login.")
        else:
            st.error("Error in registration")

if menu == "Home":
    if "user" in st.session_state:
        st.subheader("Upload Documents")
        file = st.file_uploader("Upload PDF", type=["pdf", "docx"])
        if st.button("Upload") and file is not None:
            doc_id = upload_document(st.session_state["user"], file)
            st.success(f"Document uploaded successfully! Doc ID: {doc_id}")
    else:
        st.warning("Please login first.")
