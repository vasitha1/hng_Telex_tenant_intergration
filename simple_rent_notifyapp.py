"""
This is a simplified version of an app which notifies a tenenat when a rent is due
"""

from flask import Flask, request, jsonify  
import requests  

app = Flask(__name__)  

@app.route('/notify', methods=['POST'])  
def notify():  
    # Simulate receiving data (in a real application this would come from somewhere else)  
    client_phone = '+237698827753'  
    client_name = 'Sulem Vasitha'  
    due_date = '19/02/2025'  

    # Check if the current date is past the due date (this is a basic check)  
    from datetime import datetime  

    # Format the due_date to match the datetime object  
    due_date_obj = datetime.strptime(due_date, '%d/%m/%Y')  
    current_date = datetime.now()  

    if current_date > due_date_obj:  # If rent is overdue  
        # Prepare the payload to send to Telex  
        url = "https://ping.telex.im/v1/webhooks/0195232c-ced9-7439-9036-8d26c8350f89"  
        payload = {  
            "event_name": "Rent Overdue Notification",  
            "message": f'Rent is overdue for {client_name}. Due date was {due_date}.',  
            "status": "success",  
            "username": client_name  
        }  

        # Send the notification to Telex  
        response = requests.post(  
            url,  
            json=payload,  
            headers={  
                "Accept": "application/json",  
                "Content-Type": "application/json"  
            }  
        )  

        # Check if the request was successful  
        if response.status_code == 202:  
            return jsonify({'status': 'Notification sent to Telex'}), 202  
        else:  
            return jsonify({'status': 'Failed to send notification', 'error': response.text}), response.status_code  
    else:  
        return jsonify({'status': 'No overdue notification needed'}), 202 

if __name__ == '__main__':  
    app.run(debug=True)  