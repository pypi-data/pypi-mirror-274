# The main function provides a commandline interface for the package.
# This way you can use it via python -m modulename.
from pycutroh import *
import argparse

def main():
    """Parameter declaration."""
    
    # Declaring parameters.
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--string', type=str, default='This is a demonstration string.')
    group1 = parser.add_mutually_exclusive_group()
    # If using default = 0, the mutally exclusive group is not working.
    group1.add_argument('-glop', '--getLetterOnPos', type=int, help=("Letter on position to return."))
    group1.add_argument('-glbp', '--getLettersFromPosToPos', type=tuple, help=("Get letter between positions."), nargs=2)
    group1.add_argument('-glbfs', '--getLettersBeforeSign', type=str, help=("Get letters Before specified sign."))
    group1.add_argument('-glas', '--getLettersAfterSign', type=str, help=("Get letters after specified sign."))
    group1.add_argument('-glbs', '--getLettersBetweenSigns', type=tuple, help=("Get letters between specified signs.") , nargs=2)
    
    # Create subparser.
    fieldparser = parser.add_subparsers(dest='fields', help=("Get fields separated by specified delimiter."))
    # Subparsers can not be optional (-f not working).
    fieldparserold = fieldparser.add_parser('f', help=("Get fields by delimiter and join using same delimiter."))
    fieldparserold.add_argument('--getFields', type=tuple, help=("Fields as tuple."), nargs="*")
    fieldparserold.add_argument('--delimiter', type=str, help=("Delimiter to use for field calculation."), nargs=1)
    fieldparserold.add_argument('--newDelimiter', type=str, help=("Delimiter used to join fields."), nargs=1)

    args = parser.parse_args()
    
    # Catching parameters.
    # The if statement needs the else statement at the end to catch 0 as input for the first function.
    if args.getLetterOnPos:
        print(get_letter_on_pos(args.string, args.getLetterOnPos))
    elif args.getLettersFromPosToPos:
        # Create tuple from list of tuples.
        # python -m pycutroh -glbp (0,25)
        # [('0',), ('2', '5')]
        # res = (0,25)
        res = [int(' '.join(tups).replace(' ','')) for tups in args.getLettersFromPosToPos]
        print(get_letters_from_pos_to_pos(args.string, res))
    elif args.getLettersBeforeSign:
        print(get_letters_before_sign(args.string, args.getLettersBeforeSign))
    elif args.getLettersAfterSign:
        print(get_letters_after_sign(args.string, args.getLettersAfterSign))
    elif args.getLettersBetweenSigns:
        print(get_letters_between_signs(args.string, args.getLettersBetweenSigns[0][0], args.getLettersBetweenSigns[1][0]))
    elif args.fields:
        # # Create tuple from list of tuples.
        fieldtup = [int(' '.join(tups).replace(' ','')) for tups in args.getFields]
        # Catch if newDelimiter is used otherwise run normal get_fields function. 
        if args.newDelimiter == None:
            print(get_fields(args.string, tuple(fieldtup), args.delimiter[0]))
        elif args.getFields == 0 and args.newDelimiter != None:
            print(get_fields(args.string, tuple(fieldtup), args.delimiter[0]))
        else:
            print(get_fields_new_separator(args.string, fieldtup, args.delimiter[0], args.newDelimiter[0]))
    else:
        print(get_letter_on_pos(args.string, args.getLetterOnPos))
    
    
if __name__ == '__main__':
    main()