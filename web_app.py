import gradio as gr
from datetime import datetime
import pandas as pd
from control_calidad import load_batch, reset_values, post_data


batch = {"_id": 0,              # 0
        "date": "None",         # 1
        "formula": "None",      # 2
        "location": 0,          # 3
        "formats": [],          # 4
        "brands": [],           # 5
        "comments":"",          # 6
        "logs": []}             # 7

df = pd.DataFrame.from_dict(batch, orient='index')


with gr.Blocks(css='style.css') as demo:
    batch_dataframe = gr.Dataframe(df, visible=False, col_count=1)
    warning = gr.Dataframe(value=["0","0","0","0","0","0","0","0","0","0","0"], visible=False, type='numpy' , datatype='number')
    proceed_usr = gr.Checkbox(value=False, visible=False)
    with gr.Row() as row1:
        with gr.Column(scale=6):
            batchid = gr.Number(label="Lote")
            get_batch = gr.Button(value="Ir")
            with gr.Column(visible=False) as col1:
                with gr.Row():
                    time = gr.Textbox(value=datetime.now().strftime("%H:%M"), label="Hora", interactive=True)
                    day = gr.Textbox(value=datetime.now().strftime("%d/%m/%Y"), label="Fecha", interactive=True)
                    brand = gr.Dropdown(batch_dataframe.value['data'][5], label="Marca", interactive=True)
                    frmt = gr.Dropdown(batch_dataframe.value['data'][4], label="Formato", interactive=True)
                with gr.Row():
                    vol = gr.Number(label="Volumen")
                    par = gr.Number(label="Par de cierre")
                    pres = gr.Number(label="Presion")
                with gr.Row():
                    temp = gr.Number(label="Temperatura")
                    ph = gr.Number(label="PH")
                    special = gr.Number(label="Special")
                with gr.Row():
                    sense = gr.Checkbox(label="Control organoléptico")
                    uv = gr.Checkbox(label="U.V. Funcionamento")
                    etq = gr.Checkbox(label="Etiquetado")
                with gr.Row():
                    observations = gr.Textbox(label="Observaciones")
                with gr.Row():
                    submit = gr.Button(value="Enviar")
                    reset = gr.Button(value="Reset")
                
        with gr.Column(scale=4):
            with gr.Row():
                formula = gr.Markdown("Formula "+batch_dataframe.value['data'][2][0], elem_id="formula")
                location = gr.Markdown("Location "+str(batch_dataframe.value['data'][3][0]), elem_id="location")
            with gr.Row():
                warning_markdown = gr.Markdown("Warning", visible=False, elem_id="warning")
    

    get_batch.click(load_batch, 
                    inputs=[batchid], 
                    outputs=[col1, time, day, brand, frmt, formula, location, warning_markdown, batch_dataframe, proceed_usr])
    submit.click(post_data, 
                    inputs=[batch_dataframe, time, day, frmt, brand, vol, par, pres, temp, ph, special, sense, uv, etq, observations, proceed_usr, warning], 
                    outputs=[col1, warning, warning_markdown, proceed_usr])
    print(warning)
    reset.click(reset_values, 
                inputs=[],
                outputs=[time, day, frmt, vol, par, pres, temp, ph, special, sense, uv, etq, observations, proceed_usr, warning_markdown])

demo.launch(debug=True)