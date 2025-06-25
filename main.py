from src.parser import HourlySalesCsvParser
from pathlib import Path

def main() -> None:
    parser = HourlySalesCsvParser()
    res = parser.parse(Path("sales_2025_06_01.csv"))
    for k, v in res.items():
        print(f"{k}: {v}")

if __name__ == '__main__':
    main()