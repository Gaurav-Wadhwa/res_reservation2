import streamlit as st
import qrcode
import urllib.parse
from io import BytesIO
# Ensure QR code module is available
try:
    import qrcode
except ModuleNotFoundError:
    st.error("❌ QR Code module not found. Try adding `qrcode[pil]` to your `requirements.txt` and redeploying.")
    st.stop()
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
st.image("sanjha_dhaba.png", use_container_width=True)
st.write("Please fill in the details to proceed with your table reservation...")
# Initialize session state variables
if "qr_data" not in st.session_state:
    st.session_state.qr_data = None
if "reservation_done" not in st.session_state:
    st.session_state.reservation_done = False
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
        st.error("❌ Your name is required to reserve the table.")
    else:
        # Generate reservation summary
        reservation_details = f"""
        **Hello {title} {name}!** 🎉  
        - You have booked for **{num_people}** guests.  
        - **Cuisine:** {"None" if not cuisine else ", ".join(cuisine)}  
        - **Dessert:** {"None" if not dessert else ", ".join(dessert)}  
        - **Date & Time:** {date} at {time}  
        - **{"You are bringing your own booze." if booze == "Yes" else "You are NOT bringing your own booze."}**
        """
        st.success("🎊 Congratulations! Your table has been booked.")
        st.write(reservation_details)
        # Generate a URL for the reservation summary page
        params = {
            "title": str(title),
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
# ✅ Show QR Code button only AFTER reservation is successful
if st.session_state.reservation_done:
    if st.button("Generate QR Code"):
        try:
            qr_image = generate_qr(st.session_state.qr_data)
            st.image(qr_image, caption="Scan to view your reservation summary")
            st.download_button("Download QR Code", data=qr_image, file_name="qr_code.png", mime="image/png")
        except Exception as e:
            st.error(f"⚠️ Error generating QR Code: {e}")
            # Fallback: Google Charts API for QR Code
            qr_fallback_url = f"https://chart.googleapis.com/chart?chs=200x200&cht=qr&chl={urllib.parse.quote(st.session_state.qr_data)}"
            st.image(qr_fallback_url, caption="Scan to view your reservation summary")
            st.markdown(f"[Download QR Code]({qr_fallback_url})", unsafe_allow_html=True)