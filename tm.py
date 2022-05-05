class State:
    def __init__(self, name) -> None:
        self.name = name
        self.start = False
        self.final = False
        self.transition_rules = dict()

    #maps a state to a given symbol
    def add_rule(self, reading_symbol, destination_state):
        self.transition_rules[reading_symbol] = destination_state

    def read_symbol(self, reading_symbol):
        print(self.transition_rules)
        return self.transition_rules[reading_symbol]

    def set_final(self, isFinal):
        self.final = isFinal

    def set_start(self, isStart):
        self.start = isStart

    def is_final(self):
        return self.final


class Tape:
    def __init__(self, initial_tape=[]):
        self.tape = initial_tape if initial_tape else []
        self.rw_head = 0

    def write(self, direction, write_val):
        self.tape[self.rw_head] = write_val if self.rw_head < len(self.tape) else self.tape.append(self.rw_head)
        if direction == 'R':
            self.rw_head += 1 
        else:
             self.rw_head -= 1

    def read(self):
        return self.tape[self.rw_head] if self.rw_head < len(self.tape) else '_'
    

class TM:
    def __init__(self) -> None:
        self.states = {}
        self.alphabet = set()
        self.start = None
        self.accepts = False
        self.new()
        self.tape = Tape()

    #creates a new NFA as specified by input NFA file.
    def new(self, tm_file_name='tm.txt'):
        self.states = {}
        self.alphabet = set()
        self.tape_alphabet = set()
        self.start = None
        self.accept = None
        self.reject = None
        self.accepts = False
        self.rejects = False
        with open(tm_file_name) as tm_file:
            #read states
            state_name_list = tm_file.readline().rstrip().split(',')
            for state_name in state_name_list: 
                self.states[state_name] = State(state_name)
                self.accept = state_name if state_name == 'accept' else None
                self.reject = state_name if state_name == 'reject' else None
            #read alphabet
            letters = tm_file.readline().rstrip().split(',')
            for l in letters: self.alphabet.add(l)
            #tape alphabet
            letters = tm_file.readline().rstrip().split(',')
            for l in letters: self.tape_alphabet.add(l)
            #set start state
            start_state = tm_file.readline().rstrip()
            self.states[start_state].set_start(True)
            self.start = self.states[start_state]
            #add rules
            line = tm_file.readline()
            while line:
                rule = line.rstrip().split(',')
                print(rule, rule[0])
                self.states[rule[0]].add_rule(rule[1], (rule[2], self.states[rule[3]], rule[4]))
                line = tm_file.readline()
            tm_file.close()

    #simulates NFA for every string in input file and writes results to output file.
    def run(self, input_file_name='input.txt', output_file_name='output.txt'):
        #clear output file
        with open(output_file_name, 'w') as out:
                    out.truncate(0)
                    out.close()
        #read input file, follow transition rules for each string in file and write result to output.
        with open(input_file_name) as input_file:
            with open(output_file_name, 'w') as out:
                for string in input_file:
                    self.accepts = False
                    #sim function
                    self.tape = Tape([c for c in string.rstrip()])
                    self.simulate(self.start)
                    if self.accepts:
                        out.write('accept\n')
                    else:
                        out.write('reject\n')
                out.close()
            input_file.close()

    def simulate(self, current):
        #kills path if no transition rule for previous symbol or path is @ cycle.
        if current == self.accept: 
            self.accepts = True
            return
        elif current == self.reject:
            self.rejects =True
            return

        #if input string not empty read leading character and check if any path from it is valid
        next = current.read_symbol(self.tape.read())
        print(current.name)
        print(self.tape.read())
        self.tape.write(next[2], next[0])
        self.simulate(next[1])




def main():
    test_TM = TM()
    test_TM.run()


if __name__ == '__main__':
    main()

