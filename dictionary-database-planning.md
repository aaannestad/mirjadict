Database categories:

* id
* form: the word's actual underlying form (without tones)
* tone-pattern
* basic-word-class: noun, verb, etc
* json

json categories:
* use-case (case frame, 'serialised', etc)
  * sense
    * text-description (should include formattable commands for e.g. \subj, OBJ, OBL)
    * lexical-aspect (?)

also a relational table for etymologies etc:
* id
* base-1-id
* base-2-id (for compounds)
* result-id
* nature-of-relationship


OR IN JUST JSON

* id
* form
* tone-pattern
* basic-word-class
* etymology-set []
  * derived-from-ids []
    * relation []
      * id
      * relation-nature
* definition-set []
  * use-case [] (one per syntactic use case)
    * use-case-label (with findable formattable case label commands; of the form e.g. '\subj,OBJ' or 'SERIALISED')
    * sense-set []
      * text-description (with case label commands, of the form e.g. '\subj hits OBJ')
      * example
      * lexical-aspect?
