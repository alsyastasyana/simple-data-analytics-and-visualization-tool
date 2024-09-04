from flask import Flask, request, render_template, flash, redirect
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/analyze', methods=['POST'])
def analyze_file():
    try:
        if 'file' not in request.files or request.files['file'].filename == '':
            flash('No file selected')
            return redirect('/')

        file = request.files['file']

        if not file.filename.endswith('.csv'):
            flash('Invalid file format. Please upload a CSV file.')
            return redirect('/')

        df = pd.read_csv(file)

        summary = df.describe().to_dict()

        # Display only the top 5 rows
        top_5_df = df.head(5)
        data_html = top_5_df.to_html(classes='table table-striped')

        # Example: Create a simple plot (e.g., histogram of the first numerical column)
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
        if not numeric_columns.empty:
            fig = px.histogram(df, x=numeric_columns[0], title=f'Histogram of {numeric_columns[0]}')
            plot_html = pio.to_html(fig, full_html=False)
        else:
            plot_html = None

        return render_template('result.html', tables=[data_html], summary=summary, plot_html=plot_html)

    except Exception as e:
        flash(f"An error occurred while processing the file: {str(e)}")
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
