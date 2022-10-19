import gradio as gr
import pandas as pd
from datetime import datetime
from database import get_database


def load_batch(id):
    try:
        db = get_database()
        batches = db['batches']
        data = batches.find_one({"_id": id})
        batch_dataframe = pd.DataFrame.from_dict(data, orient='index')
        if data == None:
            return gr.Column.update(visible=False), gr.Textbox.update(value=datetime.now().strftime("%H:%M")), None, None, gr.Markdown.update("No existe el lote"), None,gr.Markdown.update("") , None
        else:
            return gr.Column.update(visible=True), gr.Textbox.update(value=datetime.now().strftime("%H:%M")), gr.Dropdown.update(choices=data['brands']), gr.Dropdown.update(choices = data['formats']), gr.Markdown.update(str(data['location'])), gr.Markdown.update(data['formula']),gr.Markdown.update("") , gr.Dataframe.update(value=batch_dataframe)
    except:
        print("Error in loading batch")
        return gr.Column.update(visible=False), gr.Textbox.update(value=datetime.now().strftime("%H:%M")), None, None, gr.Markdown.update("No existe el lote"), None,gr.Markdown.update(""), None,


def reset_values(time, frmt, vol, par, pres, temp, ph, special, sense, uv, etq, observations):
    time = datetime.now().strftime("%H:%M")
    frmt = ""
    vol = 0
    par = 0
    pres = 0
    temp = 0
    ph = 0
    special = 0
    sense = False
    uv = False
    etq = False
    observations = ""
    return time, frmt, vol, par, pres, temp, ph, special, sense, uv, etq, observations


def post_data(batch_dataframe, time, frmt, brand, vol, par, pres, temp, ph, special, sense, uv, etq, observations):
    warning = check_inputs(time, frmt, vol, par, pres, temp, ph, special, sense, uv, etq)
    warning = check_warning(warning)
    log = create_log(time, frmt, brand, vol, par, pres, temp, ph, special, sense, uv, etq, observations)
    batch = load_log(batch_dataframe, log)
    warning = update_data(batch)
    return gr.Column.update(visible=False), warning


def check_inputs(time, frmt, vol, par, pres, temp, ph, special, sense, uv, etq):
    warning = ["0","0","0","0","0","0","0","0","0","0","0"]
    try:
        datetime.strptime(time, '%H:%M')
    except ValueError:
        print("Error in time")
        warning[0]="1"                      #0 Wrong time
    if frmt == "":
        warning[1]="1"                      #1 No format selected
    if frmt == "1,5L" and vol < 1.5:
        warning[2]="1"                      #2 1,5L format but less than 1,5L
    if frmt == "0,5L" and vol < 0.5:        
        warning[2]="1"                      #2 0,5L format but less than 0,5L
    if par <= 10:
        warning[3]="1"                      #3 PAR less than 10
    if pres <= 0 or pres > 20:
        warning[4]="1"                      #4 Pressure out of range
    if temp <= 0:
        warning[5]="1"                      #5 Temperature less than 0
    if ph <= 0 or ph > 14:
        warning[6]="1"                      #6 PH out of range
    if special < 0:
        warning[7]="1"                      #7 Special less than 0
    if sense == False:
        warning[8]="1"                      #8 Sense not OK  
    if uv == False:
        warning[9]="1"                      #9 UV not OK
    if etq == False:
        warning[10]="1"                     #10 Label not OK

    return warning


def check_warning(warning):
    if "1" in warning:
        return gr.Markdown.update("Warning", visible=True)
    else:
        return gr.Markdown.update("OK", visible=False)


def create_log(time, frmt, brand, vol, par, pres, temp, ph, special, sense, uv, etq, observations):
    log = {
        "time": time,
        "format": frmt,
        "brand": brand,
        "volume": vol,
        "par": par,
        "pressure": pres,
        "temperature": temp,
        "ph": ph,
        "special": special,
        "sense": sense,
        "uv": uv,
        "label": etq,
        "observations": observations
    }
    return log


def load_log(batch_dataframe, log):
    batch_dataframe[0][7].append(log)
    batch=df_to_dict(batch_dataframe)
    return batch


def df_to_dict(batch_dataframe):
    batch = {
        "_id": batch_dataframe[0][0],
        "date": batch_dataframe[0][1],
        "formula": batch_dataframe[0][2],
        "location": batch_dataframe[0][3],
        "formats": batch_dataframe[0][4],
        "brands": batch_dataframe[0][5],
        "comments": batch_dataframe[0][6],
        "logs": batch_dataframe[0][7]
    }
    return batch


def update_data(batch):
    id = batch['_id']
    db = get_database()
    batches = db['batches']
    batches.update_one({'_id': id}, {'$set': batch})
    return gr.Markdown.update("Saved!", visible=True)