# Problem Set 4C
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string


def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    result = []
    if len(sequence) == 1:
        #base case
        #Return list of permutations with base case
        return [sequence]
    else:
        #cut the first character of the string and calls get_permutation again
        base = get_permutations(sequence[1:])
        
        #check all the words in the list of permutation
        for word in base:
            #Check all the letters in each word
            for i in range(len(word)):
                #Adds the letter in all the permutations
                aux = word[0:i]+ sequence[0]+word[i:]
                #Verifies for duplicates
                if aux not in result:
                    result.append(aux)
            #Adds the letter at the last position of the permutation
            aux = word+ sequence[0]
            #Verifies for duplicates
            if aux not in result:
                result.append(aux)
        #Return list of permutations
        return(result)

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words("words.txt")
    
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words.copy()
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        
        #Creates dictionaries for upper and lower case vowels
        vowel_dict = {}
        vowel_dict_upper = {}
        for i in range(len(VOWELS_LOWER)):
            #Maps the permutation to the vowels
            vowel_dict[VOWELS_LOWER[i]]= vowels_permutation[i]
            vowel_dict_upper[VOWELS_UPPER[i]]= vowels_permutation[i].upper()
        #Create a single dictionary with upper and lower case vowels
        vowel_dict.update(vowel_dict_upper)
        
        lower_letters = string.ascii_lowercase
        upper_letters = string.ascii_uppercase
        shift_map={}
        aux_upper = {}
        letters = lower_letters+upper_letters
        #Iterates through all the letters, applying the permutation if they are vowels, do nothing otherwise
        for i in letters:
            if i in VOWELS_LOWER:
                shift_map[i] = vowel_dict[i]
            elif i in VOWELS_UPPER:
                aux_upper[i] = i
            else:
                aux_upper[i]=i
        #Create a single dictionary with all the mappings
        shift_map.update(aux_upper)
        #Return the dictionary
        return shift_map
    
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        
        #Punctuation to ignore
        punctuation = " .,:;!?-"
        shifted_message = ''
        #Goes through each letter of the original message, and decode it if it's a vowel.
        for letter in self.message_text:
            if letter not in punctuation:
                shifted_message = shifted_message+transpose_dict[letter]
            else:
                shifted_message = shifted_message+letter
        #Returns coded message
        return shifted_message
        

        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        SubMessage.__init__(self, text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
        #Get a list with all the permutations for the vowels
        list_of_permutations=get_permutations("aeiou")

        
        #Create auxiliary variables
        valid_max=-10000
        valid_counter = 0
        #Iterates through the list of permuations
        for perm in list_of_permutations:
            #Applies the encode on the message with the selected permutation and store the result
            possible_result = self.apply_transpose(self.build_transpose_dict(perm))
            
            #Iterates through the result to check which permutations has the greater number of valid words
            for word in possible_result.split():
                if is_word(self.valid_words, word) == True:
                    valid_counter = valid_counter+1
            if valid_counter>valid_max:
                valid_max = valid_counter
                best_permutation = perm
            valid_counter = 0
        #Return best result
        return [self.apply_transpose(self.build_transpose_dict(best_permutation))]
        
    

if __name__ == '__main__':

    # Example test case
    message = SubMessage("Kinder Garden!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Kindar Gerdan!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
     
