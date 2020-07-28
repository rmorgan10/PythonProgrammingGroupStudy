#PyQuizmaster 2
* Revisit PyQuizmaster, but with more sophisticated coding practices
* Task is:
    * create a usable set of flashcards for the content of this chapter
    * Build a GUI that utilizes them
    
* The project will be broken into three phases:
    1. Plan the approach
        * What classes are to be used
        * What methods should those classes have?
        * What attributes
        * What protections should those attributes have?
        * Decorators?
        * Descriptors?
        * etc
    2. Implement the backend and API
    3. Implement the GUI and have the cards inside it.
    
## Phase 1: Planning

* As I see it. The UI will look like a typical menu based GUI:
    * A main menu to select different modes of user operation eg.
        * Take the quiz
        * Add quiz cards
        * Modify the parameters of the quiz
        * Exit
        * etc
    * Sub menus and windows for all peripheral operations
    * A game window where the index cards show up and the user is prompted to respond.
    
### Classes:
**Index Card** : The most obvious class that is needed:  
*Attributes* :
* Prompt : prompt for the user. User is shown this when the card shows up, then is asked to correctly answer the question posed
* Answer : Answer to the question posed

Fundamentally this is a simple object that needs to hold little more than these two items. A list of such objects would be better build (not over engineered) as a dictionary or a database. In order to justify the existence of the object well want greater complexity *within* the object.

Possible extensions:
* Difficulty grade (set by user who sets the card)
    * Possible to modify based on how often an incorrect answer is given?
* Plausible wrong answers:
    * If multiple choice is an option, good nearly right answers are key to a challenging quiz
* Type of question: The question posed by the index card can be a matter of context. Some ways they can be posed:
    * Question directly on the card
    * True/False
    * Match definition to a word or vice-versa
    * etc
* Formatting : We may want a variety of formatting options, although not so many that each card is unique, so a code, or set of parsable instructions could be useful.  
 
 This is just kind of a list of attributes. So this could reasonably be put in a database...  

 *Methods*
* load/save???  
  

**Collection of index cards** : A collection type (eg list) that will hold the index cards we want to use.
* This can likely be a list
* We'll want to remove **index card**s that have already been shown to the player from this list
* Sortability might be nice.


**For GUI**
Menus might have similar structures, but its had to know if individual classes are desired without a knowledge of the structure of a GUI