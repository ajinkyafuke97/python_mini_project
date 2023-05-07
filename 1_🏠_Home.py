import streamlit as st
import mysql.connector
from streamlit_extras.switch_page_button import switch_page

def db_cnx():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Night@123",
        database="ecommerce_management"
    )
    return mydb
def login():


    st.text_input("User Name:",key="user_name",placeholder="Admin")
    st.text_input("Password:",key="password",type="password",placeholder="Password")
    login_btn = st.button("Login")

    if login_btn:
        user_name = st.session_state.user_name
        password = st.session_state.password
        mydb = db_cnx()
        cnx = mydb.cursor()
        cnx.execute(f"select * from Admin where User_Name = '{user_name}' and Password = '{password}'")
        data = cnx.fetchall()
        if data:
            st.success("Logged In")
            if 'Logged_Username' not in st.session_state:
                st.session_state['Logged_Username'] = data[0][1]
                st.session_state['User_Role'] = data[0][4]
            switch_page("Product")
        else:
            st.error("Incorrect User name or Password")


def add_customer():
    st.text_input("username:", key="add_user_name")
    st.text_input("Password:", key="add_password")
    st.text_input("Confirm Password:", key="add_confirm_password")
    add_btn = st.button("Create an Account")

    if add_btn:
        add_user_name = st.session_state.add_user_name
        add_password = st.session_state.add_password
        add_confirm_password = st.session_state.add_confirm_password
        if add_password == add_confirm_password:

            mydb = db_cnx()
            cnx = mydb.cursor()
            sql = f"Select * from admin where user_name = '{add_user_name}'"
            cnx.execute(sql)
            acc_data = cnx.fetchall()

            if acc_data:
                st.error("User name already exist try another user name")
            else:
                sql = "INSERT INTO admin(User_Name,Password,Confirm_Password,Role)VALUES (%s, %s, %s, %s)"
                data1 = (str(add_user_name), str(add_password), str(add_confirm_password), 'Customer')
                print(sql, data1)
                cnx.execute(sql, data1)
                mydb.commit()
                mydb.close()
                st.success(f"{add_user_name} Created please Login" )
        else:
            st.error("Passwords do not match.")
def login_auth():
    if 'Logged_Username' not in st.session_state:
        st.subheader("Login")
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        with tab1:
            login()

        with tab2:
            add_customer()
    else:
        st.success("You already logged in")




if ('Logged_Username' in st.session_state) and ('User_Role' in st.session_state):
    col1,col2 = st.columns(2)
    with col1:
        st.write("Hello",st.session_state.Logged_Username,"(",st.session_state.User_Role,")")
    with col2:
        logout = st.button("Logout")
        if logout:
            del st.session_state.Logged_Username
            del st.session_state.User_Role
            switch_page("Home")
st.title("Wellcome to Ecommerce Website")
st.image("banner.jpg")
login_auth()
