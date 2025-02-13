# Automate Gold Report

## Description
This project automates the generation of financial market reports using OANDA data for multiple trading instruments.
Access to an example report here: [Monthly Report (2022 Week 1)](output/report-2022-1.pdf)

## Features
- Automated data collection
- Report generation
- Data visualization

## Configuration
Update the `.env` file with your OANDA settings:
```bash
ACCESS_TOKEN=access_token
ACCOUNT_ID=account_id
```

## Example Usage & Results

Here's an example of the generated report visualizations:

![Gold Price Chart](figures/candlestick.png)

*Figure 1: Gold price movements over time with technical indicators*

![Temporal decomposition](figures/decomposition.png)

*Figure 2: Gold decomposition using trend, seasonal and residual*

These visualizations help track market trends and make informed trading decisions.

## License
MIT License

## Author
David Zhu
