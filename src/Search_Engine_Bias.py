import sqlite3
import requests
from bs4 import BeautifulSoup
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import ttk
import numpy as np



# Initialize SQLite database
def create_database():
    conn = sqlite3.connect('search_history.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS search_results (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        search_query TEXT,
                        google_results TEXT,
                        bing_results TEXT,
                        bias INTEGER,
                        search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    conn.commit()
    conn.close()


create_database()

# Google Custom Search API configuration
api_key = "YOUR_GOOGLE_API_KEY"
cx = "YOUR_SEARCH_ENGINE_ID"


# Function to fetch search results from Google
def google_search(query, api_key, cx, num_results=10):
    results = []
    start = 1

    while len(results) < num_results:
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cx}&start={start}"
        response = requests.get(url)
        response_json = response.json()
        items = response_json.get('items', [])
        results.extend([item['link'] for item in items])
        start += 10

        if not items or len(items) < 10:
            break  # No more results available

    return results[:num_results]


# Function to fetch search results from Bing
def bing_search(query, num_results=10):
    try:
        url = f'https://www.bing.com/search?q={query}'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for b in soup.find_all('li', class_='b_algo'):
            anchors = b.find_all('a')
            if anchors:
                link = anchors[0]['href']
                results.append(link)
                if len(results) >= num_results:
                    break  # Stop after collecting the desired number of results
        return results
    except Exception as e:
        print(f"Error in Bing search: {e}")
        return []


# Function to compare Google and Bing search results
def compare_results(results1, results2):
    common_results = set(results1).intersection(results2)
    return len(common_results), common_results


# Function to analyze bias in search results
def analyze_bias(results1, results2):
    common_count, common_links = compare_results(results1, results2)
    obs1 = len(results1) + 0.5
    obs2 = len(results2) + 0.5
    contingency_table = [[obs1, obs2], [obs1 - common_count, obs2 - common_count]]
    chi2, p, dof, expected = chi2_contingency(contingency_table)
    return chi2, p


# Function to perform Dixon Q test
def dixon_q_test(data, significance_level=0.05):
    n = len(data)
    if n < 3:
        return None, None  # Not enough data to perform the test

    data_sorted = sorted(data)
    q_statistic = (data_sorted[-1] - data_sorted[-2]) / (data_sorted[-1] - data_sorted[0])

    q_critical_values = {
        0.1: [0.941, 0.765, 0.642, 0.560, 0.507, 0.468, 0.437, 0.412, 0.392, 0.376, 0.361, 0.349, 0.338, 0.329, 0.320],
        0.05: [0.970, 0.829, 0.710, 0.625, 0.568, 0.526, 0.493, 0.466, 0.444, 0.426, 0.410, 0.396, 0.384, 0.374, 0.364],
        0.02: [0.994, 0.926, 0.821, 0.740, 0.680, 0.634, 0.598, 0.568, 0.544, 0.523, 0.507, 0.493, 0.480, 0.468, 0.457],
        0.01: [0.999, 0.970, 0.889, 0.829, 0.780, 0.741, 0.707, 0.679, 0.654, 0.634, 0.617, 0.601, 0.588, 0.575, 0.564]
    }

    if significance_level not in q_critical_values:
        raise ValueError("Significance level must be one of: 0.1, 0.05, 0.02, 0.01")

    q_critical = q_critical_values[significance_level][n - 3]

    return q_statistic, q_statistic > q_critical


# Function to analyze bias using Dixon Q test
def analyze_bias_with_dixon(results1, results2, significance_level=0.05):
    combined_results = results1 + results2
    num_results = [len(results1), len(results2)]

    q_statistic, is_outlier = dixon_q_test(num_results, significance_level)

    return q_statistic, is_outlier


# Function to visualize search result comparison
def visualize_results(google_results, bing_results):
    common_count, _ = compare_results(google_results, bing_results)
    labels = ['Google', 'Bing', 'Common']
    counts = [len(google_results), len(bing_results), common_count]

    plt.figure(figsize=(10, 6))
    sns.barplot(x=labels, y=counts)
    plt.title('Comparison of Search Results')
    plt.xlabel('Search Engine')
    plt.ylabel('Number of Results')
    plt.show()


# Function to handle search button click event
def on_search():
    query = entry1.get()
    global google_results, bing_results
    google_results = google_search(query, api_key, cx)
    bing_results = bing_search(query)

    google_result_text.delete(1.0, tk.END)
    bing_result_text.delete(1.0, tk.END)

    google_result_text.insert(tk.END, "\n".join(google_results))
    bing_result_text.insert(tk.END, "\n".join(bing_results))

    chi2, p_value = analyze_bias(google_results, bing_results)
    q_statistic, is_outlier = analyze_bias_with_dixon(google_results, bing_results)

    if q_statistic is None or is_outlier is None:
        result_text.set(
            f"Chi-square: {chi2:.2f}, p-value: {p_value:.2e}\nDixon Q: N/A, Outlier: N/A")
    else:
        result_text.set(
            f"Chi-square: {chi2:.2f}, p-value: {p_value:.2e}\nDixon Q: {q_statistic:.2f}, Outlier: {is_outlier}")

    bias = int(p_value < 0.05 or (is_outlier is not None and is_outlier))

    conn = sqlite3.connect('search_history.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO search_results (search_query, google_results, bing_results, bias) VALUES (?, ?, ?, ?)',
                   (query, "\n".join(google_results), "\n".join(bing_results), bias))
    conn.commit()
    conn.close()


# Function to handle bias analysis button click event
def on_bias_analysis():
    visualize_results(google_results, bing_results)


# Function to show search history
def show_history():
    history_window = tk.Toplevel(win1)
    history_window.title("Search History")
    history_window.geometry("700x580")

    frame = ttk.Frame(history_window, padding="10")
    frame.pack(expand=True, fill='both')

    tree = ttk.Treeview(frame, columns=("Query", "Google Results", "Bing Results", "Bias", "Date"), show='headings')
    tree.heading("Query", text="Query")
    tree.heading("Google Results", text="Google Results")
    tree.heading("Bing Results", text="Bing Results")
    tree.heading("Bias", text="Bias")
    tree.heading("Date", text="Date")

    conn = sqlite3.connect('search_history.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM search_results')
    records = cursor.fetchall()
    conn.close()

    for record in records:
        query, google_results, bing_results, bias, search_date = record[1], record[2], record[3], record[4], record[5]
        tree.insert("", tk.END, values=(query, google_results, bing_results, bias, search_date))

    tree.pack(expand=True, fill='both')

    #back_button = ttk.Button(frame, text="Back", command=history_window.destroy)
    #back_button.pack(pady=10)


# Function to handle comparison button click event

def calculate_statistics():
    conn = sqlite3.connect('search_history.db')
    cursor = conn.cursor()
    cursor.execute('SELECT google_results, bing_results FROM search_results')
    records = cursor.fetchall()
    conn.close()

    google_counts = []
    bing_counts = []

    for record in records:
        google_results = record[0].split('\n')
        bing_results = record[1].split('\n')
        google_counts.append(len(google_results))
        bing_counts.append(len(bing_results))

    return google_counts, bing_counts


def on_compare_results():
    google_counts, bing_counts = calculate_statistics()

    plt.figure(figsize=(10, 6))
    plt.hist(google_counts, bins=range(0, 61, 5), alpha=0.5, label='Google', color='b', density=True)
    plt.hist(bing_counts, bins=range(0, 61, 5), alpha=0.5, label='Bing', color='r', density=True)
    sns.kdeplot(google_counts, color='b', label='Google')
    sns.kdeplot(bing_counts, color='r', label='Bing')
    plt.axvline(np.mean(google_counts), color='b', linestyle='dashed', linewidth=1)
    plt.axvline(np.mean(bing_counts), color='r', linestyle='dashed', linewidth=1)

    google_var = np.var(google_counts)
    google_std = np.std(google_counts)
    bing_var = np.var(bing_counts)
    bing_std = np.std(bing_counts)

    plt.text(40, 0.25, f'Google STD: {google_std:.2f}\nGoogle VAR: {google_var:.2f}', color='blue')
    plt.text(40, 0.2, f'Bing STD: {bing_std:.2f}\nBing VAR: {bing_var:.2f}', color='red')

    plt.title('Distribution of Search Results')
    plt.xlabel('Number of Results')
    plt.ylabel('Density')
    plt.legend()
    plt.figtext(0.15, 0.8, f'Google STD: {google_std:.2f}', color='blue')
    plt.figtext(0.15, 0.75, f'Google VAR: {google_var:.2f}', color='blue')
    plt.figtext(0.15, 0.7, f'Bing STD: {bing_std:.2f}', color='red')
    plt.figtext(0.15, 0.65, f'Bing VAR: {bing_var:.2f}', color='red')
    plt.show()


# GUI setup
win1 = tk.Tk()
win1.title("Search Engine Comparison")
win1.geometry("530x580")
win1.resizable(False,False)
win1.configure(background='beige')
win1.iconphoto(True, tk.PhotoImage(file="D:\\Bachelor of Computer Engineering\\project1\\browser_icon.png"))



style = ttk.Style()
style.configure('TFrame', background='beige')
style.configure('TLabel', background='beige', foreground='black')
style.configure('TButton', background='white', foreground='black')
style.configure('TEntry', background='white', foreground='black')
style.configure('TText', background='white', foreground='black')
style.configure('TButton', background='white', foreground='black', borderwidth=1)
style.map('TButton',
          background=[('active', 'white')],
          foreground=[('active', 'black')])

frame1 = ttk.Frame(win1, padding="10")
frame1.grid(row=0, column=0, sticky="N")

label1 = ttk.Label(frame1, text="Enter your query:")
label1.grid(row=0, column=0, padx=5, pady=5)

entry1 = ttk.Entry(frame1, width=50)
entry1.grid(row=0, column=1, padx=5, pady=5)

button1 = ttk.Button(frame1, text="Search", command=on_search)
button1.grid(row=0, column=2, padx=5, pady=5)

result_text = tk.StringVar()
result_label = ttk.Label(frame1, textvariable=result_text)
result_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

google_result_label = ttk.Label(frame1, text="Google Results:")
google_result_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

google_result_text = tk.Text(frame1, height=10, width=50)
google_result_text.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

bing_result_label = ttk.Label(frame1, text="Bing Results:")
bing_result_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

bing_result_text = tk.Text(frame1, height=10, width=50)
bing_result_text.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

frame2 = ttk.Frame(win1)
frame2.grid(row=1, column=0, sticky="N")

bias_analysis_button = ttk.Button(frame2, text="Bias Analysis of Past Results", command=on_bias_analysis)
bias_analysis_button.grid(row=0, column=0, padx=10, pady=10)

comparison_button = ttk.Button(frame2, text="Comparison of Search Results", command=on_compare_results)
comparison_button.grid(row=0, column=1, padx=10, pady=10)

history_button = ttk.Button(frame2, text="Search History", command=show_history)
history_button.grid(row=0, column=2, padx=10, pady=10)


win1.mainloop()


