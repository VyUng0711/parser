from collections import defaultdict
from math import sqrt, sin, cos, tan


def read_line(file):
    """
    Helper function to read a file line by line and return list of lines.
    """
    with open(file) as opened:
        lines = opened.readlines()
    return lines


def convert_grammar(grammar_file):
    """
        This function processes the grammar contained in the .txt file into
        list of list (each list contains one rule) and converts the grammar
        into Chomsky Normal Form by adding more rules and non terminal symbols
        accordingly.
        The output is a list of rule. Each rule will have the form:
        A -> B C
        or
        A -> a
        where a is the terminal and A, B, C are variables.
    """
    # Read the text file that contains the grammar
    lines = read_line(grammar_file)
    grammar = []
    for line in lines:
        # If the right hand side contains "|" such as A -> B | C, I split into multiple rows:
        # A -> B and A -> C. This also ensures CNF.
        if "|" in line:
            left, right = line.split("->")
            left = [left.strip()]
            vars = right.split("|")
            for var in vars:
                var_list = var.split()
                grammar.append(left + var_list)
        else:
            grammar.append(line.replace("->", "").split())

    # for l in grammar:
    #     print(l)
    d = defaultdict(list)
    # Remove all rules of the type A -> B C D ... or A -> B a b C d.
    # by breaking the big rule down and adding more shorter rules respectively
    unit = []
    output_grammar = []
    new_rule_ind = 0

    for rule in grammar:
        new = []
        if len(rule) == 2 and rule[1][0] != "'":
            unit.append(rule)
            d[rule[0]].append(rule[1:])
            continue
        elif len(rule) > 2:
            terminals = []
            for i in range(len(rule)):
                if rule[i][0] == "'":
                    terminals.append((rule[i], i))
            if terminals:
                for item in terminals:
                    # Create a new non terminal symbol and replace the terminal symbol with it.
                    # the new non terminal symbol will have the same name as the
                    # symbol it derived from attached the index (for example: A0, B2,...)
                    rule[item[1]] = str(rule[0]) + str(new_rule_ind)
                    new.append([str(rule[0]) + str(new_rule_ind), item[0]])
                new_rule_ind += 1
            while len(rule) > 3:
                new.append([str(rule[0]) + str(new_rule_ind), rule[1], rule[2]])
                rule = [rule[0]] + [str(rule[0]) + str(new_rule_ind)] + rule[3:]
                new_rule_ind += 1
        d[rule[0]].append(rule[1:])
        output_grammar.append(rule)
        if new:
            for new_rule in new:
                output_grammar.append(new_rule)
    while unit:
        rule = unit.pop()
        if rule[1] in d:
            for item in d[rule[1]]:
                new_rule = [rule[0]] + item
                if len(new_rule) > 2 or new_rule[1][0] == "'":
                    output_grammar.append(new_rule)
                else:
                    unit.append(new_rule)
                d[rule[0]].append(rule[1:])
    return output_grammar


def parse(grammar, sentence):
    """
    This function is used for both Question 1 and Question 3 to simulate Parser1 and ParseFunc
    The function is implemented using the idea of the CYK algorithm.
    """
    s = sentence.split()
    n = len(s)
    table = [[[] for x in range(n)] for y in range(n)]
    # Examine each substring of length 1 (which corresponds to each word in the input string)
    for i in range(n):
        for rule in grammar:
            # for rule, test whether rule[0] -> s[i] is a rule.
            if rule[1] == f"'{s[i]}'":
                # If so, we place it into the table in the corresponding cell.
                # table[0][i].append(Node(rule[0], s[i]))
                table[0][i].append(rule[0])

    for length in range(2, n + 1):  # length of the substring
        for start in range(0, n - length + 1):  # start position of the substring
            for left_length in range(1, length):  # length of left side after split
                right_length = length - left_length  # length of right size after split
                # For each rule A -> BC check if cell table[left_length - 1][start] contains rule[1] (B)
                # and if table[right_length - 1][start + left_length] contains rule[2] (C)
                # If so put A (rule[0]) into table[length - 1][start]
                for rule in grammar:
                    if [x for x in table[left_length - 1][start] if x == rule[1]]:
                        if [x for x in table[right_length - 1][start + left_length] if x == rule[2]]:
                            table[length - 1][start].append(rule[0])

    S = grammar[0][0]
    # If our start symbol S is contained in the cell table[-1][0], accept; else, reject.
    if [n for n in table[-1][0] if n == S]:
        print("--> The given string is a member of the language produced by the given grammar.")
        return True
    else:
        print("--> The given string is not a member of the language produced by the given grammar.")
        return False


# The call to parse() in both functions below are redundant, I could just have used parse() in main()
# but just to make sure I covered all parts that was asked in the assignment.
def parser1(grammar, sentence):
    """
    This function is answer for Question 1C.
    """
    return parse(grammar, sentence)


def parse_func(grammar, sentence):
    """
    This function is answer for Question 3C.
    """
    return parse(grammar, sentence)


def func_generator(grammar, sentence):
    """
    This function is answer for Question 3D - outputing the equivalent function if the string is accepted by ParseFunc
    """
    if parse_func(grammar, sentence):
        # Because it's not syntactically correct to have digits in number separated by space,
        # I removed all spaces in the string.
        s = sentence.replace(' ', '')
        left, right = s.split("=")
        # This is the syntax for the function that would be output using the exec() function.
        expr = 'def ' + left + ':\n    ' + right
        print(expr)
        exec(expr)

if __name__ == '__main__':
    # grammar_file = "english_grammar.txt"
    # string_file = "test_english.txt"
    english_grammar = "english_grammar.txt"
    test_english = "test_english.txt"
    func_grammar = "func_grammar.txt"
    test_func = "test_func.txt"
    # Output for Problem 1 (Parser1)
    for s in read_line(test_english):
        # print(s)
        parser1(convert_grammar(english_grammar), s)
    # Output for Problem 2 (both ParseFunc and Function Generator)
    for s in read_line(test_func):
        # print(s)
        # Because parse() is already called within func_generator(),
        # I didn't repeat the computation here, but to test it, please uncomment the line below:
        # parse_func(convert_grammar(func_grammar), s)
        func_generator(convert_grammar(func_grammar), s)

