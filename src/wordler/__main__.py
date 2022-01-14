from datetime import date

from wordler.constants import PUZZLE_SIZE
from wordler.solver import solve_daily

result = solve_daily(size=PUZZLE_SIZE)

header = f"Daily size {PUZZLE_SIZE} for {date.today().isoformat()}"

print(header)
for row in result.emojis:
    print(row)
print()
print("----")
print()
print(header)
for emojis, guess in zip(result.emojis, result.guesses):
    print(f"{emojis} ({guess})")
