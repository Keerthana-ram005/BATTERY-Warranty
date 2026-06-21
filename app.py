import streamlit as st
import os
from datetime import date

from database import (
    create_tables,
    add_user,
    login_user,
    add_customer,
    get_customer_by_mobile,
    add_warranty,
    add_purchase,
    get_customer_data,
    get_customer_purchase_count,
    add_claim,
    get_claim_history
)


# ----------------- INITIAL SETUP -----------------

create_tables()

st.set_page_config(
    page_title="Battery Warranty Tracker",
    layout="wide"
)

filepath = os.path.join("uploads", filename)

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ----------------- SESSION STATE -----------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


if "user" not in st.session_state:
    st.session_state.user = None


# Stores searched customer mobile
if "search_mobile" not in st.session_state:
    st.session_state.search_mobile = ""


# ----------------- TITLE -----------------

st.title("Battery Warranty Tracker")
st.subheader(
    "Manage battery warranties and expiry dates"
)


# ================= AFTER LOGIN =================

if st.session_state.logged_in:


    st.success(
        f"Welcome {st.session_state.user[1]}"
    )


    # ---------------- LOGOUT ----------------

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False

        st.session_state.user = None

        st.session_state.search_mobile = ""

        st.rerun()


    # ---------------- CUSTOMER SEARCH ----------------

    st.header(
        "Customer Search"
    )


    mobile = st.text_input(
        "Enter Customer Mobile Number"
    )


    if st.button("Get Data"):

        # Store mobile so it stays after rerun
        st.session_state.search_mobile = mobile


    if st.session_state.search_mobile:


        records = get_customer_data(
            st.session_state.search_mobile
        )


        if records:


            st.success(
                "Customer Found"
            )


            purchase_count = (
                get_customer_purchase_count(
                    st.session_state.search_mobile
                )
            )


            st.write(
                "Customer Name:",
                records[0][1]
            )


            st.write(
                "Mobile:",
                records[0][2]
            )


            # Purchase History
            with st.expander(
                f"Purchase History ({purchase_count})",
                expanded=True
            ):
                for record in records:


                    purchase_id = record[0]


                    # ---------------- PURCHASE DETAILS ----------------

                    st.subheader(
                        f"Battery - {record[3]}"
                    )


                    st.write(
                        "Brand:",
                        record[3]
                    )


                    st.write(
                        "Battery Type:",
                        record[4]
                    )


                    st.write(
                        "Serial Number:",
                        record[5]
                    )


                    st.write(
                        "Quantity:",
                        record[6]
                    )


                    st.write(
                        "Purchase Date:",
                        record[7]
                    )


                    st.write(
                        "Expiry Date:",
                        record[8]
                    )


                    st.write(
                        "Warranty Period:",
                        record[10],
                        "Months"
                    )


                    st.write(
                        "Warranty Type:",
                        record[11]
                    )


                    # ---------------- PHOTO DISPLAY ----------------

                    if record[9]:

                        st.image(
                            record[9],
                            width=250
                        )


                    # ---------------- CLAIM HISTORY ----------------

                    claims = get_claim_history(
                        purchase_id
                    )


                    with st.expander(
                        f"Claim History ({len(claims)})"
                    ):


                        if claims:


                            for claim in claims:


                                st.write(
                                    "Claim Date:",
                                    claim[0]
                                )


                                st.write(
                                    "Reason:",
                                    claim[1]
                                )


                                st.write(
                                    "Status:",
                                    claim[2]
                                )


                                st.divider()


                        else:


                            st.info(
                                "No claims made yet"
                            )
                    # ---------------- ADD CLAIM ----------------

                    if st.button(
                        "Add Claim",
                        key=f"add_claim_{purchase_id}"
                    ):

                        st.session_state[
                            f"show_claim_{purchase_id}"
                        ] = True


                    # Show claim form only for selected purchase

                    if st.session_state.get(
                        f"show_claim_{purchase_id}",
                        False
                    ):


                        reason = st.text_area(
                            "Enter Claim Reason",
                            key=f"reason_{purchase_id}"
                        )


                        if st.button(
                            "Submit Claim",
                            key=f"submit_claim_{purchase_id}"
                        ):


                            if reason.strip():


                                add_claim(
                                    purchase_id,
                                    reason
                                )


                                st.success(
                                    "Claim added successfully!"
                                )


                                # Close the claim box
                                st.session_state[
                                    f"show_claim_{purchase_id}"
                                ] = False


                                st.rerun()


                            else:


                                st.error(
                                    "Please enter a claim reason"
                                )


                    st.divider()


        else:


            st.warning(
                "No customer data found"
            )


    # ================= ADD NEW PURCHASE =================


    st.header(
        "Add New Purchase"
    )


    with st.form(
        "purchase_form"
    ):


        # ---------------- CUSTOMER DETAILS ----------------


        st.subheader(
            "Customer Details"
        )


        customer_name = st.text_input(
            "Customer Name"
        )


        customer_mobile = st.text_input(
            "Mobile Number"
        )


        # ---------------- BATTERY DETAILS ----------------


        st.subheader(
            "Battery Details"
        )


        brand = st.text_input(
            "Brand"
        )


        product_type = st.text_input(
            "Battery Type"
        )


        serial_number = st.text_input(
            "Serial Number"
        )


        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=1
        )


        purchase_date = st.date_input(
            "Date of Purchase",
            value=date.today()
        )
        # ---------------- WARRANTY DETAILS ----------------


        st.subheader(
            "Warranty Details"
        )


        warranty_period = st.number_input(
            "Warranty Period (Months)",
            min_value=1,
            step=1
        )


        warranty_type = st.selectbox(
            "Warranty Type",
            [
                "Full Replacement",
                "Pro-Rata"
            ]
        )


        # ---------------- PHOTO CAPTURE ----------------


        st.subheader(
            "Capture Bill / Battery Photo"
        )


        photo = st.camera_input(
            "Take Photo"
        )


        submit = st.form_submit_button(
            "Register Purchase"
        )


        # ---------------- SAVE PURCHASE ----------------


        if submit:


            # Save customer

            add_customer(
                customer_name,
                customer_mobile
            )


            customer = get_customer_by_mobile(
                customer_mobile
            )


            customer_id = customer[0]


            # Save warranty

            warranty_id = add_warranty(
                brand,
                warranty_period,
                warranty_type
            )


            # Save image

            photo_path = None


            if photo:


                filename = (
                    f"{serial_number}.jpg"
                )


                photo_path = os.path.join(
                    UPLOAD_FOLDER,
                    filename
                )


                with open(
                    photo_path,
                    "wb"
                ) as file:


                    file.write(
                        photo.getbuffer()
                    )


            # Save purchase

            add_purchase(
                customer_id,
                brand,
                product_type,
                serial_number,
                quantity,
                str(purchase_date),
                photo_path,
                warranty_id,
                warranty_period
            )


            st.success(
                "Battery purchase registered successfully!"
            )


            st.balloons()


# ================= LOGIN / REGISTER =================


else:


    menu = st.sidebar.selectbox(
        "Menu",
        [
            "Login",
            "Register"
        ]
    )


    # ---------------- LOGIN ----------------


    if menu == "Login":


        st.subheader(
            "Login Section"
        )


        username = st.text_input(
            "Username"
        )


        password = st.text_input(
            "Password",
            type="password"
        )


        if st.button(
            "Login"
        ):


            user = login_user(
                username,
                password
            )


            if user:


                st.session_state.logged_in = True


                st.session_state.user = user


                st.rerun()


            else:


                st.error(
                    "Invalid username or password"
                )


    # ---------------- REGISTER ----------------


    elif menu == "Register":


        st.subheader(
            "Create New Account"
        )


        new_username = st.text_input(
            "Username",
            key="new_user"
        )


        new_password = st.text_input(
            "Password",
            type="password",
            key="new_pass"
        )


        role = st.selectbox(
            "Role",
            [
                "Admin"
            ]
        )


        if st.button(
            "Register"
        ):


            add_user(
                new_username,
                new_password,
                role
            )


            st.success(
                "Admin account created successfully. Please login."
            )