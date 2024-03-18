# importing necessary libraries 
from flask import Flask, g, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def main(): 
    return render_template('main.html')

@app.route('/send-message/', methods=['POST', 'GET'])
def send_message(): 
   if request.method == 'GET': 
    return render_template('submit.html')
   
   else:
      try: 
        insert_message(request) # running insert message 
        return render_template('submit.html', name=request.form['name'], message=request.form['message']) # returns submit html with the successful submission
      except: 
         return render_template('submit.html') 
      
@app.route('/view/')
def view(): 
  limit = 5
  mylist=random_messages(limit) # runs the random amt of messages
  return render_template('view.html', message_list = mylist)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# functions 
def get_message_db():
    # purpose: to handle a database full of messages 
    if 'db' not in g: 
       g.message_db = sqlite3.connect('message_db.sqlite')

    conn = g.message_db
    cursor = conn.cursor()

    # creating the table if it does not exist 
    cursor.execute("CREATE TABLE IF NOT EXISTS messages (handle TEXT, message TEXT);")

    return g.message_db

def insert_message(request):
  # extracting the message and handle from the request 
  message = request.form["message"]
  handle = request.form["name"]

  db = get_message_db() 
  error = None # keeping track of empty messages 

  if not message: 
    error = "Message is required."
  elif not handle: 
    error = "Name is required."

  if error is None: 
     db.execute("INSERT INTO messages (handle, message) VALUES (?,?)", (handle, message)) # query to add the messages to the db 
     db.commit() 

  db.close() 

  return message, handle
  
def random_messages(n): 
   """
   Returns random messages
   """

   db = get_message_db() 
   cursor = db.cursor() 
  
   cursor.execute("SELECT message, handle FROM messages ORDER BY RANDOM() LIMIT (?)", (n,))
   messages = cursor.fetchall()

   db.close() 

   return messages 