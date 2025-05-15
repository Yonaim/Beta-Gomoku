from .agent import Agent
from .gamestate import GameState
from .ui.console_renderer import ConsoleRenderer
from .settings import TIME_LIMIT, N_ITERATION

PLAYER_1 = 1
PLAYER_2 = 2

def input_move() -> tuple[int, int]:
	while True:
		raw = input("좌표 (x, y)를 입력하세요: ").strip()
		try:
			x_s, y_s = raw.split()
			x, y = int(x_s), int(y_s)
			return y, x
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
			print("당신의 차례입니다.")
			while True:
				try:
					move = input_move()
					state.apply_move(move)
					state.current_player = PLAYER_2
					break
				except ValueError:
					print("잘못된 수입니다. 재입력해주세요\n")
		else:
			print("AI의 차례입니다.")
			print("AI가 다음 수를 생각 중입니다...")
			move = ai.select_move(state)
			state.apply_move(move)
			print(f"AI의 수: ({move[0]}, {move[1]})\n")
			state.current_player = PLAYER_1

	renderer.draw(state.board)

	if (state.get_winner() == PLAYER_1):
		print("당신의 승리입니다!")
	else:
		print("AI에게 패배했습니다.")

if __name__ == "__main__":
	main()