import numpy as np

def load_data(filename):
    with open(filename, 'r') as f:
        content = f.read()
    # Unterstützt Komma- oder Zeilen-Trennung
    if ',' in content:
        data = np.array([float(x) for x in content.replace('\n', '').split(',') if x.strip()])
    else:
        data = np.array([float(x) for x in content.split() if x.strip()])
    return data

def normalize_data(data):
    min_val = np.min(data)
    shifted = data - min_val
    return shifted

def probabilities(shifted):
    total = np.sum(shifted)
    # Falls alle Werte 0 sind (z.B. identische Werte), Gleichverteilung
    if total == 0:
        return np.ones_like(shifted) / len(shifted)
    return shifted / total

def statistics(probs):
    indices = np.arange(len(probs))
    mean = np.sum(indices * probs)
    var = np.sum(((indices - mean) ** 2) * probs)
    std = np.sqrt(var)
    # Modus
    mode = int(np.argmax(probs))
    # Median
    cum_probs = np.cumsum(probs)
    median = int(np.where(cum_probs >= 0.5)[0][0])
    # Quartile
    q1 = int(np.where(cum_probs >= 0.25)[0][0])
    q3 = int(np.where(cum_probs >= 0.75)[0][0])
    return mean, var, std, mode, median, q1, q3

def ascii_histogram(probs, width=50):
    max_prob = np.max(probs)
    for idx, p in enumerate(probs):
        bar = '█' * int(p / max_prob * width)
        print(f"{idx:2d}: {p:.6f} | {bar}")

def main():
    filename = 'sim_strght_pref.txt'  # Passe den Dateinamen ggf. an
    data = load_data(filename)
    shifted = normalize_data(data)
    probs = probabilities(shifted)
    mean, var, std, mode, median, q1, q3 = statistics(probs)

    print("Statistische Kennzahlen:")
    print(f"Erwartungswert:       {mean:.2f}")
    print(f"Varianz:              {var:.2f}")
    print(f"Standardabweichung:   {std:.2f}")
    print(f"Modus:                {mode}")
    print(f"Median:               {median}")
    print(f"1. Quartil (Q1):      {q1}")
    print(f"3. Quartil (Q3):      {q3}\n")

    print("ASCII-Histogramm der Wahrscheinlichkeiten:")
    ascii_histogram(probs, width=50)

if __name__ == '__main__':
    main()
