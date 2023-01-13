from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
from forms import upload_data, LoginUser, RegisterUser
from model import User, login_manager, bcrypt,db, login_user, current_user, logout_user, login_required, Predictions
from clicks_forecast import load_data, transform_data, train_model, predict, evaluate, check_reliablity, create_report
import pdfkit
from datetime import date

app = Flask(__name__)
app.config["SECRET_KEY"] = '12312'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
login_manager.init_app(app)
login_manager.login_message_category = "info"

bcrypt.init_app(app)
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegisterUser()
    if form.validate_on_submit() and not form.validate_username(form.username):
        user = User(username=form.username.data, password=form.password1.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("index"))
    if form.errors:
        for message in form.errors.values():
            flash(f"Ouch.. Error: {str(message)}", category='danger')
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginUser()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(attempted_pass=form.password.data):
            login_user(user)
            print("succes!")
            return redirect(url_for('index'))
        else:
            flash("Wrong credentials! Try again please.", category="danger")
    return render_template("login.html", form=form)

@app.route("/logout", methods=["GET","POST"])
def logout():
    logout_user()
    flash("You are now logged out!", category='success')
    return redirect(url_for("login"))



@app.route('/pdf/<prediction_id>', methods=['GET'])
def generate_pdf(prediction_id):
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    try:
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        result = Predictions.query.filter_by(id=prediction_id).first()
        res = render_template('pdf.html', result=result)
        response_string = pdfkit.from_string(res, configuration=config)
        response = make_response(response_string)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment;filename=prediction.pdf'
        return response
    except:
            flash("Site is not compatible with requirements",category="warning")
            return redirect(url_for('index'))

@app.route("/")
@app.route("/home",methods=["GET", "POST"])
@login_required
def index():
    df = load_data()
    form = upload_data()
    form.campaign_id.choices = [campaign for campaign in df.campaign_id.unique()]
    target_list = ["impressions","clicks"]
    form.target_col.choices = [target for target in target_list]
    if request.method == "POST" and form.validate_on_submit():
        if form.validate_user_id(form.prediction_name.data, current_user.id):
            session["campaign_id"] = form.campaign_id.data
            session["prediction_name"] = form.prediction_name.data
            session["target"] = form.target_col.data
            session["amount_spend"] = form.eu_to_spend.data
            return redirect(url_for('create_model'))
        else:
           flash("Prediction name already taken!", category='danger')
    if form.errors:
        for error in form.errors.values():
            flash(f"Ouch.. Error: {str(error)}", category='danger')
    return render_template("index.html", form=form, targets=target_list)

@app.route("/prediction", methods=["GET", "POST"])
@login_required
def create_model():
    df = load_data()
    campaign = session["campaign_id"]
    target = session["target"]
    amount_spend = session["amount_spend"]
    name = session["prediction_name"]
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

    if request.method == "POST":
        if request.form['submit-button'] == "Save":
            prediction = Predictions(prediction_name=name,prediction_value=result, prediction_campaign=campaign, predicted_column=target,
                                     coefficient=coef, intercept=intercept, date=date.today(),
                                     mae=evaluation_metrics[0], mse=evaluation_metrics[1], rmse=evaluation_metrics[2],
                                     r2=evaluation_metrics[3], correlation=evaluation_metrics[4])
            prediction.user_id = current_user.id
            db.session.add(prediction)
            db.session.commit()
            flash("Prediction saved!", category='success')
            return redirect(url_for("index"))
    reliable = check_reliablity(correlation=evaluation_dict["Correlation"], r_squared=evaluation_dict["R2 Score"])
    report = create_report(r2=evaluation_dict["R2 Score"], correlation=evaluation_dict["Correlation"], mae=evaluation_dict["Mean Absolute Error (MAE)"],
                           mse=evaluation_dict["Mean Squared Error (MSE)"])
    return render_template("prediction.html", result = result,
                           metrics={"Coefficient": float(coef),"Intercept": float(intercept)},
                           evaluation=evaluation_dict,
                           reliable=reliable,
                           report=report)

@app.route('/account', methods=["GET", "POST"])
@login_required
def account():
    user_predictions = Predictions.query.filter_by(user_id=current_user.id).all()
    return render_template('account.html', predictions=user_predictions)


if __name__ == "__main__":
    app.run(debug=True)
