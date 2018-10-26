from copy import deepcopy
import argparse

import yacc
import parser
import basic_block as bb

# gen for all basic blocks
def gen(blocks, list_ids, definitions):
    num_bb = len(blocks)
    d = 0
    for i in range(0, num_bb - 1):
        next_leader = list_ids[i+1]
        defs = []
        while d < len(definitions) and definitions[d] < next_leader:
            defs.append(definitions[d])
            d += 1
        blocks[i].set_gen(set(defs)) 
    # gen for the last basic block
    if d < len(definitions):
        blocks[num_bb-1].set_gen(set(definitions[d:]))

# kill for all basic blocks
def kill(blocks, definitions, var_def):
    for block in blocks:
        for gen in block.get_gen():
            if gen in definitions.keys():
                var = definitions[gen][0]
                block.set_kill(set(var_def[var]))

# in for a given index of a basic block
def in_set(blocks, list_ids, i):       
        for entry in blocks[i].get_entries():
            index = bb.binary_search(list_ids, entry)
            blocks[i].set_in(set(blocks[index].get_out()))
       
def algorithm(list_ids, blocks):
    w = deepcopy(list_ids)

    while w:
        w = sorted(w)
        block_id = w.pop(0)
        i = bb.binary_search(list_ids, block_id)

        in_set(blocks, list_ids, i)
        block_out = deepcopy(blocks[i].get_out())
        blocks[i].set_out(blocks[i].get_gen() | (blocks[i].get_in() - blocks[i].get_kill()))

        if block_out != blocks[i].get_out():
            for s in blocks[i].get_successors():
                if s != block_id:
                    w.append(s)

def get_definitions(num_lines, blocks_ids, definitions, var_def, return_goto, blocks, location):
    locations = []
    next_leader = 0
    len_blocks = len(blocks_ids)

    # find variable - left side of location
    for d in definitions.items():
        if d[0] == location:
            var = d[1][0]
    
    for i, block in enumerate(blocks):
        if i + 1 < len_blocks:
                next_leader = blocks[i+1].get_id()
        else:
            next_leader = num_lines + 1  # +1 because of range()

        if location in block.get_out():
            for gen in range(block.get_id(), next_leader):
                if gen > location:
                    for d in definitions.items():
                        if gen == d[0]:
                            if var in d[1][1]:
                                locations.append(d[0])
                    for rg in return_goto.items():
                        if gen == rg[0]:
                            if var in rg[1]:
                                locations.append(rg[0])
        elif location in block.get_kill():
            stop_def = -1
            for def_var in var_def[var]:
                if def_var >= location and def_var in block.get_gen():
                    stop_def = def_var
                    break
            for gen in range(block.get_id(), next_leader):
                if gen <= stop_def:
                    for d in definitions.items():
                        if gen == d[0]:
                            if var in d[1][1]:
                                locations.append(d[0])
                    for rg in return_goto.items():
                        if gen == rg[0]:
                            if var in rg[1]:
                                locations.append(rg[0])
    return locations

def main():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("file", help="name of a file with three-address instructions")
    args_parser.add_argument("location", type=int, help="location of a definition in a given file")
    
    args = args_parser.parse_args()
    file = args.file
    location = args.location

    # parse file to see whether it contains a
    # valid three-address instructions
    with open(file, "r") as tac_file:
        for i, line in enumerate(tac_file):
            yacc.parse(line)

    definitions, num_lines = bb.make_definitions(file)
    if location > num_lines or location < 1:
        print("No such location.")
        exit(0)
    if location not in definitions.keys():
        print("\nNo assignment at " + str(location) + ".\n" + bb.get_line(file, location))
        exit(0)
    
    return_goto = bb.make_return_goto(file, list(definitions.keys()))

    blocks = bb.make_basic_blocks(file)
    blocks = bb.erase_empty_block(blocks, len(blocks) - 1)

    var_def = bb.var_def(definitions)
    list_ids = bb.block_ids(blocks)
    gen(blocks, list_ids, list(definitions.keys()))  
    kill(blocks, definitions, var_def)
    
    algorithm(list_ids, blocks)
    # bb.print_blocks(blocks)

    locations = get_definitions(num_lines, list_ids, definitions, var_def, return_goto, blocks, location)
    bb.print_locations(file, location, locations)

if __name__ == "__main__":
    main()