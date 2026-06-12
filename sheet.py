import json
import os
from gsheet import insert_matrix

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Character:
    def __init__(self, file_path:str):
        self.file_path = file_path
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.ability = data.get('ability', None)
            self.adven_class = data.get('adven_class', None)
            self.age = int(data.get('age', 0))
            self.belief = data.get('belief', None)
            self.chr_name = data.get('chr_name', None)
            self.gender = data.get('gender', None)
            self.growth = data.get('growth', None)
            self.player = data.get('player', None)
            self.race = data.get('race', None)
            self.reputation_total = int(data.get('reputation_total', 0))
            self.reputation_used = int(data.get('reputation_used', 0))
            self.skills = data.get('skills', None)
            self.soulscar = int(data.get('soulscar', 0))
            self.total_abi = int(data.get('total_abi', 0))
            self.total_exp = int(data.get('total_exp', 0))
            self.used_exp = int(data.get('used_exp', 0))
            self.level = max(self.skills.values()) if self.skills else 0
    
    def __str__(self):
        return f"Lv.{self.level} {self.chr_name}\nPlayer: {self.player}"
    
    def to_csv_row(self):
        #chr_name, player, race, belief, age, gender, adv_class, level, used_exp
        return f"{self.chr_name},{self.player},{self.race},{self.belief},{self.age},{self.gender},{self.adven_class},{self.level},{self.used_exp}\n"
    
    def to_list(self):
        return [self.chr_name, self.player, self.race, self.belief, self.age, self.gender, self.adven_class, self.level, self.used_exp]

def import_chr_to_gsheet(chr_data_folder:str, sheet_name:str = 'chr', start_cell:str = 'B3'):
    chr_files = [f for f in os.listdir(chr_data_folder) if f.endswith('.json')]
    data_list = []
    for filename in chr_files:
        file_path = os.path.join(chr_data_folder, filename)
        chr = Character(file_path)
        data_list.append(chr.to_list())
    
    insert_matrix(sheet_name, start_cell, data_list)

if __name__ == "__main__":
    chr_data_folder = 'chr_data'
    import_chr_to_gsheet(chr_data_folder)