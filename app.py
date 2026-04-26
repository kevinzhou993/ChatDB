from flask import Flask, render_template, request
from llm.llm_sql import generate_sql, validate_sql, execute_sql

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    question = ""
    sql_query = ""
    columns = []
    rows = []
    error = ""

    if request.method == "POST":
        question = request.form.get("question", "").strip()

        if question:
            try:
                sql_query = generate_sql(question)

                if not validate_sql(sql_query):
                    raise ValueError("Only SELECT queries are allowed.")

                columns, rows = execute_sql(sql_query)

            except Exception as e:
                error = str(e)

    return render_template(
        "index.html",
        question=question,
        sql_query=sql_query,
        columns=columns,
        rows=rows,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)