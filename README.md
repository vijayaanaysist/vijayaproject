# 💄 Cosmetic Offers Tracker & Auto Price Monitor

## 📌 Project Overview
This project is a Python-based price monitoring system that collects cosmetic product prices from multiple websites and compares offers automatically.

## 🎯 Objective
To help customers find the best cosmetic deals without manually checking different websites.

---

## 🚀 Features
- Scrapes product prices from:
  - Purplle
  - Nykaa
- Extracts:
  - Product Name
  - Original Price
  - Offer Price
  - Discount %
  - Website Name
- Cleans and transforms data using Pandas
- Stores data into CSV file
- Automatically runs every 10 minutes using Scheduler

---

## 🛠 Technologies Used
- Python
- requests
- BeautifulSoup
- pandas
- schedule

---

## 📂 Project Workflow

User Product → Scraper → Data Cleaning → Save to CSV → Automation

Website → Extract Price → Transform → Store → Auto Update

---

## 📊 Output File

cosmetic_offers.csv

Columns:
Product | Website | Original Price | Offer Price | Discount % | Date

---

## ⚙️ How to Run

1. Clone the repository: