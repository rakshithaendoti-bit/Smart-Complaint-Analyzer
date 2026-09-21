import sqlite3
import re


# ================= DATABASE CONNECTION =================

def get_connection():
    connection = sqlite3.connect("complaints.db")
    return connection


# ================= CREATE TABLE =================

def create_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint TEXT NOT NULL,
            category TEXT,
            issue TEXT,
            solution TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


# ================= TEXT CLEANING =================

def clean_text(text):

    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text


# ================= ANALYZE COMPLAINT =================

def analyze_complaint(complaint):

    text = clean_text(complaint)

    category = "Other Issues"
    issue = "General Issue"
    solution = "Please contact customer support for further assistance."


    # ================= LAPTOP / COMPUTER =================

    if any(word in text for word in [
        "laptop", "computer", "pc", "desktop"
    ]):

        category = "Laptop / Computer Issues"

        if any(word in text for word in [
            "slow", "hanging", "hang", "lag", "performance"
        ]):

            issue = "Computer Performance Issue"

            solution = (
                "Restart the computer, close unnecessary applications, "
                "remove unwanted files and check available storage."
            )

        elif any(word in text for word in [
            "battery", "charging", "charge", "charger"
        ]):

            issue = "Battery / Charging Issue"

            solution = (
                "Check the charger and charging port. Try another power "
                "source and check the battery condition."
            )

        elif any(word in text for word in [
            "screen", "display", "black screen"
        ]):

            issue = "Display Issue"

            solution = (
                "Restart the computer and check the display connection. "
                "If the problem continues, contact technical support."
            )

        elif any(word in text for word in [
            "not working", "does not work", "won't work"
        ]):

            issue = "Computer Not Working"

            solution = (
                "Restart the computer and check power connections. "
                "If the issue continues, contact technical support."
            )

        else:

            issue = "General Computer Issue"

            solution = (
                "Restart the computer and check the system settings. "
                "Contact technical support if the problem continues."
            )


    # ================= MOBILE =================

    elif any(word in text for word in [
        "mobile", "phone", "smartphone", "android", "iphone"
    ]):

        category = "Mobile / Phone Issues"

        if any(word in text for word in [
            "battery", "charging", "charge", "charger"
        ]):

            issue = "Mobile Battery / Charging Issue"

            solution = (
                "Check the charger and charging port. Try another charger "
                "and restart the phone."
            )

        elif any(word in text for word in [
            "slow", "hanging", "hang", "lag"
        ]):

            issue = "Mobile Performance Issue"

            solution = (
                "Restart the phone, close background applications and "
                "remove unnecessary files."
            )

        elif any(word in text for word in [
            "screen", "display", "touch"
        ]):

            issue = "Mobile Screen Issue"

            solution = (
                "Restart the phone and check for physical damage. "
                "If the issue continues, contact service support."
            )

        elif any(word in text for word in [
            "not working", "does not work", "won't work"
        ]):

            issue = "Mobile Not Working"

            solution = (
                "Restart the phone and check system updates. "
                "Contact technical support if required."
            )

        else:

            issue = "General Mobile Issue"

            solution = (
                "Restart the phone and check the device settings "
                "and available storage."
            )


    # ================= INTERNET =================

    elif any(word in text for word in [
        "internet", "wifi", "wi-fi", "network", "connection", "data"
    ]):

        category = "Internet / Network Issues"

        if any(word in text for word in [
            "slow", "speed", "very slow"
        ]):

            issue = "Slow Internet Connection"

            solution = (
                "Restart the router, check the network signal and "
                "disconnect unused devices."
            )

        elif any(word in text for word in [
            "disconnect", "disconnecting", "disconnected"
        ]):

            issue = "Internet Disconnection"

            solution = (
                "Restart the router and check the network connection. "
                "Contact your internet service provider if needed."
            )

        elif any(word in text for word in [
            "not working", "no internet", "does not work"
        ]):

            issue = "Internet Not Working"

            solution = (
                "Restart the router and check network cables or Wi-Fi. "
                "Contact your internet service provider if the issue continues."
            )

        else:

            issue = "General Network Issue"

            solution = (
                "Restart the router and check your network connection."
            )


    # ================= APP / WEBSITE =================

    elif any(word in text for word in [
        "youtube", "instagram", "facebook", "whatsapp",
        "website", "web site", "app", "application",
        "browser", "google"
    ]):

        category = "App / Website Issues"

        if any(word in text for word in [
            "not opening", "does not open", "won't open",
            "not working", "does not work"
        ]):

            issue = "Application Not Working"

            solution = (
                "Restart the application, check for updates, "
                "clear the cache and make sure you have a stable "
                "internet connection."
            )

        elif any(word in text for word in [
            "crash", "crashing", "closes"
        ]):

            issue = "Application Crash"

            solution = (
                "Restart the application, clear its cache and "
                "update it to the latest version."
            )

        elif any(word in text for word in [
            "loading", "load"
        ]):

            issue = "Application Loading Issue"

            solution = (
                "Check your internet connection, restart the application "
                "and clear the cache."
            )

        else:

            issue = "General App / Website Issue"

            solution = (
                "Restart the application and check for updates."
            )


    # ================= PAYMENT =================

    elif any(word in text for word in [
        "payment", "money", "transaction", "upi",
        "bank", "amount", "deducted", "refund"
    ]):

        category = "Payment Issues"

        if any(word in text for word in [
            "deducted", "debited", "money deducted"
        ]):

            issue = "Money Deducted"

            solution = (
                "Check your transaction status and bank statement. "
                "If the amount is not refunded, contact bank or payment support."
            )

        elif any(word in text for word in [
            "failed", "failure"
        ]):

            issue = "Payment Failed"

            solution = (
                "Check your account balance and internet connection. "
                "Try the payment again after some time."
            )

        elif "pending" in text:

            issue = "Payment Pending"

            solution = (
                "Wait for the transaction status to update. "
                "Do not make another payment until the status is confirmed."
            )

        else:

            issue = "General Payment Issue"

            solution = (
                "Check the transaction details and contact payment support."
            )


    # ================= DELIVERY =================

    elif any(word in text for word in [
        "delivery", "delivered", "order", "courier",
        "parcel", "package"
    ]):

        category = "Delivery Issues"

        if any(word in text for word in [
            "late", "delay", "delayed", "not received"
        ]):

            issue = "Delivery Delayed"

            solution = (
                "Check the order tracking information and contact "
                "the delivery service if the delay continues."
            )

        elif any(word in text for word in [
            "missing", "lost"
        ]):

            issue = "Package Missing"

            solution = (
                "Check the tracking details and contact the delivery "
                "service or seller."
            )

        else:

            issue = "General Delivery Issue"

            solution = (
                "Check the delivery tracking information and contact "
                "customer support."
            )


    # ================= FOOD =================

    elif any(word in text for word in [
        "food", "meal", "restaurant", "dish",
        "pizza", "burger", "biryani"
    ]):

        category = "Food Issues"

        if any(word in text for word in [
            "bad", "spoiled", "quality", "tasty", "taste"
        ]):

            issue = "Food Quality Issue"

            solution = (
                "Report the food quality issue to the restaurant or "
                "food delivery service and request appropriate assistance."
            )

        elif any(word in text for word in [
            "wrong", "missing", "incorrect"
        ]):

            issue = "Wrong / Missing Food Item"

            solution = (
                "Check the order details and contact customer support "
                "for replacement or refund."
            )

        elif any(word in text for word in [
            "spilled", "damaged"
        ]):

            issue = "Food Damaged During Delivery"

            solution = (
                "Take a photo of the damaged order and contact "
                "customer support for assistance."
            )

        else:

            issue = "General Food Issue"

            solution = (
                "Contact the restaurant or food delivery support."
            )


    # ================= ACCOUNT =================

    elif any(word in text for word in [
        "account", "login", "password", "username",
        "sign in", "signin"
    ]):

        category = "Account Issues"

        if any(word in text for word in [
            "password", "forgot password"
        ]):

            issue = "Password Issue"

            solution = (
                "Use the Forgot Password option and follow the "
                "account recovery instructions."
            )

        elif any(word in text for word in [
            "login", "sign in", "signin"
        ]):

            issue = "Login Issue"

            solution = (
                "Check your username and password. If required, "
                "reset your password using account recovery."
            )

        else:

            issue = "General Account Issue"

            solution = (
                "Check your account settings and contact customer support."
            )


    # ================= SECURITY =================

    elif any(word in text for word in [
        "hack", "hacked", "security", "privacy",
        "suspicious", "unauthorized", "stolen",
        "scam", "fraud"
    ]):

        category = "Security / Privacy Issues"

        if any(word in text for word in [
            "hack", "hacked", "unauthorized"
        ]):

            issue = "Unauthorized Account Activity"

            solution = (
                "Change your password immediately, enable two-factor "
                "authentication and contact the service provider."
            )

        elif "privacy" in text:

            issue = "Privacy Concern"

            solution = (
                "Review privacy settings and remove unnecessary "
                "permissions from applications."
            )

        else:

            issue = "Security Concern"

            solution = (
                "Change your password, enable two-factor authentication "
                "and contact official support if necessary."
            )


    # SAVE RESULT

    save_to_database(
        complaint,
        category,
        issue,
        solution
    )

    return {
        "category": category,
        "issue": issue,
        "solution": solution
    }


# ================= SAVE =================

def save_to_database(
    complaint,
    category,
    issue,
    solution
):

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO complaints
            (complaint, category, issue, solution)
            VALUES (?, ?, ?, ?)
        """, (
            complaint,
            category,
            issue,
            solution
        ))

        connection.commit()

        cursor.close()
        connection.close()

    except Exception as e:

        print("Database Error:", e)


# ================= GET HISTORY =================

def get_history():

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, complaint, category, issue, solution, created_at
            FROM complaints
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()

        cursor.close()
        connection.close()

        return rows

    except Exception as e:

        print("History Error:", e)
        return []


# ================= DELETE HISTORY =================

def delete_history(complaint_id):

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM complaints
            WHERE id = ?
        """, (complaint_id,))

        connection.commit()

        deleted = cursor.rowcount > 0

        cursor.close()
        connection.close()

        return deleted

    except Exception as e:

        print("Delete Error:", e)
        return False


# Create database table when file is loaded
create_table()