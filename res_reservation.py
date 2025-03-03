import os
os.system("pip install --no-cache-dir --force-reinstall qrcode[pil]")
import streamlit as st
import qrcode
import urllib.parse
from io import BytesIO
# Function to generate QR code
def generate_qr(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=8,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    img_buffer = BytesIO()
    img.save(img_buffer, format="PNG")
    return img_buffer.getvalue()
# Display restaurant logo (Optional)
st.image("sanjha_dhaba.png")
st.write("Please fill the details to proceed with your table reservation...")
# Ensure session state is initialized
if "qr_data" not in st.session_state:
    st.session_state.qr_data = None
if "reservation_done" not in st.session_state:
    st.session_state.reservation_done = False  # Track if reservation is done
# Form for table reservation
with st.form(key="booking"):
    title = st.selectbox("Title", options=["Dr.", "Mr.", "Ms."])
    name = st.text_input("Your name", placeholder="What would you like us to call you?")
    num_people = st.number_input("For how many guests?", min_value=1, max_value=20)
    cuisine = st.multiselect("Preferred Cuisine(s)", ["American", "Chinese", "Continental", "Indian", "Italian", "Mexican", "Chef's special"])
    booze = st.radio("Are you bringing your own booze?", ["No", "Yes", "I don't drink"], horizontal=True)
    dessert = st.multiselect("Preferred Dessert(s)", ["Brownie", "Cake", "Donut", "Ice Cream", "Pastry", "Waffle"])
    date = st.date_input("Select Reservation Date")
    time = st.time_input("Select Reservation Time")
    submit_btn = st.form_submit_button("Reserve my table", type="primary")
if submit_btn:
    if not name.strip():
        st.error("Your name is required to reserve the table.")
    else:
        # Generate reservation summary
        reservation_details = f"""
        Hello **{title} {name}**,\n
        You have booked for **{num_people}** guests.\n
        **Cuisine:** {"None" if not cuisine else ", ".join(cuisine)}\n
        **Dessert:** {"None" if not dessert else ", ".join(dessert)}\n
        Your table has been booked for **{date} at {time}**.\n
        **{"You are bringing your own booze." if booze == "Yes" else "You are NOT bringing your own booze."}**
        """
        st.success("🎊 Congratulations! Your table has been booked.")
        # Generate a URL for the reservation summary page
        params = {
            "title":str(title),
            "name": urllib.parse.quote(name),
            "date": date.strftime("%Y-%m-%d"),
            "time": time.strftime("%H:%M:%S"),
            "guests": str(num_people),
        }
        encoded_params = urllib.parse.urlencode(params)
        reservation_url = f"https://sanjhadhaba.streamlit.app/reservation_summary?{encoded_params}"
        # Store URL in session state
        st.session_state.qr_data = reservation_url
        st.session_state.reservation_done = True  # Mark reservation as completed
        # Debugging: Show the reservation link
        #st.write(f"✅ **Debugging:** Reservation URL: {reservation_url}")
# ✅ Show QR Code button only AFTER reservation is successful
if st.session_state.reservation_done:
    if st.button("Generate QR Code"):
        qr_image = generate_qr(st.session_state.qr_data)
        st.image(qr_image, caption="Scan to view your reservation summary")
        st.download_button("Download QR Code", data=qr_image, file_name="qr_code.png", mime="image/png")
