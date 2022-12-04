from flask import Flask, render_template, request, redirect, url_for, session, flash
from forms import upload_data
from clicks_forecast import load_data, transform_data, train_model, predict, evaluate, check_reliablity

app = Flask(__name__)

app.config["SECRET_KEY"] = '12312'

@app.route("/home",methods=["GET", "POST"])
def index():
    df = load_data()
    form = upload_data()
    form.campaign_id.choices = [campaign for campaign in df.campaign_id.unique()]
    target_list = ["impressions","clicks"]
    form.target_col.choices = [target for target in target_list]
    if request.method == "POST" and form.validate_on_submit():
        session["campaign_id"] = form.campaign_id.data
        session["target"] = form.target_col.data
        session["amount_spend"] = form.eu_to_spend.data
        return redirect(url_for('create_model'))
    if form.errors:
        for error in form.errors.values():
            flash(f"Ouch.. Error: {str(error)}", category='danger')
    return render_template("index.html", form=form, targets=target_list)

@app.route("/prediction", methods=["GET", "POST"])
def create_model():
    df = load_data()
    campaign = session["campaign_id"]
    target = session["target"]
    amount_spend = session["amount_spend"]

    coef, intercept = train_model(*transform_data(df=df,dependent=target, campaign=campaign))
    result = predict(slope=coef, interc=intercept, eu=amount_spend)

    evaluation_metrics = evaluate(df, coef, intercept, campaign, target)
    evaluation_dict = {
        "Mean Absolute Error (MAE)": evaluation_metrics[0],
        "Mean Squared Error (MSE)": evaluation_metrics[1],
        "Root Mean Squared Error (RMSE)": evaluation_metrics[2],
        "R2 Score": evaluation_metrics[3],
        "Correlation": evaluation_metrics[4]
    }
    reliable = check_reliablity(correlation=evaluation_dict["Correlation"], r_squared=evaluation_dict["R2 Score"])
    return render_template("prediction.html", result = result,
                           metrics={"Coefficient": float(coef),"Intercept": float(intercept)},
                           evaluation=evaluation_dict,
                           reliable=reliable)



if __name__ == "__main__":
    app.run(debug=True)
