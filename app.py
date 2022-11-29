from flask import Flask, request
import sys
import pip
from application.util.utililty import read_yaml_file, write_yaml_file
from matplotlib.style import context
from application.logger import logging
from application.exception import BackorderException
import os, sys
import json
from application.config.configration import Configration
from application.constant import CONFIGRATION_DIR, CURRENT_TIME_STAMP
from application.pipeline.pipeline import Pipeline
from application.entity.backorder_predictor import BackOrderPredictor, BackorderData
from application.logger import get_log_dataframe
from flask import send_file, abort, render_template


ROOT_DIR = os.getcwd()
LOG_FOLDER_NAME = "logs"
PIPELINE_FOLDER_NAME = "application"
SAVED_MODELS_DIR_NAME = "saved_models"
MODEL_CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIGRATION_DIR, "model.yaml")
LOG_DIR = os.path.join(ROOT_DIR, LOG_FOLDER_NAME)
PIPELINE_DIR = os.path.join(ROOT_DIR, PIPELINE_FOLDER_NAME)
MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_DIR_NAME)



BACKORDER_DATA_KEY = "backorder_data"
WENT_ON_BACKORDER_KEY = "went_on_backorder"

app = Flask(__name__)


@app.route('/storage', defaults={'req_path': 'application'})
@app.route('/storage/<path:req_path>')
def render_artifact_dir(req_path):
    os.makedirs("application", exist_ok=True)
    # Joining the base and the requested path
    print(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        if ".html" in abs_path:
            with open(abs_path, "r", encoding="utf-8") as file:
                content = ''
                for line in file.readlines():
                    content = f"{content}{line}"
                return content
        return send_file(abs_path)

    # Show directory contents
    files = {os.path.join(abs_path, file_name): file_name for file_name in os.listdir(abs_path) if
             "storage" in os.path.join(abs_path, file_name)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('files.html', result=result)


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return str(e)


@app.route('/view_experiment_hist', methods=['GET', 'POST'])
def view_experiment_history():
    experiment_df = Pipeline.get_experiments_status()
    context = {
        "experiment": experiment_df.to_html(classes='table table-striped col-12')
    }
    return render_template('experiment_history.html', context=context)


@app.route('/train', methods=['GET', 'POST'])
def train():
    message = ""
    pipeline = Pipeline(config=Configration(current_time_stamp=CURRENT_TIME_STAMP))
    if not Pipeline.experiment.running_status:
        message = "Training started."
        pipeline.start()
    else:
        message = "Training is already in progress."
    context = {
        "experiment": pipeline.get_experiments_status().to_html(classes='table table-striped col-12'),
        "message": message
    }
    return render_template('train.html', context=context)

#Work in Progress...
@app.route('/predict', methods=['GET', 'POST'])
def predict():

    context = {
        BACKORDER_DATA_KEY: None,
        WENT_ON_BACKORDER_KEY: None
    }

    if request.method == 'POST':
        national_inv = float(request.form['National_Inv'])
        lead_time = float(request.form['Lead_time'])
        in_transit_qty = float(request.form['In_Transit_Qty'])
        forecast_3_m = float(request.form['Forecast_3_Month'])
        forecast_6_m = float(request.form['Forecast_6_Month'])
        forecast_9_m = float(request.form['Forecast_9_Month'])
        sales_1_m = float(request.form['Sales_1_Month'])
        sales_3_m = float(request.form['Sales_3_Month'])
        sales_6_m = float(request.form['Sales_6_Month'])
        sales_9_m = float(request.form['Sales_9_Month'])
        min_bank = float(request.form['Min_Bank'])
        pieces_past_due = float(request.form['Pieces_past_due'])
        Perf_6_Month_Avg = float(request.form['Perf_6_Month_Avg'])
        Perf_12_Month_Avg = float(request.form['Perf_12_Month_Avg'])
        Local_Bo_Qty = float(request.form['Local_Bo_Qty'])

        Potential_Issue = request.form['Potential_Issue']
        Deck_Risk = request.form['Deck_Risk']
        OE_Constraint = request.form['OE_Constraint']
        PPAP_Risk = request.form['PPAP_Risk']
        Stop_Auto_Buy = request.form['Stop_Auto_Buy']
        Rev_Stop = request.form['Rev_Stop']

        backorder_data = BackorderData(
                    national_inv=national_inv,
                    lead_time=lead_time,
                    in_transit_qty=in_transit_qty,
                    forecast_3_m=forecast_3_m,
                    forecast_6_m=forecast_6_m,
                    forecast_9_m=forecast_9_m,
                    sales_1_m=sales_1_m,
                    sales_3_m=sales_3_m,
                    sales_6_m=sales_6_m,
                    sales_9_m=sales_9_m,
                    min_bank=min_bank,
                    pieces_past_due=pieces_past_due,
                    Perf_6_Month_Avg=Perf_6_Month_Avg,
                    Perf_12_Month_Avg=Perf_12_Month_Avg,
                    Local_Bo_Qty=Local_Bo_Qty,
                    Potential_Issue=Potential_Issue,
                    Deck_Risk=Deck_Risk,
                    OE_Constraint=OE_Constraint,
                    PPAP_Risk=PPAP_Risk,
                    Stop_Auto_Buy=Stop_Auto_Buy,
                    Rev_Stop=Rev_Stop,
                                   )
                                   
        backorder_df = backorder_data.get_backorder_input_data_frame()
        predictor = BackOrderPredictor(model_dir=MODEL_DIR)
        went_on_backorder = predictor.predict(X=backorder_df)
        if went_on_backorder==0:
            went_on_backorder='No'
        else:
            went_on_backorder='Yes'
        context = {
            BACKORDER_DATA_KEY: backorder_data.get_backorder_data_as_dict(),
            WENT_ON_BACKORDER_KEY: went_on_backorder,
        }
        return render_template('predict.html', context=context)
    return render_template("predict.html", context=context)


@app.route('/saved_models', defaults={'req_path': 'saved_models'})
@app.route('/saved_models/<path:req_path>')
def saved_models_dir(req_path):
    os.makedirs("saved_models", exist_ok=True)
    # Joining the base and the requested path
    print(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('saved_models_files.html', result=result)


@app.route("/update_model_config", methods=['GET', 'POST'])
def update_model_config():
    try:
        if request.method == 'POST':
            model_config = request.form['new_model_config']
            model_config = model_config.replace("'", '"')
            print(model_config)
            model_config = json.loads(model_config)

            write_yaml_file(file_path=MODEL_CONFIG_FILE_PATH, data=model_config)

        model_config = read_yaml_file(file_path=MODEL_CONFIG_FILE_PATH)
        return render_template('update_model.html', result={"model_config": model_config})

    except  Exception as e:
        logging.exception(e)
        return str(e)


@app.route(f'/logs', defaults={'req_path': f'{LOG_FOLDER_NAME}'})
@app.route(f'/{LOG_FOLDER_NAME}/<path:req_path>')
def render_log_dir(req_path):
    os.makedirs(LOG_FOLDER_NAME, exist_ok=True)
    # Joining the base and the requested path
    logging.info(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        log_df = get_log_dataframe(abs_path)
        context = {"log": log_df.to_html(classes="table-striped", index=False)}
        return render_template('log.html', context=context)

    # Show directory contents
    files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('log_files.html', result=result)


if __name__ == "__main__":
    app.run(debug=True)
