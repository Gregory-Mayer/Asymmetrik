import nltk
import re

#takes in raw text and parses out the name and returns it as a string 
def get_human_names(text):
    #turns the text into a list of words
    tokens = nltk.tokenize.word_tokenize(text)
    #tags the words into categories to be used to identify the names inside the the list
    pos = nltk.pos_tag(tokens)
    #this is used if the bigram list doesnt find a name
    sentt = nltk.ne_chunk(pos, binary = False)
    #to return the person object
    person_list = []
    #used to increase the accuracy of identifing the name
    non_person_list = ['Software','Phone','Engineer','Analytic','Developer' , 'Technologies' , 'LTD', 'LLC', 'INC', 'inc', 'llc', 'ltd']
    person = []
    name = ""
    bigramList = list(nltk.bigrams(pos))
    #goes through the bigrams and finds a matching pair of NNP type grams and are not in the non personlist
    for gram in bigramList:
        #the non person list is to help improve the accuracy of identifying the name the first index of the bigram is the text and the second is the tag value
        if ((gram[0][0] not in non_person_list) and (gram[0][1] == "NNP") and (gram[1][0] not in non_person_list) and (gram[1][1] == "NNP")):
            name = gram[0][0] + " " + gram[1][0]
            person_list.append(name)
            break
    #goes through a tree search of the text of a chuck of text and finds all the person type leaves
    if(len(person_list) < 1):
        person_list = []
        for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
            for leaf in subtree.leaves():
                person.append(leaf[0])
            if len(person) > 1: 
                for part in person:
                    if part not in non_person_list:
                        name += part + ' '
                if name[:-1] not in person_list:
                    person_list.append(name[:-1])
                name = ''
            person = []
    #goes through a tree search of the text of a chuck of text and finds all the organization type leaves if no person leave is found
    if(len(person_list) < 1):
        person_list = []
        for subtree in sentt.subtrees(filter=lambda t: t.label() == 'ORGANIZATION'):
            for leaf in subtree.leaves():
                person.append(leaf[0])
            if len(person) > 1: 
                for part in person:
                    if part not in non_person_list:
                        name += part + ' '
                if name[:-1] not in person_list:
                    person_list.append(name[:-1])
                name = ''
            person = []
    fullName = ""
    #turns the list into a string for the return to be a string
    for name in person_list:
        if fullName == "":
            fullName = name
        else:
            fullName = fullName + " " + name 
    return (fullName)

#
#
#takes in raw text and returns the a phone number as a string 
def get_Phone_Number(text):
    #cleans up the text file to make it easier to user regex to find the phone
    #number
    result = ""
    text = text.replace(' ', '').replace('\r', '').replace('\s','').replace('-','').replace('\\','').replace('/','').replace('+','').replace('e','').replace('t','').replace('s','').replace('(','').replace(')','')
    #removes the fax if there exists a fax number on the business card
    if(re.search(r'((fax|FAX|Fax))', text) != "" and re.search(r'((fax|FAX|Fax))', text) != None):
        text = re.sub(r'(fax|FAX|Fax)(:?)(\d?)\d\d\d\d\d\d\d\d\d\d', '', text)
    #finds the remaining phone number
    if(re.search(r'(\d\d\d\d\d\d\d\d\d\d\d|\d\d\d\d\d\d\d\d\d\d)', text) != "" and re.search(r'(\d\d\d\d\d\d\d\d\d\d\d|\d\d\d\d\d\d\d\d\d\d)', text) != None):
        result = re.search(r'(\d\d\d\d\d\d\d\d\d\d\d|\d\d\d\d\d\d\d\d\d\d)' , text).group()

    return result

#
#
#takes raw text and returns the email from the text as a string
def get_Email(text):
    result = ""
    if(re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+', text) != "" and re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+', text) != None):
        result = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+',text).group()
    return result

#first test for the program to parse out the name, number, and email.
TestText = """
ASYMMETRIK LTD
Mike Smith
Senior Software Engineer
(410)555-1234
msmith@asymmetrik.com
"""

#second test for the program to parse out the name, number, and email.
TestText1 = """
Foobar Technologies
Analytic Developer
Lisa Haung
1234 Sentry Road
Columbia, MD 12345
Phone: 410-555-1234
Fax: 410-555-4321
lisa.haung@foobartech.com
"""


#third test for the program to parse out the name, number, and email.
TestText2 = """
Arthur Wilson
Software Engineer
Decision & Security Technologies
ABC Technologies
123 North 11th Street
Suite 229
Arlington, VA 22209
Tel: +1 (703) 555-1259
Fax: +1 (703) 555-1200
awilson@abctech.com
"""

#testing the number for the fax coming before the phone number
TestText3 = """
Arthur Wilson
Software Engineer
Decision & Security Technologies
ABC Technologies
123 North 11th Street
Suite 229
Arlington, VA 22209
Fax: +1 (703) 555-1200
Tel: +1 (703) 555-1259
awilson@abctech.com
"""

# scaled application of the parser to parse out the name, number, and email out of a resume.
TestText4 = """
GREGORY MAYER
211 Kent rd, Glen Burnie, MD | (443) 805-4974 | g.mayer.93@gmail.com

Education
Sofiac (now run by Exerceo)                                              Hanover, MD
Information Technology Initiative: Software Development Program, and Cybersecurity Program        
Worked approximately 20 hours a week for both of the schools that I have attended. 
University of Maryland, Baltimore County (UMBC)                               Baltimore, MD
BS: Computer Science                                        
GPA: 3.75/4.0        Major GPA: 4.0/4.0                                Anticipated Graduation: 05/2019
Anne Arundel Community College                                                                                                                                    Arnold, MD
AA: Transfer Studies Mathematics                                                                                                                                     05/2013
GPA: 3.64
"""

def main():

    print("\n\n********** TEST 1 ***********")
    text = TestText
    #print(text)
    name = get_human_names(text)
    phone = get_Phone_Number(text)
    email = get_Email(text)
    print( "Name: " + name)
    print( "Email: " + email)
    print( "Phone: " + phone)
    if(name == "Mike Smith" and phone == "4105551234" and email == "msmith@asymmetrik.com"):
        print("Passed Test 1")
    else:
        print("Failed Test 1")
    print("*****************************")
   
    print("\n\n********** TEST 2 ***********")
    text = TestText1
    #print(text)
    name = get_human_names(text)
    phone = get_Phone_Number(text)
    email = get_Email(text)
    print( "Name: " + name)
    print( "Email: " + email)
    print( "Phone: " + phone)
    if(name == "Lisa Haung" and phone == "4105551234" and email == "lisa.haung@foobartech.com"):
        print("Passed Test 2")
    else:
        print("Failed Test 2")
    print("*****************************")

    print("\n\n************ TEST 3 ************")
    text = TestText2
    #print(text)
    name = get_human_names(text)
    phone = get_Phone_Number(text)
    email = get_Email(text)
    print( "Name: " + name)
    print( "Email: " + email)
    print( "Phone: " + phone)
    if(name == "Arthur Wilson" and phone == "17035551259" and email == "awilson@abctech.com"):
        print("Passed Test 3")
    else:
        print("Failed Test 3")
    print("********************************")
        
    print("\n\n************ TEST 4 ************")
    text = TestText4
    #print(text)
    name = get_human_names(text)
    phone = get_Phone_Number(text)
    email = get_Email(text)
    print( "Name: " + name)
    print( "Email: " + email)
    print( "Phone: " + phone)
    if(name == "GREGORY MAYER" and phone == "4438054974" and email == "g.mayer.93@gmail.com"):
        print("Passed Test 4")
    else:
        print("Failed Test 4")
    print("********************************")

    print("\n\n********* EMPTY STRING TEST **********")
    text = ""
    #print(text)
    name = get_human_names(text)
    phone = get_Phone_Number(text)
    email = get_Email(text)
    print( "Name: " + name)
    print( "Email: " + email)
    print( "Phone: " + phone)
    if(name == "" and phone == "" and email == ""):
        print("Passed Empty String Test")
    else:
        print("Failed Empty String Test")
    print("**************************************")        
    
    return 0
main()
