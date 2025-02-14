import argparse

import data_loader
import plot

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib import colors

from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt
from io import BytesIO

# Set locale for time-related functions to English (United States)
import locale
locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')

from scipy.stats import kurtosis, skew

import datetime

def get_statistics(df):
    # Calcul des statistiques sur les prix de clôture
    prix_cloture   = df["Close"]
    moyenne        = prix_cloture.mean()
    variance       = prix_cloture.var()
    ecart_type     = prix_cloture.std()
    asymetrie      = skew(prix_cloture)
    kurtosis_exces = kurtosis(prix_cloture)  # Kurtosis en excès (0 pour une distribution normale)
    return moyenne, variance, ecart_type, asymetrie, kurtosis_exces

styles = getSampleStyleSheet()
def get_h2(text):
    return Paragraph(text, style=styles["h2"])

def get_normal(text):
    return Paragraph(text, style=styles["Normal"])

def get_title(text):
    return Paragraph(text, style=styles["Title"])

def get_table(data):
    # example data 
    # data = [
    # ["Date", "Price", "Volume"],
    # ["2025-03-01", "$1850", "5000"],
    # ["2025-03-02", "$1860", "4800"],
    # ["2025-03-03", "$1845", "5200"],
    # ["2025-03-04", "$1870", "5100"],
    # ["2025-03-05", "$1865", "4950"],
    # ]

    # --- Create the Table ---
    table = Table(data)

    # --- Style the Table ---
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),    # Header background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),     # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),                 # Center all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),       # Bold font for header
        ('FONTSIZE', (0, 0), (-1, 0), 12),                     # Font size for header
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),                 # Padding for header
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),        # Background for data cells
        ('GRID', (0, 0), (-1, -1), 1, colors.black),           # Grid lines
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),       # Bold font for first column
    ])

    table.setStyle(table_style)

    return table

def week_to_unix(year, week):
    """
    Given a year and an ISO week number, returns a tuple with:
      - Unix timestamp for the start of the week (Monday at 00:00:00)
      - Unix timestamp for the end of the week (Sunday at 23:59:59)
    """
    # Get the Monday and Sunday of the given week using ISO calendar
    monday = datetime.date.fromisocalendar(year, week, 1)
    sunday = datetime.date.fromisocalendar(year, week, 7)
    # print(monday)
    # print(sunday)

    # Create datetime objects for the beginning and end of the week
    monday_dt = datetime.datetime.combine(monday, datetime.time(0, 0, 0), tzinfo=datetime.timezone.utc)
    # Use a specific time for Sunday: 23:59:59 (avoids fractional seconds)
    sunday_dt = datetime.datetime.combine(sunday, datetime.time(0, 0, 0), tzinfo=datetime.timezone.utc)
    
    # Convert the datetime objects to Unix timestamps (seconds since 1970-01-01)
    monday_unix = int(monday_dt.timestamp())
    sunday_unix = int(sunday_dt.timestamp())

    # print(monday_unix)
    # print(sunday_unix)
    
    return monday_unix, sunday_unix

def generate_pdf(year, week):

    monday_unix, sunday_unix = week_to_unix(year, week)

    print("Downloading data...")
    df = data_loader.get_df("XAU_USD", "H1", start_unix=monday_unix, end_unix=sunday_unix)

    print("Plotting candlestick chart...")
    plot.plot_candlestick(df, "figures/candlestick.png")

    print("Plotting decomposition chart...")
    plot.plot_decomposition(df["Close"], "figures/decomposition.png")

    print("Generating PDF...")
    file_name = f"output/report-{year}-{week}.pdf"
    # Création du document avec des marges définies
    doc = SimpleDocTemplate(file_name, pagesize=letter,
                            rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)

    # Récupération des styles de base
    story = []

    # --- Ajout du titre ---
    story.append(get_title(f"Gold Analysis - Week {week} - {year}")) # TODO changer le titre 
    story.append(Spacer(1, 24))  # Espace après le titre

    # --- Introduction des statistiques ---
    story.append(get_h2("Period Analysis"))
    story.append(get_normal(f"Start Date : {df.index[0].strftime('%A, %B %d, %Y')}"))
    story.append(get_normal(f"End Date   : {df.index[-1].strftime('%A, %B %d, %Y')}"))
    story.append(get_normal(f"Number of candles : {len(df)}"))
    # story.append(get_normal("News : ...")) # TODO rajouter les news

    # --- Insertion du graphique dans le PDF ---
    story.append(get_h2("Price Charts"))
    img = Image('figures/candlestick.png', width=400, height=300) 
    story.append(img)
    story.append(Spacer(1, 12))

    # --- Weekly statistics ---
    moyenne, variance, ecart_type, asymetrie, kurtosis_exces = get_statistics(df)
    data = [
        ["Stat", "Value"],
        ["Mean Close Price", f"{moyenne:.2f} CAD"],
        # ["Variance", f"{variance:.4f}"],
        ["Standard Deviation", f"{ecart_type:.2f} CAD"],
        ["Skewness", f"{asymetrie:.2f}"],
        ["Kurtosis", f"{kurtosis_exces:.2f}"],
    ]
    story.append(get_h2("Weekly Statistics"))
    story.append(get_table(data))

    # --- PageBreak ---
    story.append(PageBreak())

    # --- Insertion du graphique dans le PDF ---
    story.append(get_h2("Time Series Decomposition"))
    img = Image('figures/decomposition.png', width=400, height=300)  # Vous pouvez ajuster la taille selon vos besoins
    # img = Image(buffer, width=400, height=300)  # Vous pouvez ajuster la taille selon vos besoins
    story.append(img)
    story.append(Spacer(1, 12))

    # --- Construction du PDF ---
    doc.build(story)
    print(f"Le PDF '{file_name}.pdf' a été créé avec le titre, du texte et une image incorporée.")

if __name__ == "__main__":
    # using args to get year and week
    # parser 
    parser = argparse.ArgumentParser()
    # add argument first is year 
    parser.add_argument("year", help="year of the week")
    # add argument second is week
    parser.add_argument("week", help="week number")

    # parse the arguments
    args = parser.parse_args()
    # call the function
    generate_pdf(int(args.year), int(args.week))