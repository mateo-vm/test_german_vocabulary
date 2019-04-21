#! python3
# Tester for German learners (from English)
# Format of the info in the database:
# {'german': ['english', 'class', 'theme', 'additional info']}

import shelve, re, random, time

# ------------------------------------------------------------------------------
# Auxiliar functions -----------------------------------------------------------
# ------------------------------------------------------------------------------

def get_noun():
# Function that controls the proper input of a noun
    while 1:
        print('German words are cap sensitive.')
        print('Noun requires its article and a starting capital character.')
        g_noun = input()
        validate = noun_regex.fullmatch(g_noun)
        if validate != None:
            break
    return g_noun

def get_verb():
# Function that controls the proper input of a verb
    while 1:
        print('German words are cap sensitive (please do not use capital letters).')
        print('Please write the verb in infinitive.')
        g_verb = input()
        if g_verb.islower() and g_verb.isalpha() and g_verb[-1]=='n': # Verbs in german always finish in n
            break
    return g_verb

def get_rest():
    while 1:
        print('German words are cap sensitive (please do not use capital letters).')
        print('Please write the desired word.')
        g_rest = input()
        if g_rest.islower() and g_rest.isalpha():
            break
    return g_rest

def print_info(i_german, i_english, i_class, i_theme, extra):
# Print the information of a word
    print('    German: ' + i_german)
    print('   English: ' + i_english)
    print('     Class: ' + i_class)
    print('     Theme: ' + i_theme)
    print('Extra info: ' + extra)

def print_list(f, l, c1, c2, c3):
    list_file = open(f, 'a')
    for key in l:
        # Print the line
        list_file.write(key.ljust(c1) + ' | ' + db[key][0].rjust(c2) +
                        ' | '+db[key][2].rjust(c3))
        if db[key][3] != '':
            list_file.write('     (' + db[key][3] + ')')
        list_file.write('\n')
    list_file.close()

def choose_class_test():
    print('''Chose the set of words you want to use:
    1.- All the words.
    2.- Nouns.
    3.- Verbs.
    4.- Adjectives.
    5.- Others.''')
    test_list = []
    while 1:
        option = input()
        if option == '1':
            noun_flag = True
            test_list = list(db.keys())
            break
        elif option == '2':
            noun_flag = True
            for key in db:
                if db[key][1] == 'noun':
                    test_list.append(key)
            break
        elif option == '3':
            noun_flag = False
            for key in db:
                if db[key][1] == 'verb':
                    test_list.append(key)
            break
        elif option == '4':
            noun_flag = False
            for key in db:
                if db[key][1] == 'adjective':
                    test_list.append(key)
            break
        elif option == '5':
            noun_flag = False
            for key in db:
                if db[key][1] == 'other':
                    test_list.append(key)
            break
        else:
            print('Option not valid.')
    return (noun_flag, test_list)

def choose_theme(input_list):
    theme_list = []
    for key in input_list:
        if db[key][2] not in theme_list:
            theme_list.append(db[key][2])
    theme_list.sort()
    print('These are the available themes for this test:')
    for i in range(len(theme_list)):
        print('   ' + str(i+1) + '.- ' + theme_list[i])
    while 1:
        print('Choose one or press ENTER to go with all.')
        theme = input()
        if theme == '':
            return input_list
        elif theme.isdecimal():
            if (int(theme) - 1) in range(len(theme_list)):
                theme = theme_list[int(theme) - 1]
                break
    output_list = []
    for key in input_list:
        if db[key][2] == theme:
            output_list.append(key)
    return output_list

def print_results(total, right, duration):
    hours = duration // 3600
    minutes = (duration // 60) - hours * 60
    seconds = duration - minutes * 60 - hours * 3600
    # Print the results of the test
    try:
        print('These are the results of the test:')
        print('          Questions: {0:d}'.format(total))
        print('    Correct answers: {0:d}'.format(right))
        print('         Percentage: {0:.2f}%'.format(100*right/total))
        print('         Total time: {0:.0f}h {1:.0f}m {2:.2f}s'.format(hours, minutes, seconds))
        print('  Time per question: {0:.2f}s'.format(duration/total))
    except ZeroDivisionError:
        print('No more results avaliable')

# ------------------------------------------------------------------------------
# Tests ------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def e2g_test():
    (noun_flag, test_list) = choose_class_test()
    # Ask for the requirement of the article
    article_flag = False
    if noun_flag:
        print('''Would you like to include the article too?
(article + noun OR only noun) [Y/N]''')
        article_option = ''
        while 1:
            article_option = input()
            article_option = article_option.lower()
            if article_option == 'y':
                break
            elif article_option == 'n':
                article_flag = True
                break
    # Check if there are words before continuing
    if len(test_list) > 0:
        test_list = choose_theme(test_list)
        print('''German words are cap sensitive.
(Remember the capital letter for the nouns)''')
        total = 0
        right = 0
        # Start of the test
        start = time.time()
        while 1:
            ans = '1'
            key = random.choice(test_list)
            # Check is there is any extra info and print it
            if db[key][3] == '':
                print(db[key][0])
            else:
                print(db[key][0] + ' (' + db[key][3] + ')')            
            while all(x.isalpha() or x.isspace() for x in ans) == False:
                ans = input()
            # Check the requirement of the article
            sol = key
            if article_flag:
                if db[key][1] == 'noun':
                    sol = key[4:]
            # Check solution
            if ans == 'e':
                break
            elif ans == sol:
                right += 1
                print('RIGHT answer')
            else:
                print('WRONG answer')
                print('The right answer is: ' + sol)
            total += 1
        end = time.time()
        duration = end - start
        print_results(total, right, duration)
    else:
        print('There are no words in the database that match the requirements.')

def g2e_test():
    (noun_flag, test_list) = choose_class_test()
    # Check if there are words before continuing
    if len(test_list) > 0:
        test_list = choose_theme(test_list)
        total = 0
        right = 0
        # Start of the test
        start = time.time()
        while 1:
            ans = '1'
            key = random.choice(test_list)
            print(key)
            while (ans.isalpha() == False):
                ans = input()
            ans = ans.lower()
            # Check solution
            if ans == 'e':
                break
            elif ans == db[key][0]:
                right += 1
                print('RIGHT answer')
            else:
                print('WRONG answer')
                print('The right answer is: ' + db[key][0])
            total += 1
        end = time.time()
        duration = end - start
        print_results(total, right, duration)
    else:
        print('There are no words in the database that match the requirements.')

def article_test():
    print('''Enter the following number for each article:
    1.- Der     2.- Die     3.- Das
    Type \'e\' to finish the test.''')
    test_list = []
    art_list = ['der', 'die', 'das']
    for key in db:
        if db[key][1] == 'noun':
            test_list.append(key)
    # Check if there are words before continuing
    if len(test_list) > 0:
        test_list = choose_theme(test_list)
        total = 0
        right = 0
        # Start of the test
        start = time.time()
        while 1:
            ans = ''
            key = random.choice(test_list)
            print(key[4:])
            while ans != '1' and ans != '2' and ans != '3' and ans != 'e':
                ans = input()
            if ans == 'e':
                break
            elif art_list[int(ans)-1] == key[0:3]:
                right += 1
                print('RIGHT answer')
            else:
                print('WRONG answer')
                print('The right answer is: ' + key[0:3])
            total += 1
        end = time.time()
        duration = end - start
        print_results(total, right, duration)
    else:
        print('There are no nouns in the database.')
        
# ------------------------------------------------------------------------------
# Main command functions -------------------------------------------------------
# ------------------------------------------------------------------------------

def print_help():
    print('''These are the commands available:
      \'add\': allows to add a word to the database.
   \'delete\': allows to delete a word from the database.
    \'clear\': deletes all the words on the database.
     \'list\': creates a list with the words in the database
               and stores them on a .txt file.
     \'info\': shows the information of a word.
     \'test\': take a test to practice.
     \'exit\': exits the program.''')

def add():
# Function that allows to add new words (also can overwrite the previous ones)
    # Choose class
    global classes
    while 1:
        print('What is the class of the word you want to add?')
        print('''    1.- Noun.
    2.- Verb.
    3.- Adjective.
    4.- Other.''')
        vclass = input()
        if vclass == '1':
            vclass = 'noun'
            break
        elif vclass == '2':
            vclass = 'verb'
            break
        elif vclass == '3':
            vclass = 'adjective'
            break
        elif vclass == '4':
            vclass = 'other'
            break
    # Enter word in german
    print('Please introduce the german word.')
    if vclass == 'noun':
        german = get_noun()
    elif vclass == 'verb':
        german = get_verb()
    else:
        german = get_rest()
    # Enter word in english
    while 1:
        print('Please enter the word in English.')
        if vclass == 'verb':
            print('The verb does no require beginning with \'to \'.')
        english = input()
        english = english.lower()
        if english.isalpha():
            break
    # Enter theme
    theme_list = []
    for key in db:
        if db[key][2] not in theme_list:
            theme_list.append(db[key][2])
    theme_list.sort()
    while 1:
        print('This is the current list of existing themes:')
        for i in range(len(theme_list)):
            print('   ' + str(i+1) + '.- ' + theme_list[i])
        print('''Choose a theme from the previous list or write a new one.
(The default option is general)''')
        while 1:
            theme = input()
            if theme == '':
                theme = 'general'
                break
            elif theme.isdecimal():
                if (int(theme) - 1) in range(len(theme_list)):
                    theme = theme_list[int(theme) - 1]
                    break
            elif all(x.isalpha() or x.isspace() for x in theme):
                theme = theme.lower()
                break
            print('Option not valid')
        add_theme = ''
        print('Do you want the word \'' + german + '\' to be included in the theme \'' + theme + '\'? [Y]:')
        add_theme = input()
        add_theme = add_theme.lower()
        if add_theme == 'y':
            break
    # Add extra information to help during the tests
    print('Would you like to add extra information?')
    print('''(This info will be used in the English to German tests
to differenciate between different translations of the same word)''')
    print('If you do not want it, just press ENTER.')
    extra_info = input()
    # Confirm and save the new word
    add_var = ''
    while add_var != 'y' and add_var != 'n':
        print('Do you want to save the word with the following content? [Y/N]:')
        print_info(german, english, vclass, theme, extra_info)
        add_var = input()
        add_var = add_var.lower()
    if add_var == 'y':
        db[german] = [english, vclass, theme, extra_info]
        print('The new word was successfully added.')
    else:
        print('The new word was not added.')

def delete():
# Function that allows to delete words
    while 1:
        print('Please enter the german word you want to delete from the list.')
        print('(This input is cap sensitive)')
        print('Type \'EXIT\' to exit this section')
        word = input()
        if word == 'EXIT':
            break
        elif word in db:
            # Confirm the word you want to delete
            print('Are you sure you want to delete \'' + word + '\'?')
            print('(Confirm by writing the word again)')
            word2 = input()
            if word == word2:
                del db[word]
                print('The word was successfully deleted.')
                break
            else:
                print('Confirmation word was wrong.')
        else:
            print('This word is not in the list.')

def clear():
# Deletes the entire list of words
    confirmation = 'I am sure.'
    print('Are you sure you want to clear all the words on the database?')
    print('Confirm this by printing \'' + confirmation +'\'')
    print('(This input is cap sensitive)')
    conf_input = input()
    if conf_input == confirmation:
        for key in db:
            del db[key]
        print('Database succesfully cleared.')
    else:
        print('Database not cleared.')
    
def make_list():
# Creates a list of the words on the database
    # Initialize the variables
    noun_list = []
    verb_list = []
    adj_list = []
    oth_list = []
    max_len_german = 0
    max_len_english = 0
    max_len_theme = 0
    file_name = 'german_words_list.txt'
    print('Creating list...')
    # Get the words
    wlist = list(db.keys())
    for key in wlist:
        # Get the longest word in each column
        if len(key) > max_len_german:
            max_len_german = len(key)
        if len(db[key][0]) > max_len_english:
            max_len_english = len(db[key][0])
        if len(db[key][2]) > max_len_theme:
            max_len_theme = len(db[key][2])
        # Agroup the words according to their class
        if db[key][1] == 'noun':
            noun_list.append(key)
        elif db[key][1] == 'verb':
            verb_list.append(key)
        elif db[key][1] == 'adjective':
            adj_list.append(key)
        else:
            oth_list.append(key)
    # Store the list on a .txt file
    # Store the nouns
    list_file = open(file_name, 'w')
    list_file.write(' NOUNS '.center(40, '-') + '\n')
    list_file.close()
    noun_list.sort(key=lambda x: x[4])
    print_list(file_name, noun_list, max_len_german, max_len_english, max_len_theme)
    # Store the verbs
    list_file = open(file_name, 'a')
    list_file.write(' VERBS '.center(40, '-') + '\n')
    list_file.close()
    print_list(file_name, verb_list, max_len_german, max_len_english, max_len_theme)
    # Store the adjectives
    list_file = open(file_name, 'a')
    list_file.write(' ADJECTIVES '.center(40, '-') + '\n')
    list_file.close()
    print_list(file_name, adj_list, max_len_german, max_len_english, max_len_theme)
    # Store the rest
    list_file = open(file_name, 'a')
    list_file.write(' OTHERS '.center(40, '-') + '\n')
    list_file.close()
    print_list(file_name, oth_list, max_len_german, max_len_english, max_len_theme)
    print('List was stored in \'' + file_name + '\'.')
    
def info():
# Shows the information of a word
    while 1:
        print('Please enter the german word you want more information about.')
        print('(This input is cap sensitive)')
        print('Type \'EXIT\' to exit this section')
        word = input()
        if word == 'EXIT':
            break
        elif word in db:
            # Call the function to print the information
            print_info(word, db[word][0], db[word][1], db[word][2], db[word][3])
            break
        else:
            print('This word is not in the list.')
    
def test():
# Tests
    print('''Choose the type of test you would like to take:
    1.- English to German.
    2.- German to English.
    3.- Article test.''')
    while 1:
        test_type = input()
        if  test_type == '1':
        # English to German test
            e2g_test()
            break
        elif  test_type == '2':
        # German to English test
            g2e_test()
            break
        elif test_type == '3':
        # Article test
            article_test()
            break
        else:
            print('Option not valid.')

def invalid():
    print('The command introduced was not found.')

def exit_program():
    db.close()
    global exit_flag
    exit_flag = True
    
# ------------------------------------------------------------------------------
# Start the program ------------------------------------------------------------
# ------------------------------------------------------------------------------

# Opens and loads the database
db = shelve.open('german_database')
# Create the variables and regexs
classes = ['noun', 'verb', 'adjective', 'other']
exit_flag = False
noun_regex = re.compile('''(
    (der|die|das)          # Article
    ([ ])                  # Space
    ([A-ZÄÜÖ][a-zäüöß]*)   # Noun
    )''', re.VERBOSE | re.UNICODE)


# Introduction
print('Welcome to this tester.')
print('Please type the task you want to carry out.')
print('Type \'help\' if you need information about the commands.')

while(exit_flag == False):
    # Read the command
    command = input()
    command = command.lower()
    
    input_map = {
        'help': print_help,
        'add': add,
        'delete': delete,
        'clear': clear,
        'list': make_list,
        'info': info,
        'test': test,
        'exit': exit_program
        }
    input_map.get(command, invalid)()
    
