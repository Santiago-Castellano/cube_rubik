from simpleai.search import (
    SearchProblem,
    astar
)

INITIAL = "V,V,V-B,B,B-R,R,R|Z,Z,Z-R,R,R-A,A,A|N,N,N-A,A,A-N,N,N|B,B,B-N,N,N-B,B,B|A,A,A-Z,Z,Z-Z,Z,Z|R,R,R-V,V,V-V,V,V"

GOAL = "R,R,R-R,R,R-R,R,R|A,A,A-A,A,A-A,A,A|V,V,V-V,V,V-V,V,V|Z,Z,Z-Z,Z,Z-Z,Z,Z|N,N,N-N,N,N-N,N,N|B,B,B-B,B,B-B,B,B"

ROTATIONS = [[0, 1, 2, 3], [4, 2, 5, 3]]

def convert_state_to_list(state):
    state_list = []
    for face in state.split('|'):
        new_face = [row.split(',') for row in face.split('-')]
        state_list.append(new_face)
    return state_list

def convert_state_to_str(state):
    state_str = ""
    for idx_face, face in enumerate(state):
        if idx_face != 0:
            state_str +="|"
        for idx_row, row in enumerate(face):
            if idx_row != 0:
                state_str += "-"
            for idx, piece in enumerate(row):
                if idx != 0:
                    state_str += ","
                state_str += piece

    return state_str

def rotate(state, axis, idx, direction):
    faces_to_rotate = ROTATIONS[axis][::direction]
    aux_faces = {}
    for face in faces_to_rotate:
        aux_faces[face] = state[face][idx]
    idx_actual_face = 0
    while idx_actual_face != 4:
        next_idx = idx_actual_face + 1
        if idx_actual_face == 3:
            next_idx = 0
        state[faces_to_rotate[idx_actual_face]][idx] = aux_faces[faces_to_rotate[next_idx]]
        idx_actual_face += 1

class Rubik(SearchProblem):
    def cost(self, state1, action, state2):
        return 1

    def is_goal(self, state):
        return state == GOAL

    def actions(self, state):
        available_actions = []
        for rotate in [0, 1]:
            for idx in range(3):
                for direction in [1, -1]:
                    available_actions.append((rotate, idx, direction))

        return available_actions

    def result(self, state, action):
        axis, idx, direction = action
        list_state = convert_state_to_list(state)
        rotate(list_state, axis, idx, direction)

        return convert_state_to_str(list_state)

    def heuristic(self, state):
        correct_position = 0
        list_state = convert_state_to_list(state)
        goal_list = convert_state_to_list(GOAL)
        for idx_face, face in enumerate(list_state):
            for idx_row, row in enumerate(face):
                for idx, piece in enumerate(row):
                    if piece == goal_list[idx_face][idx_row][idx]:
                        correct_position += 1
        
        return -correct_position

if __name__=="__main__":
    problem = Rubik(INITIAL)

    result = astar(problem, graph_search=True)

    print("Goal node:", result)
    if result:
        print("Path from initial to goal:")
        for action, state in result.path():
            print("Action:", action)
            print("State:", state)