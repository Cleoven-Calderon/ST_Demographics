

---

# National Indicators Dashboard

A **Streamlit** web app that visualizes key **economic and demographic indicators** for countries around the world using **World Bank API** data. This interactive dashboard allows users to explore trends in GDP, GDP per capita, inflation, population, life expectancy, and fertility rate over time.

Visit here ➡️ https://st-national-indicators-dashboard.streamlit.app/
---

## **Features**

* **Interactive country selection:** Pick any country from the World Bank database.
* **Real-time data:** Fetches the latest available data using the World Bank API.
* **Economic indicators:**

  * GDP (Billion USD)
  * GDP per capita (USD)
  * Inflation (Annual %)
* **Demographic indicators:**

  * Population (Million)
  * Life Expectancy (Years)
  * Fertility Rate (TFR)
* **Beautiful charts:**

  * Line charts for trends over time
  * Bar charts for totals
  * Area charts for visual emphasis
* **Responsive design:** Works well on different screen sizes.
* **Vibrant color gradients:** Economic indicators in red, demographic indicators in green.

---

## **Installation**

1. **Clone the repository**:

```bash
git clone <repository-url>
cd <repository-folder>
```

2. **Create a virtual environment (optional but recommended):**

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

---

## **Running the App**

```bash
streamlit run app.py
```

* The app will open in your default browser.
* Use the **sidebar** to select a country or refresh the data.

---

## **Dependencies**

* [Streamlit](https://streamlit.io/) – For building the dashboard
* [Pandas](https://pandas.pydata.org/) – For data manipulation
* [Requests](https://requests.readthedocs.io/) – To fetch data from the World Bank API
* [Altair](https://altair-viz.github.io/) – For interactive charts

You can install them via:

```bash
pip install streamlit pandas requests altair
```

---

## **Screenshots**
<img width="1913" height="1079" alt="Screenshot 2025-11-29 225539" src="https://github.com/user-attachments/assets/d55a27c0-921a-4f36-b3ec-597cf732bdd2" />

---

## **License**

This project is **open source** and free to use under the MIT License.

