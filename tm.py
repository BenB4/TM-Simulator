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
        return self.transition_rules[reading_symbol]

    def set_final(self, isFinal):
        self.final = isFinal

    def set_start(self, isStart):
        self.start = isStart

    def is_final(self):
        return self.final

class _Tape_Segment:
    def __init__(self, val='_', next=None, prev=None):
        self.value = val
        self.next = next
        self.prev = prev

class Tape:
    def __init__(self, initial_tape=[]):
        self.start = None
        self.curr = None
        if initial_tape:
            self.start = _Tape_Segment(initial_tape[0])
            self.curr = self.start
            if initial_tape[1:]:
                for v in initial_tape[1:]:
                    next = _Tape_Segment(v, None, self.curr)
                    self.curr.next = next
                    self.curr = next
                self.curr = self.start

    def write(self, direction, write_val):
        self.curr.value = write_val
        if direction == 'R':
            if not self.curr.next:
                self.curr.next = _Tape_Segment('_', None, self.curr)
            self.curr = self.curr.next
        else:
            if not self.curr.prev:
                self.curr.prev =_Tape_Segment('_', self.curr, None)
            self.curr = self.curr.prev

    def read(self):
        return self.curr.value
    

class TM:
    def __init__(self, tm_file_name='tm.txt') -> None:
        self.new(tm_file_name)

    #creates a new NFA as specified by input NFA file.
    def new(self, tm_file_name='tm.txt'):
        self.states = {}
        self.alphabet = set()
        self.tape_alphabet = set()
        self.start = None
        self.accept = None
        self.reject = None
        self.accepts = False
        self.tape = Tape()
        with open(tm_file_name) as tm_file:
            #read states
            state_name_list = tm_file.readline().rstrip().split(',')
            for state_name in state_name_list: 
                self.states[state_name] = State(state_name)
                if state_name == 'accept': self.accept = self.states[state_name]
                if state_name == 'reject': self.reject = self.states[state_name]
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
                self.states[rule[0]].add_rule(rule[1], (rule[2], self.states[rule[3]], rule[4]))
                line = tm_file.readline()
            tm_file.close()

    #simulates TM
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
        if current == self.accept: 
            self.accepts = True
            return
        elif current == self.reject:
            self.rejects =True
            return
        if self.tape.read() not in current.transition_rules:
            self.rejects = True
            return
        next = current.read_symbol(self.tape.read())
        self.tape.write(next[2], next[0])
        self.simulate(next[1])


def main():
    test_TM = TM()
    test_TM.run()


if __name__ == '__main__':
    main()

