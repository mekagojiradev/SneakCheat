
class Player:
    def __init__(self, name: str, score: int) -> None:
        self.name = name
        self.score = score
        
    def __lt__(self, other) -> bool:
        if isinstance(other, Player):
            return self.score < other.score
        if isinstance(other, int):
            return self.score < other
        return False
    
    def __eq__(self,other) -> bool:
        if isinstance(other, Player):
            return self.score == other.score and self.name == other.name
        if isinstance(other, int):
            return self.score == other
        return False

    def __str__(self) -> str:
        return f'{self.name:<15}{self.score:<10}'

            
             