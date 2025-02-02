import streamlit as st
from firebase_config import auth, storage
from mysql_connection import get_connection
import uuid


# Set Page Config
st.set_page_config(page_title="Patient Document Portal", page_icon="🩺", layout="centered")

# Helper functions

def login_user(aadhar_no, password):
    """Authenticate user with Aadhar number and password."""
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT name FROM patients WHERE aadhar_no = %s AND password = %s"
    cursor.execute(query, (aadhar_no, password))
    result = cursor.fetchone()
    conn.close()
    return result

def register_user(name, aadhar_no, mobile_no, email_id, password):
    """Register a new patient with password."""
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO patients (name, aadhar_no, mobile_no, email_id, password) VALUES (%s, %s, %s, %s, %s)"
    try:
        cursor.execute(query, (name, aadhar_no, mobile_no, email_id, password))
        conn.commit()
        conn.close()
        return True
    except:
        conn.rollback()
        conn.close()
        return False

def upload_document(aadhar_no, file):
    """Upload a document to Firebase and store details in MySQL."""
    doc_id = str(uuid.uuid4())  # Generate unique doc_id
    firebase_path = f"documents/{doc_id}.pdf"

    # Upload file to Firebase Storage
    storage.child(firebase_path).put(file)

    # Store file metadata in MySQL
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO documents (aadhar_no, doc_id, doc_name) VALUES (%s, %s, %s)"
    cursor.execute(query, (aadhar_no, doc_id, file.name))
    conn.commit()
    conn.close()
    
    return doc_id

def get_documents(aadhar_no):
    """Fetch all documents uploaded by a user."""
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT doc_id, doc_name FROM documents WHERE aadhar_no = %s"
    cursor.execute(query, (aadhar_no,))
    documents = cursor.fetchall()  # List of tuples (doc_id, doc_name)
    conn.close()
    return documents

# UI Design
st.markdown("<h1 style='text-align: center; color: #2C3E50;'>🩺 Patient Document Portal</h1>", unsafe_allow_html=True)
st.markdown("---")

if "user" not in st.session_state:
    st.session_state["user"] = None
    st.session_state["page"] = "login"

# ------------------ LOGIN PAGE ------------------
if st.session_state["page"] == "login":
    st.subheader("🔑 Login")
    aadhar_no = st.text_input("Aadhar Number")
    password = st.text_input("Password", type="password")
    if st.button("Login", use_container_width=True):
        user = login_user(aadhar_no, password)
        if user:
            st.session_state["user"] = aadhar_no
            st.session_state["page"] = "home"
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.markdown("Don't have an account? [Register New Patient](#)", unsafe_allow_html=True)
    if st.button("Register New Patient", use_container_width=True):
        st.session_state["page"] = "signup"
        st.rerun()

# ------------------ SIGNUP PAGE ------------------
elif st.session_state["page"] == "signup":
    st.subheader("📝 Register New Patient")
    name = st.text_input("Full Name")
    aadhar_no = st.text_input("Aadhar Number")
    mobile_no = st.text_input("Mobile Number")
    email_id = st.text_input("Email ID")
    password = st.text_input("Password", type="password")
    
    if st.button("Register", use_container_width=True):
        if register_user(name, aadhar_no, mobile_no, email_id, password):
            st.success("✅ Registration successful. Please login.")
            st.session_state["page"] = "login"
            st.rerun()
        else:
            st.error("Error in registration. Aadhar number may already exist.")

    st.markdown("[Back to Login](#)", unsafe_allow_html=True)
    if st.button("Back to Login", use_container_width=True):
        st.session_state["page"] = "login"
        st.rerun()

# ------------------ HOME PAGE ------------------
elif st.session_state["page"] == "home":
    st.success(f"✅ Welcome, {st.session_state['user']}!")
    tab1, tab2 = st.tabs(["📂 Upload Documents", "📑 View & Download Documents"])

    # Upload Documents
    with tab1:
        st.subheader("📤 Upload Documents")
        file = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"])
        if st.button("Upload", use_container_width=True) and file:
            doc_id = upload_document(st.session_state["user"], file)
            st.success(f"✅ Document uploaded successfully! Document ID: {doc_id}")

    # View & Download Documents
    with tab2:
        st.subheader("📥 Your Uploaded Documents")
        documents = get_documents(st.session_state["user"])
        
        if documents:
            st.success(f"📌 Found {len(documents)} document(s).")
            for doc_id, doc_name in documents:
                firebase_path = f"documents/{doc_id}.pdf"
                file_url = storage.child(firebase_path).get_url(None)
                st.write(f"📄 **{doc_name}**")
                st.markdown(f"[⬇️ Download]({file_url})", unsafe_allow_html=True)
        else:
            st.warning("⚠️ No documents found. Please upload a document.")

    # Logout Button
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state["user"] = None
        st.session_state["page"] = "login"
        st.rerun()
