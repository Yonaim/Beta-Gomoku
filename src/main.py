from .agent import Agent
from .gamestate import GameState
from .ui.console_renderer import ConsoleRenderer

N_ITERATION = 1500
TIME_LIMIT = 3.5
PLAYER_1 = 1
PLAYER_2 = 2

def input_move() -> tuple[int, int]:
	while True:
		raw = input("당신의 차례입니다.\n좌표 (x, y)를 입력하세요: ").strip()
		try:
			x_s, y_s = raw.split()
			x, y = int(x_s), int(y_s)
			return x, y
		except Exception:
			print("유효한 형식으로 입력하세요. 예: 2 3\n")

def main():
	# 임시: player 우선 시작
	state = GameState(current_player=PLAYER_1)
	renderer = ConsoleRenderer()
	ai = Agent(player_id=PLAYER_2, time_limit=TIME_LIMIT, n_iteration=N_ITERATION)

	while not state.is_terminated():
		renderer.draw(state.board)

		if state.current_player == PLAYER_1:
			while True:
				try:
					move = input_move()
					state.apply_move(move)
					state.current_player = PLAYER_2
					break
				except ValueError:
					print("잘못된 수입니다. 재입력해주세요\n")
		else:
			move = ai.select_move(state)
			state.apply_move(move)
			print(f"AI의 수: {move}")

	if (state.get_winner() == PLAYER_1):
		print("당신의 승리입니다!")
	else:
		print("AI에게 패배했습니다.")

if __name__ == "__main__":
	main()