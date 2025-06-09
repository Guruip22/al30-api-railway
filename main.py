import os
from flask import Flask, jsonify
from pyhomebroker import HomeBroker

app = Flask(__name__)

@app.route("/api/al30")
def get_al30():
    try:
        hb = HomeBroker(265)
        hb.auth.login(
            dni=os.getenv("DNI"),
            user=os.getenv("HB_USER"),
            password=os.getenv("HB_PASS"),
            raise_exception=True
        )
        quotes = hb.quotes.realtime.tickers(['AL30'])
        al30_data = quotes.loc['AL30']
        return jsonify({
            "contado_inmediato": al30_data['last_price'],
            "contado_24hs": al30_data['previous_price']
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8080))
    )
