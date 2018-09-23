import re
import collections

# class that represents a single basic block
class BasicBlock:
    def __init__(self, id_bb, entries, successors):
        self._id_bb = id_bb             # number of its leading instruction
        self._entries = entries         # list of all incoming basic blocks
        self._successors = successors   # list of all succeeding basic blocks
        self._in = set()
        self._out = set()
        self._kill = set()
        self._gen = set()
    
    def __str__(self):
        print("ID", self._id_bb) 
        print("entries = ", self._entries)
        print("successors = ", self._successors)
        print("OUT = ", self._out)
        print("IN = ", self._in)
        print("GEN = ", self._gen) 
        print("KILL = ", self._kill)
        print("----------------------------")
        print("----------------------------")

    # getters
    def get_id(self):
        return self._id_bb
    
    def get_entries(self):
        return self._entries
    
    def get_successors(self):
        return self._successors

    def get_in(self):
        return self._in
    
    def get_out(self):
        return self._out
    
    def get_kill(self):
        return self._kill
    
    def get_gen(self):
        return self._gen
    
    # setters
    def set_gen(self, element):
        self._gen |= element

    def set_kill(self, element):
        self._kill |= element

    def set_in(self, element):
        self._in |= element

    def set_out(self, element):
        self._out |= element
    
    __repr__ = __str__

def make_basic_blocks(tac_file):
    map_entries = make_entries(tac_file)
    map_successors = make_successors(tac_file)
    
    # make basic blocks
    basic_blocks = []
    for key, entries in map_entries.items():
        for key1, successors in map_successors.items():
            if key == key1:
                basic_blocks.append(BasicBlock(key, entries, successors))
    
    return basic_blocks

def make_entries(tac_file):
    # regex for matching instructions with goto
    regex = "^(?P<num>[0-9]+): (.)*goto [(](?P<goto_num>[0-9]+)[)]$";
    regex_goto = re.compile(regex)
    # dict for saving leader instruction and its entry branches
    # 1st instruction is a leader
    map_leaders = dict({1: []})
    
    with open(tac_file, "r") as file:
        for line in file:
            match = re.match(regex_goto, line.strip())
            if match is not None:
                goto_num = int(match.group("goto_num"))
                num = int(match.group("num"))
                
                # save entries for a leader
                if goto_num in map_leaders.keys():
                    map_leaders[goto_num].extend([num])
                else:
                    map_leaders[goto_num] = [num]
                # instruction after goto is a leader
                if num + 1 not in map_leaders.keys():
                    map_leaders[num + 1] = []
                 
    map_leaders = collections.OrderedDict(sorted(map_leaders.items()))
    leaders = list(map_leaders.items())
    
    for i in range(0, len(leaders)):
        key = leaders[i][0]
        # add rest of the entries
        if i != 0: 
            previous = leaders[i-1][0]
            map_leaders[key].append(previous)
        
        # add valid entries
        # if an element of an entry list is not a leader 
        # change it into leader of its basic block
        for index, e in enumerate(map_leaders[key]):
            if e not in map_leaders.keys():
                for l in range(1, len(leaders) + 1):
                    if e > leaders[l-1][0] and e < leaders[l][0]:
                        map_leaders[key].remove(e)
                        map_leaders[key].insert(index, leaders[l-1][0])
    return map_leaders

def make_successors(tac_file):
    # regex for matching instructions with goto
    regex = "^(?P<num>[0-9]+): (.)*goto [(](?P<goto_num>[0-9]+)[)]$";
    regex_goto = re.compile(regex)
    # dict for saving leader instruction and its succeeding branches
    # 1st instruction is a leader
    map_successors = dict({1: []})

    with open(tac_file, "r") as file:
        for line in file:
            match = re.match(regex_goto, line.strip())
            if match is not None:
                goto_num = int(match.group("goto_num"))
                num = int(match.group("num"))

                # successors for a basic block with goto
                map_successors[num] = [num + 1, goto_num]
                if goto_num not in map_successors.keys():
                    map_successors[goto_num] = []

                if num + 1 not in map_successors.keys():
                    map_successors[num + 1] = []
                 
    map_leaders = make_entries(tac_file)
    map_successors = collections.OrderedDict(sorted(map_successors.items()))

    map_valid_successors = dict({1: []})

    leaders = list(map_leaders.items())
    successors = list(map_successors.items())

    # make valid successors
    for i, s in enumerate(successors):
        leader_ids = []
        for l in leaders:
            leader_ids.append(l[0])
        if s[0] not in leader_ids:
            map_valid_successors[successors[i-1][0]] = s[1] 
        else:
            map_valid_successors[s[0]] = s[1]

    # if a list of successors is empty
    # add a successor which is the next basic block
    # in a list of basic blocks
    for x in map_valid_successors.items():
        if x[1] == []:
            for index, leader in enumerate(leaders):
                if leader[0] != x[0]:
                    pass
                else:
                    if index + 1 < len(map_leaders.keys()):
                        x[1].append(leaders[index + 1][0])

    return map_valid_successors

# erase block that generates nothing
# edge case when last instruction is goto
def erase_empty_block(blocks, n):
    if bool(blocks[n].get_gen()) == False:
        blocks[n - 1].get_successors().remove(blocks[n].get_id())
        blocks.pop()
    return blocks

# returns a map 
# key: number of an instruction
# value: (variable x, list of variables used for a definition of variable x) 
def make_definitions(tac_file):
        # a map / dict is used due to many search and insert operations
    definitions = dict()
    # regex for matching instructions with an assign operator 
    regex = "^(?P<num>[0-9]+): (?P<var_name>(\w+)|(\w+\[\w+\]))+ \s*:=\s*(?P<def>(.)+)$";
    regex_def = re.compile(regex)
    # needed for gen function
    num_lines = 0

    with open(tac_file, "r") as file:
        for line in file:
            num_lines += 1
            match = re.match(regex_def, line.strip())
            if match is not None:
                num = int(match.group("num"))
                var_name = match.group("var_name")
                definition = match.group("def")
                # find all variables in a definition
                definition = re.findall(r'(\w+\[\w+\])|([a-zA-Z]+[0-9]*)', definition.strip())
                # remove empty strings from findall match
                # by adding it to a string match
                # (findall returns a list of tuples containing a match and an empty string)
                definition = list(map(lambda x: x[0] + x[1], definition))
                definitions[num] = (var_name, definition)                
    return definitions, num_lines

# returns a map
# key x is a left side of the assignement
# value is a list of definitions of x 
def make_map(definitions):
    new_map = dict()
    for definition in definitions.items():
        key = definition[1][0]
        value = definition[0]
        if key in new_map:
            new_map[key].append(value)
        else:
            new_map[key] = [value]
    return new_map

def block_ids(blocks):
    list_blocks_id = []
    for block in blocks:
        list_blocks_id.append(block.get_id())
    return list_blocks_id

def binary_search(list_items, item):
    start = 0
    end = len(list_items) - 1
    
    while start <= end:
        middle = (start + end) // 2
        if item == list_items[middle]:
            return middle
        elif item < list_items[middle]:
            end = middle - 1
        else:
            start = middle + 1
    return -1

def get_line(tac_file, location):
    with open(tac_file, "r") as file:
        for i, line in enumerate(file):
            # location is counted from 1 and i from 0
            if i == location - 1:
                return line

def print_blocks(blocks):
    for i, b in enumerate(blocks):
        print("B" + str(i + 1))
        b.__str__()

def print_locations(file, location, locations):
    print("Definition ")
    print(str.rstrip(get_line(file, location)))
    if len(locations) == 0:
        print("is used nowhere.")
    elif len(locations) == 1:
        print("is used in definition:")
        print(str.rstrip(get_line(file, locations[0])))
    else:
        print("is used in definitions:")
        for location in locations:
            print(str.rstrip(get_line(file, location)))