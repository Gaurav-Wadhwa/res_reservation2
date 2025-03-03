import streamlit as st
import urllib.parse

def generate_qr(data):
    encoded_data = urllib.parse.quote(data)
    return f"https://quickchart.io/chart?chs=200x200&cht=qr&chl={encoded_data}"
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
        # Generate QR Code using Google API
        qr_url = generate_qr(st.session_state.qr_data)
        
        # Display QR Code
        st.image(qr_url, caption="Scan to view your reservation summary")
        
        # Download QR Code (as a clickable link)
        st.markdown(f"[Download QR Code]({qr_url})", unsafe_allow_html=True)
