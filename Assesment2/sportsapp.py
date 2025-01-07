import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO

API_KEY = "3"  
BASE_URL = "https://www.thesportsdb.com/api/v1/json/" + API_KEY + "/"


class SportsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sports App")
        self.geometry("1000x700")
        self.pages = {}
        self.create_pages()

    def create_pages(self):
        # Create a custom style for the Notebook
        style = ttk.Style(self)
        style.theme_create('CustomTheme', parent='alt', settings={
            "TNotebook": {
                "configure": {
                    "tabmargins": [2, 5, 2, 0],
                    "background": "#123456",  # Background of the navigation bar
                }
            },
            "TNotebook.Tab": {
                "configure": {
                    "padding": [10, 5],
                    "background": "#456789",  # Background of the tabs
                    "foreground": "white",   # Text color of the tabs
                },
                "map": {
                    "background": [("selected", "#1E90FF")],  # Active tab color
                    "foreground": [("selected", "white")],    # Active tab text color
                }
            }
        })
        style.theme_use('CustomTheme')

        container = ttk.Notebook(self)

        # Create pages
        self.pages["Welcome"] = WelcomePage(container)
        self.pages["AboutSports"] = AboutSports(container)
        self.pages["PlayerSearch"] = PlayerSearch(container)
        self.pages["TeamInfo"] = TeamInfo(container)
        self.pages["HeadToHeadComparison"] = HeadToHeadComparison(container)

        # Add pages to container in the desired order
        container.add(self.pages["Welcome"], text="Welcome")
        container.add(self.pages["AboutSports"], text="About the Sports")
        container.add(self.pages["PlayerSearch"], text="Player Search")
        container.add(self.pages["TeamInfo"], text="Team Info")
        container.add(self.pages["HeadToHeadComparison"], text="Head-to-Head Comparison")

        container.pack(expand=1, fill="both")


def add_background_image(frame, image_path):
    """Adds a background image to the given frame."""
    def resize_bg(event):
        img = Image.open(image_path)
        img = img.resize((event.width, event.height))  # Resize image to fit frame size
        bg_image = ImageTk.PhotoImage(img)
        background_label.config(image=bg_image)
        background_label.image = bg_image  # Keep reference to the image

    background_label = tk.Label(frame)
    background_label.place(relwidth=1, relheight=1)  # Stretch the label to cover the whole frame
    frame.bind("<Configure>", resize_bg)  # Bind resize event to update the background image


class WelcomePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        # Add background image
        add_background_image(self, "cover.jpeg")  

        # Heading
        tk.Label(self, text="WELCOME TO FUTBALL", font=("Arial", 24, "bold"), fg="#040f36").pack(pady=60)

        # Body Text
        tk.Label(
            self,
            text="Choose any navigation bar and do your research.",
            font=("Arial", 16), 
            wraplength=700,
            justify="center",
            fg="#040f36"
        ).pack(pady=10)


class AboutSports(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        # Add background image
        add_background_image(self, "ten.jpeg") 

        tk.Label(self, text="About the Sports", font=("Arial", 16)).pack(pady=10)

        # Change button color
        tk.Button(self, text="Fetch Information", command=self.fetch_sports_info, bg="#4CAF50", fg="white").pack(pady=10)
        
        self.result = tk.Text(self, height=25, width=100)
        self.result.pack()

    def fetch_sports_info(self):
        url = f"{BASE_URL}all_sports.php"
        response = requests.get(url)
        data = response.json()

        self.result.delete(1.0, tk.END)
        if data and "sports" in data:
            for sport in data["sports"]:
                details = f"Sport: {sport['strSport']} - Description: {sport['strSportDescription']}\n\n"
                self.result.insert(tk.END, details)
        else:
            self.result.insert(tk.END, "No sports found!")


class PlayerSearch(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        # Add background image
        add_background_image(self, "ten.jpeg")  

        tk.Label(self, text="Player Search", font=("Arial", 16)).pack(pady=10)

        self.player_name = tk.StringVar()
        tk.Entry(self, textvariable=self.player_name, width=30).pack(pady=5)

        # Change button color
        tk.Button(self, text="Search Player", command=self.search_player, bg="#4CAF50", fg="white").pack(pady=10)
        
        self.result_frame = tk.Frame(self)
        self.result_frame.pack()

    def search_player(self):
        player_name = self.player_name.get()
        if not player_name:
            messagebox.showerror("Error", "Please enter a player name!")
            return

        url = f"{BASE_URL}searchplayers.php?p={player_name}"
        response = requests.get(url)
        data = response.json()

        for widget in self.result_frame.winfo_children():
            widget.destroy()

        if data and "player" in data:
            for player in data["player"]:
                details = f"Name: {player['strPlayer']} - Team: {player['strTeam']} - Position: {player['strPosition']}\n"
                tk.Label(self.result_frame, text=details).pack()
                player_image_url = player.get('strThumb', None)
                if player_image_url:
                    self.display_player_image(player_image_url)
        else:
            tk.Label(self.result_frame, text="No player found!").pack()

    def display_player_image(self, image_url):
        try:
            response = requests.get(image_url)
            image_data = response.content
            image = Image.open(BytesIO(image_data))
            image = image.resize((250, 250))
            img_tk = ImageTk.PhotoImage(image)
            label = tk.Label(self.result_frame, image=img_tk)
            label.image = img_tk
            label.pack(side=tk.LEFT, padx=70)
        except Exception as e:
            print(f"Error fetching image: {e}")


class TeamInfo(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        # Add background image
        add_background_image(self, "ten.jpeg")  

        tk.Label(self, text="Team Information", font=("Arial", 16)).pack(pady=10)

        self.team_name = tk.StringVar()
        tk.Entry(self, textvariable=self.team_name, width=30).pack(pady=5)

        # Change button color
        tk.Button(self, text="Search Team", command=self.search_team, bg="#4CAF50", fg="white").pack(pady=10)

        self.result = tk.Text(self, height=25, width=100)
        self.result.pack()

    def search_team(self):
        team_name = self.team_name.get()
        if not team_name:
            messagebox.showerror("Error", "Please enter a team name!")
            return

        url = f"{BASE_URL}searchteams.php?t={team_name}"
        response = requests.get(url)
        data = response.json()

        self.result.delete(1.0, tk.END)
        if data and "teams" in data:
            for team in data["teams"]:
                details = f"Team: {team['strTeam']} - Formed Year: {team['intFormedYear']} - Stadium: {team['strStadium']}\nDescription: {team['strDescriptionEN']}\n\n"
                self.result.insert(tk.END, details)
        else:
            self.result.insert(tk.END, "No team found!")


class HeadToHeadComparison(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        # Add background image
        add_background_image(self, "ten.jpeg")  

        tk.Label(self, text="Head-to-Head Comparison", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Team 1:").pack(pady=5)
        self.team1_name = tk.StringVar()
        tk.Entry(self, textvariable=self.team1_name, width=30).pack(pady=5)

        tk.Label(self, text="Team 2:").pack(pady=5)
        self.team2_name = tk.StringVar()
        tk.Entry(self, textvariable=self.team2_name, width=30).pack(pady=5)

        # Change button color
        tk.Button(self, text="Compare Teams", command=self.compare_teams, bg="#4CAF50", fg="white").pack(pady=10)

        result_frame = tk.Frame(self)
        result_frame.pack(fill="both", expand=True)

        self.result = tk.Text(result_frame, height=25, width=100)
        self.result.pack(side=tk.LEFT, fill="both", expand=True)

        scrollbar = tk.Scrollbar(result_frame, command=self.result.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        self.result.config(yscrollcommand=scrollbar.set)

    def compare_teams(self):
        team1 = self.team1_name.get()
        team2 = self.team2_name.get()

        if not team1 or not team2:
            messagebox.showerror("Error", "Please enter both team names!")
            return

        self.result.delete(1.0, tk.END)

        team1_data = self.fetch_team_data(team1)
        if team1_data:
            self.result.insert(tk.END, f"=== {team1.upper()} ===\n")
            self.result.insert(tk.END, self.format_team_data(team1_data))
        else:
            self.result.insert(tk.END, f"No data found for {team1}.\n")

        team2_data = self.fetch_team_data(team2)
        if team2_data:
            self.result.insert(tk.END, f"\n=== {team2.upper()} ===\n")
            self.result.insert(tk.END, self.format_team_data(team2_data))
        else:
            self.result.insert(tk.END, f"No data found for {team2}.\n")

        self.result.insert(tk.END, "\n=== All Past Matches ===\n")
        all_matches_data = self.fetch_all_matches(team1, team2)
        if all_matches_data:
            for match in all_matches_data:
                match_info = f"{match['dateEvent']} - {match['strEvent']} - Score: {match['intHomeScore']}:{match['intAwayScore']}\n"
                self.result.insert(tk.END, match_info)
        else:
            self.result.insert(tk.END, "No past matches found.\n")

    def fetch_team_data(self, team_name):
        url = f"{BASE_URL}searchteams.php?t={team_name}"
        response = requests.get(url)
        data = response.json()
        if data and "teams" in data:
            return data["teams"][0]
        return None

    def format_team_data(self, team_data):
        details = (
            f"Team: {team_data['strTeam']}\n"
            f"Formed Year: {team_data['intFormedYear']}\n"
            f"Stadium: {team_data['strStadium']}\n"
            f"Description: {team_data['strDescriptionEN']}\n"
        )
        return details

    def fetch_all_matches(self, team1, team2):
        url = f"{BASE_URL}searchallteams.php?t1={team1}&t2={team2}"
        response = requests.get(url)
        data = response.json()
        if data and "matches" in data:
            return data["matches"]
        return None


if __name__ == "__main__":
    app = SportsApp()
    app.mainloop()
