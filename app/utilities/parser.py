import re
import operator
import logging

from .logging_config import setup_logging

class ParserError(Exception):
    """Custom exception class for parsing errors."""
    pass

def evaluate_expression(expression, cell_resolver):
    logging.info(f"In evaluate_expression with expression: {expression}, cell_resolver: {cell_resolver}")
    
    setup_logging()
    
    def get_priority(op):
        priorities = {'+': 1, '-': 1, '*': 2, '/': 2}
        return priorities.get(op, 0)

    def apply_operation(operators, values):
        if not operators:
            logging.error("Operator stack is empty.")
            raise ParserError("Operator stack is empty.")
        
        op = operators.pop()

        logging.info(f"Applying operation: {op} with values: {values}")  # Log operation details

        if len(values) < 2:
            logging.error(f"Insufficient values for operation with operator {op}.")
            raise ParserError("Insufficient values for operation.")
        
        # Ensure that we have enough values before attempting to pop
        right, left = values.pop(), values.pop()

        operations = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}
        
        # Log the operation with operands for clarity
        logging.info(f"Applying operation: {left} {op} {right}")
        
        if op not in operations:
            logging.error(f"Invalid operator {op}.")
            raise ParserError(f"Invalid operator {op}.")
        
        result = operations[op](left, right)
        values.append(result)
        logging.info(f"Operation result: {result}")

    def get_value(token):
        if re.match(r'^-?\d+(\.\d+)?$', token):
            return float(token)
        elif re.match(r'^[A-Za-z]+\d+$', token):
            if cell_resolver:
                logging.info(f"Attempting to resolve token: {token}")
                try:
                    resolved_value = cell_resolver(token)
                except Exception as e:
                    logging.error(f"Error resolving cell {token}: {e}")
                    raise
                if resolved_value is None:
                    logging.error(f"Cell {token} not found.")
                    raise ParserError(f"Cell {token} not found.")
                logging.info(f"Resolved {token} to {resolved_value}")
                return resolved_value
            else:
                logging.error(f"Unable to resolve cell reference for {token}.")
                raise ParserError(f"Unable to resolve cell reference for {token}.")
        else:
            logging.error(f"Invalid token {token}.")
            raise ParserError(f"Invalid token {token}.")

    tokens = re.findall(r'[A-Za-z]+\d+|\d+\.?\d*|[+\-*/()]', expression)

    logging.info(f"Tokens identified: {tokens}")
    
    values = []
    operators = []

    for token in tokens:
        try:
            if token.isdigit():
                logging.info(f"Token is a number: {token}")  # Added to indicate token is recognized as a number
                values.append(float(get_value(token)))

            elif re.match(r'^[a-zA-Z]+\d+$', token):
                logging.info(f"Token is a cell reference: {token}")
                values.append(float(get_value(token)))

            elif token in ('+', '-', '*', '/'):
                logging.info(f"Token is an operator: {token}")  # Added to indicate token is recognized as an operator
                while operators and get_priority(operators[-1]) >= get_priority(token):
                    apply_operation(operators, values)
                operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    apply_operation(operators, values)
                operators.pop()  # Remove the '('
        except ParserError as e:
            logging.error(f"Parser error during evaluation: {e}")
            raise
    
    while operators:
        apply_operation(operators, values)

    if len(values) != 1:
        logging.error("Error in expression evaluation: Incorrect number of values after evaluation.")
        raise ParserError("Error in expression evaluation.")
    
    final_value = values[0]
    if final_value.is_integer():  # Check if the value is an integer
        logging.info(f"Final evaluated value: {int(values[0])}")
        return int(final_value)  # Convert to int if it has no decimal part
    else:
        logging.info(f"Final evaluated value: {values[0]}")
        return final_value  # Return as float if it has a decimal part