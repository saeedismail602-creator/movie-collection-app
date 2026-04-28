# 🎬 Cinematic Movie Collection App

A premium, high-performance Flask web application designed for movie enthusiasts to curate, rate, and rank their all-time favorite films. Featuring a **Dark Cinematic UI**, this app provides a professional, "Netflix-style" experience for managing your personal movie library.

---

## 🚀 Features

- **Dark Cinematic UI:** A sleek, modern interface with a deep-space theme, radial gradients, and "Inter" typography.
- **Interactive Card-Flip:** Hover over any movie to reveal a 3D flip animation displaying detailed ratings, personal reviews, and plot overviews.
- **Dynamic Ranking:** Automatically re-ranks your collection in real-time based on your ratings—your #1 movie always takes the spotlight.
- **TMDB Integration:** Seamlessly search for and add movies using **The Movie Database (TMDB) API** for instant high-quality posters and metadata.
- **Responsive Grid:** A fluid, mobile-first layout that looks stunning on everything from smartphones to 4K monitors.
- **Full CRUD Support:** Add, update ratings/reviews, and delete movies with a professional, intuitive workflow.

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite with Flask-SQLAlchemy (ORM)
- **Frontend:** HTML5, CSS3 (Modern Grid/Flexbox), FontAwesome 5
- **Forms:** Flask-WTF (with CSRF protection)
- **UI Framework:** Bootstrap 5 (for base components & forms)
- **API:** TMDB (The Movie Database) API
- **Environment:** Dotenv for secure API key management

---

## 📸 Interface Preview

- **Index:** A responsive grid of cinematic posters with interactive hover states.
- **Search:** A streamlined interface for finding global blockbusters.
- **Manage:** Professional dark-themed forms for editing your personal critiques.

---

## 🛠️ Setup Instructions

1. **Clone the repository.**
2. **Install dependencies:**  
   `pip install -r requirements.txt`
3. **Configure Environment:**  
   Create a `.env` file and add your `MOVIE_DB_SEARCH_KEY_PASS` and `SECRET_KEY_PASS`.
4. **Run the App:**  
   `python main.py`

---
*Developed with ❤️ for movie lovers.*
