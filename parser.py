"""
ፓርሰር - የአማርኛ ፕሮግራሚንግ ቋንቋ ሁለተኛ ደረጃ ማቀነባበሪያ
ሚና: ቶከኖችን ወደ የኮድ ዛፍ (AST) መቀየር
"""

import traceback

class ParseError(Exception):
    def __init__(self, message, line_num, column, line_content=""):
        self.message = message
        self.line_num = line_num
        self.column = column
        self.line_content = line_content
        super().__init__(self._format_message())
    
    def _format_message(self):
        """ዝርዝር የስህተት መልዕክት ማዘጋጀት"""
        msg = f"\n❌ የአጻጻፍ ስህተት በምስር {self.line_num}, አምድ {self.column}\n"
        if self.line_content:
            msg += f"   {self.line_content}\n"
            msg += f"   {' ' * (self.column - 1)}^\n"
        msg += f"   {self.message}"
        return msg

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.ast = []
        self.current_token = None
        self._advance()
    
    def _advance(self):
        """ወደ ቀጣይ ቶከን መሄድ"""
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
            self.pos += 1
        else:
            self.current_token = ('EOF', '', -1, -1)
    
    def _peek(self):
        """ወደፊት ማየት (ቀጣዩን ቶከን ሳይቀይር)"""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ('EOF', '', -1, -1)
    
    def _peek_ahead(self, n=1):
        """በርካታ ቶከኖች ወደፊት ማየት"""
        if self.pos + n - 1 < len(self.tokens):
            return self.tokens[self.pos + n - 1]
        return ('EOF', '', -1, -1)
    
    def _expect(self, token_type, value=None):
        """የተወሰነ ቶከን መገኘቱን ማረጋገጥ"""
        if (self.current_token[0] == token_type and 
            (value is None or self.current_token[1] == value)):
            result = self.current_token
            self._advance()
            return result
        else:
            # Get line content for better error message
            line_content = ""
            if hasattr(self, 'lexer') and hasattr(self.lexer, 'get_line_content'):
                line_content = self.lexer.get_line_content(self.current_token[2])
            
            expected = f"{token_type} {value if value else ''}"
            got = f"{self.current_token[0]} {self.current_token[1]}"
            raise ParseError(
                f"የሚጠበቅ: {expected}, የተገኘ: {got}",
                self.current_token[2],
                self.current_token[3],
                line_content
            )
    
    def parse(self):
        """መላውን ፕሮግራም ማቀናበር"""
        try:
            while self.current_token[0] != 'EOF':
                statement = self._parse_statement()
                if statement:
                    self.ast.append(statement)
            return self.ast
        except ParseError:
            raise
        except Exception as e:
            # Convert any unexpected error to ParseError with location
            line_num = self.current_token[2] if self.current_token else -1
            column = self.current_token[3] if self.current_token else -1
            line_content = ""
            if hasattr(self, 'lexer') and hasattr(self.lexer, 'get_line_content'):
                line_content = self.lexer.get_line_content(line_num)
            
            raise ParseError(
                f"ያልተጠበቀ ስህተት: {str(e)}",
                line_num,
                column,
                line_content
            )
    
    def _parse_statement(self):
        """አንድ መግለጫ ማቀናበር"""
        token_type, token_value, line_num, column = self.current_token
        
        # Skip semicolons
        if token_type == 'SEMICOLON':
            self._advance()
            return None
        
        if token_type == 'KEYWORD':
            if token_value == 'PRINT':
                return self._parse_print_statement()
            elif token_value == 'IF':
                return self._parse_if_statement()
            elif token_value == 'FOR':
                return self._parse_for_statement()
            elif token_value == 'WHILE':
                return self._parse_while_statement()
            elif token_value == 'FUNCTION':
                return self._parse_function_statement()
            elif token_value == 'RETURN':
                return self._parse_return_statement()
            elif token_value in ['INT', 'STRING']:
                return self._parse_declaration_statement()
            elif token_value == 'READ':
                return self._parse_read_statement()
            elif token_value == 'TRY':
                return self._parse_try_catch_statement()
            elif token_value == 'LIST':
                return self._parse_list_declaration()
            elif token_value == 'DICT':
                return self._parse_dict_declaration()
        
        # Variable assignment or function call
        if token_type == 'IDENTIFIER':
            # Check if it's a function call
            next_token = self._peek()
            if next_token[0] == 'SYMBOL' and next_token[1] == '(':
                return self._parse_function_call()
            else:
                return self._parse_assignment_statement()
        
        # Expression statement (like standalone function calls)
        if token_type in ['INTEGER', 'FLOAT', 'STRING', 'SYMBOL'] and token_value == '(':
            return self._parse_expression_statement()
        
        # ያልታወቀ መግለጫ - skip to next statement
        self._advance()
        return None
    
    def _parse_print_statement(self):
        """የማተም መግለጫ ማቀናበር"""
        line_num = self.current_token[2]
        column = self.current_token[3]
        self._expect('KEYWORD', 'PRINT')
        
        # የሚታተመውን ነገር ማግኘት
        value = self._parse_expression()
        
        # Optional multiple values with commas
        values = [value]
        while self.current_token[0] == 'COMMA':
            self._advance()
            values.append(self._parse_expression())
        
        # የመጨረሻ ምልክት (optional)
        if self.current_token[0] == 'SEMICOLON':
            self._advance()
        
        return {
            'type': 'print',
            'values': values if len(values) > 1 else value,
            'line': line_num,
            'column': column
        }
    
    def _parse_assignment_statement(self):
        """የመመደቢያ መግለጫ ማቀናበር"""
        line_num = self.current_token[2]
        column = self.current_token[3]
        
        # ተለዋዋጭ ስም
        var_name = self.current_token[1]
        self._expect('IDENTIFIER')
        
        # Check for compound assignment operators
        if self.current_token[0] == 'OPERATOR':
            operator = self.current_token[1]
            if operator in ['+=', '-=', '*=', '/=', '%=']:
                self._advance()
                value = self._parse_expression()
                
                if self.current_token[0] == 'SEMICOLON':
                    self._advance()
                
                return {
                    'type': 'compound_assignment',
                    'variable': var_name,
                    'operator': operator[:-1],  # Remove the '='
                    'value': value,
                    'line': line_num,
                    'column': column
                }
            elif operator == '=':
                self._advance()
                value = self._parse_expression()
                
                if self.current_token[0] == 'SEMICOLON':
                    self._advance()
                
                return {
                    'type': 'assignment',
                    'variable': var_name,
                    'value': value,
                    'line': line_num,
                    'column': column
                }
        
        raise ParseError(
            "የመመደቢያ ምልክት = ይጠበቃል",
            line_num,
            column,
            self._get_line_content(line_num)
        )
    
    def _parse_declaration_statement(self):
        """የውሂብ አይነት መግለጫ ማቀናበር"""
        line_num = self.current_token[2]
        column = self.current_token[3]
        
        # የውሂብ አይነት
        data_type = self.current_token[1]
        self._expect('KEYWORD')
        
        # ተለዋዋጭ ስም
        var_name = self.current_token[1]
        self._expect('IDENTIFIER')
        
        # ከሆነ ዋጋ (optional)
        value = None
        if self.current_token[0] == 'OPERATOR' and self.current_token[1] == '=':
            self._advance()  # = ዝለል
            value = self._parse_expression()
        
        # የመጨረሻ ምልክት
        if self.current_token[0] == 'SEMICOLON':
            self._advance()
        
        return {
            'type': 'declaration',
            'data_type': data_type,
            'variable': var_name,
            'value': value,
            'line': line_num,
            'column': column
        }
    
    def _parse_if_statement(self):
        """የሁኔታ መግለጫ ማቀናበር"""
        line_num = self.current_token[2]
        column = self.current_token[3]
        self._expect('KEYWORD', 'IF')
        
        # ሁኔታ
        condition = self._parse_expression()
        
        # የሚሰራው ክፍል
        self._expect('SYMBOL', '{')
        if_body = self._parse_block()
        self._expect('SYMBOL', '}')
        
        # አለባችሁ (else) ክፍል (optional)
        else_body = None
        if (self.current_token[0] == 'KEYWORD' and 
            self.current_token[1] == 'ELSE'):
            self._advance()  # ELSE ዝለል
            self._expect('SYMBOL', '{')
            else_body = self._parse_block()
            self._expect('SYMBOL', '}')
        
        return {
            'type': 'if',
            'condition': condition,
            'if_body': if_body,
            'else_body': else_body,
            'line': line_num,
            'column': column
        }
    
    def _parse_for_statement(self):
        """የለ loop መግለጫ ማቀናበር"""
        line_num = self.current_token[2]
        column = self.current_token[3]
        self._expect('KEYWORD', 'FOR')
        
        # Loop variable
        var_name = self.current_token[1]
        self._expect('IDENTIFIER')
        
        # Check if it's a range-based for loop
        if self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'IN':
            self._advance()  # 'IN' keyword
            start = self._parse_expression()
            self._expect('KEYWORD', 'TO')
            end = self._parse_expression()
            step = None
            
            # Optional step
            if self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'STEP':
                self._advance()
                step = self._parse_expression()
        else:
            # Traditional for loop with initialization, condition, increment
            self._expect('OPERATOR', '=')
            start = self._parse_expression()
            self._expect('SYMBOL', ';')
            condition = self._parse_expression()
            self._expect('SYMBOL', ';')
            increment = self._parse_expression()
            
            # ዑደት አካል
            self._expect('SYMBOL', '{')
            body = self._parse_block()
            self._expect('SYMBOL', '}')
            
            return {
                'type': 'for_traditional',
                'variable': var_name,
                'start': start,
                'condition': condition,
                'increment': increment,
                'body': body,
                'line': line_num,
                'column': column
            }
        
        # Range-based for loop
        self._expect('SYMBOL', '{')
        body = self._parse_block()
        self._expect('SYMBOL', '}')
        
        return {
            'type': 'for',
            'variable': var_name,
            'start': start,
            'end': end,
            'step': step,
            'body': body,
            'line': line_num,
            'column': column
        }
    
    def _parse_while_statement(self):
        """የበሚታይ loop መግለጫ ማቀናበር"""
        line_num = self.current_token[2]
        column = self.current_token[3]
        self._expect('KEYWORD', 'WHILE')
        
        condition = self._parse_expression()
        
        self._expect('SYMBOL', '{')
        body = self._parse_block()
        self._expect('SYMBOL', '}')
        
        return {
            'type': 'while',
            'condition': condition,
            'body': body,
            'line': line_num,
            'column': column
        }
    
    def _parse_function_statement(self):
        """የተግባር መግለጫ ማቀናበር"""
        line_num = self.current_token[2]
        column = self.current_token[3]
        self._expect('KEYWORD', 'FUNCTION')
        
        func_name = self.current_token[1]
        self._expect('IDENTIFIER')
        
        self._expect('SYMBOL', '(')
        
        # መለኪያዎች
        parameters = []
        if self.current_token[0] != 'SYMBOL' or self.current_token[1] != ')':
            while True:
                param_name = self.current_token[1]
                self._expect('IDENTIFIER')
                
                # Optional type annotation
                if self.current_token[0] == 'SYMBOL' and self.current_token[1] == ':':
                    self._advance()
                    param_type = self.current_token[1]
                    self._expect('KEYWORD')
                    parameters.append((param_name, param_type))
                else:
                    parameters.append((param_name, None))
                
                if self.current_token[0] == 'SYMBOL' and self.current_token[1] == ')':
                    break
                self._expect('SYMBOL', ',')
        
        self._expect('SYMBOL', ')')
        
        # Optional return type
        return_type = None
        if self.current_token[0] == 'SYMBOL' and self.current_token[1] == '->':
            self._advance()
            return_type = self.current_token[1]
            self._expect('KEYWORD')
        
        # የተግባር አካል
        self._expect('SYMBOL', '{')
        body = self._parse_block()
        self._expect('SYMBOL', '}')
        
        return {
            'type': 'function',
            'name': func_name,
            'parameters': parameters,
            'return_type': return_type,
            'body': body,
            'line': line_num,
            'column': column
        }
    
    def _parse_return_statement(self):
        """የመመለሻ መግለጫ ማቀናበር"""
        line_num = self.current_token[2]
        column = self.current_token[3]
        self._expect('KEYWORD', 'RETURN')
        
        value = None
        if self.current_token[0] != 'SEMICOLON':
            value = self._parse_expression()
        
        if self.current_token[0] == 'SEMICOLON':
            self._advance()
        
        return {
            'type': 'return',
            'value': value,
            'line': line_num,
            'column': column
        }
    
    def _parse_function_call(self):
        """የተግባር ጥሪ ማቀናበር"""
        line_num = self.current_token[2]
        column = self.current_token[3]
        func_name = self.current_token[1]
        self._expect('IDENTIFIER')
        
        self._expect('SYMBOL', '(')
        
        # ነጋሪቶች
        arguments = []
        if self.current_token[0] != 'SYMBOL' or self.current_token[1] != ')':
            while True:
                arg = self._parse_expression()
                arguments.append(arg)
                
                if self.current_token[0] == 'SYMBOL' and self.current_token[1] == ')':
                    break
                self._expect('SYMBOL', ',')
        
        self._expect('SYMBOL', ')')
        
        if self.current_token[0] == 'SEMICOLON':
            self._advance()
        
        return {
            'type': 'function_call',
            'name': func_name,
            'arguments': arguments,
            'line': line_num,
            'column': column
        }
    
    def _parse_read_statement(self):
        """የማንበብ መግለጫ ማቀናበር"""
        line_num = self.current_token[2]
        column = self.current_token[3]
        self._expect('KEYWORD', 'READ')
        
        # Optional prompt
        prompt = None
        if self.current_token[0] == 'STRING':
            prompt = self.current_token[1]
            self._advance()
        
        # Optional variable to store input
        var_name = None
        if self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'INTO':
            self._advance()
            var_name = self.current_token[1]
            self._expect('IDENTIFIER')
        
        if self.current_token[0] == 'SEMICOLON':
            self._advance()
        
        return {
            'type': 'read',
            'prompt': prompt,
            'variable': var_name,
            'line': line_num,
            'column': column
        }
    
    def _parse_try_catch_statement(self):
        """የሞክር/ያዝ መግለጫ ማቀናበር"""
        line_num = self.current_token[2]
        column = self.current_token[3]
        self._expect('KEYWORD', 'TRY')
        
        self._expect('SYMBOL', '{')
        try_body = self._parse_block()
        self._expect('SYMBOL', '}')
        
        self._expect('KEYWORD', 'CATCH')
        
        # Optional exception variable
        error_var = None
        if self.current_token[0] == 'SYMBOL' and self.current_token[1] == '(':
            self._advance()
            error_var = self.current_token[1]
            self._expect('IDENTIFIER')
            self._expect('SYMBOL', ')')
        
        self._expect('SYMBOL', '{')
        catch_body = self._parse_block()
        self._expect('SYMBOL', '}')
        
        return {
            'type': 'try_catch',
            'try_body': try_body,
            'error_var': error_var,
            'catch_body': catch_body,
            'line': line_num,
            'column': column
        }
    
    def _parse_list_declaration(self):
        """የዝርዝር መግለጫ ማቀናበር"""
        line_num = self.current_token[2]
        column = self.current_token[3]
        self._expect('KEYWORD', 'LIST')
        
        var_name = self.current_token[1]
        self._expect('IDENTIFIER')
        
        value = None
        if self.current_token[0] == 'OPERATOR' and self.current_token[1] == '=':
            self._advance()
            value = self._parse_list_literal()
        
        if self.current_token[0] == 'SEMICOLON':
            self._advance()
        
        return {
            'type': 'list_declaration',
            'variable': var_name,
            'value': value,
            'line': line_num,
            'column': column
        }
    
    def _parse_dict_declaration(self):
        """የመዝገብ መግለጫ ማቀናበር"""
        line_num = self.current_token[2]
        column = self.current_token[3]
        self._expect('KEYWORD', 'DICT')
        
        var_name = self.current_token[1]
        self._expect('IDENTIFIER')
        
        value = None
        if self.current_token[0] == 'OPERATOR' and self.current_token[1] == '=':
            self._advance()
            value = self._parse_dict_literal()
        
        if self.current_token[0] == 'SEMICOLON':
            self._advance()
        
        return {
            'type': 'dict_declaration',
            'variable': var_name,
            'value': value,
            'line': line_num,
            'column': column
        }
    
    def _parse_list_literal(self):
        """የዝርዝር ቀጥተኛ ዋጋ ማቀናበር"""
        self._expect('SYMBOL', '[')
        
        elements = []
        if self.current_token[0] != 'SYMBOL' or self.current_token[1] != ']':
            while True:
                element = self._parse_expression()
                elements.append(element)
                
                if self.current_token[0] == 'SYMBOL' and self.current_token[1] == ']':
                    break
                self._expect('SYMBOL', ',')
        
        self._expect('SYMBOL', ']')
        
        return {
            'type': 'list_literal',
            'elements': elements
        }
    
    def _parse_dict_literal(self):
        """የመዝገብ ቀጥተኛ ዋጋ ማቀናበር"""
        self._expect('SYMBOL', '{')
        
        pairs = []
        if self.current_token[0] != 'SYMBOL' or self.current_token[1] != '}':
            while True:
                key = self._parse_expression()
                self._expect('SYMBOL', ':')
                value = self._parse_expression()
                pairs.append((key, value))
                
                if self.current_token[0] == 'SYMBOL' and self.current_token[1] == '}':
                    break
                self._expect('SYMBOL', ',')
        
        self._expect('SYMBOL', '}')
        
        return {
            'type': 'dict_literal',
            'pairs': pairs
        }
    
    def _parse_block(self):
        """የኮድ ክፍል ማቀናበር"""
        statements = []
        while (self.current_token[0] != 'SYMBOL' or 
               self.current_token[1] != '}'):
            if self.current_token[0] == 'EOF':
                raise ParseError(
                    "ያልተዘጋ ኮድ ክፍል { ይጠበቃል",
                    self.current_token[2],
                    self.current_token[3]
                )
            statement = self._parse_statement()
            if statement:
                statements.append(statement)
        return statements
    
    def _parse_expression(self):
        """ሒሳባዊ መግለጫ ማቀናበር"""
        return self._parse_logical_or()
    
    def _parse_logical_or(self):
        """ወይም (OR) ኦፔሬተር ማቀናበር"""
        left = self._parse_logical_and()
        
        while (self.current_token[0] == 'OPERATOR' and 
               self.current_token[1] in ['||', 'ወይም']):
            operator = self.current_token[1]
            self._advance()
            right = self._parse_logical_and()
            
            left = {
                'type': 'binary_operation',
                'operator': 'or',
                'left': left,
                'right': right
            }
        
        return left
    
    def _parse_logical_and(self):
        """እና (AND) ኦፔሬተር ማቀናበር"""
        left = self._parse_comparison()
        
        while (self.current_token[0] == 'OPERATOR' and 
               self.current_token[1] in ['&&', 'እና']):
            operator = self.current_token[1]
            self._advance()
            right = self._parse_comparison()
            
            left = {
                'type': 'binary_operation',
                'operator': 'and',
                'left': left,
                'right': right
            }
        
        return left
    
    def _parse_comparison(self):
        """የማነፃፀሪያ መግለጫ ማቀናበር"""
        left = self._parse_addition()
        
        while (self.current_token[0] == 'OPERATOR' and 
               self.current_token[1] in ['==', '!=', '<', '>', '<=', '>=']):
            operator = self.current_token[1]
            self._advance()
            right = self._parse_addition()
            
            left = {
                'type': 'binary_operation',
                'operator': operator,
                'left': left,
                'right': right
            }
        
        return left
    
    def _parse_addition(self):
        """የመደመር/መቀነስ መግለጫ ማቀናበር"""
        left = self._parse_multiplication()
        
        while (self.current_token[0] == 'OPERATOR' and 
               self.current_token[1] in ['+', '-']):
            operator = self.current_token[1]
            self._advance()
            right = self._parse_multiplication()
            
            left = {
                'type': 'binary_operation',
                'operator': operator,
                'left': left,
                'right': right
            }
        
        return left
    
    def _parse_multiplication(self):
        """የማባዛት/ማካፈል መግለጫ ማቀናበር"""
        left = self._parse_unary()
        
        while (self.current_token[0] == 'OPERATOR' and 
               self.current_token[1] in ['*', '/', '%', '//']):
            operator = self.current_token[1]
            self._advance()
            right = self._parse_unary()
            
            left = {
                'type': 'binary_operation',
                'operator': operator,
                'left': left,
                'right': right
            }
        
        return left
    
    def _parse_unary(self):
        """የአንድነት ኦፔሬተር ማቀናበር"""
        if self.current_token[0] == 'OPERATOR' and self.current_token[1] in ['-', '!', 'አይደለም']:
            operator = self.current_token[1]
            self._advance()
            expr = self._parse_unary()
            return {
                'type': 'unary_operation',
                'operator': operator,
                'expr': expr
            }
        
        return self._parse_power()
    
    def _parse_power(self):
        """የሃይል ኦፔሬተር ማቀናበር"""
        left = self._parse_primary()
        
        if self.current_token[0] == 'OPERATOR' and self.current_token[1] == '**':
            operator = self.current_token[1]
            self._advance()
            right = self._parse_unary()  # Right-associative
            
            left = {
                'type': 'binary_operation',
                'operator': operator,
                'left': left,
                'right': right
            }
        
        return left
    
    def _parse_primary(self):
        """መሰረታዊ አካላት ማቀናበር"""
        token_type, token_value, line_num, column = self.current_token
        
        if token_type == 'INTEGER':
            self._advance()
            return {'type': 'number', 'value': token_value, 'line': line_num, 'column': column}
        
        elif token_type == 'FLOAT':
            self._advance()
            return {'type': 'float', 'value': token_value, 'line': line_num, 'column': column}
        
        elif token_type == 'STRING':
            self._advance()
            return {'type': 'string', 'value': token_value, 'line': line_num, 'column': column}
        
        elif token_type == 'IDENTIFIER':
            # Check if it's a function call
            if self.current_token[0] == 'SYMBOL' and self.current_token[1] == '(':
                return self._parse_function_call()
            self._advance()
            return {'type': 'variable', 'name': token_value, 'line': line_num, 'column': column}
        
        elif token_type == 'KEYWORD' and token_value in ['TRUE', 'FALSE']:
            self._advance()
            return {'type': 'boolean', 'value': token_value == 'TRUE', 'line': line_num, 'column': column}
        
        elif token_type == 'SYMBOL' and token_value == '[':
            return self._parse_list_literal()
        
        elif token_type == 'SYMBOL' and token_value == '(':
            self._advance()
            expr = self._parse_expression()
            self._expect('SYMBOL', ')')
            return expr
        
        elif token_type == 'SYMBOL' and token_value == '{':
            return self._parse_dict_literal()
        
        else:
            raise ParseError(
                f"ያልተጠበቀ አገላለጽ: {token_value}",
                line_num,
                column,
                self._get_line_content(line_num)
            )
    
    def _parse_expression_statement(self):
        """የመግለጫ ዓይነት መግለጫ ማቀናበር"""
        expr = self._parse_expression()
        
        if self.current_token[0] == 'SEMICOLON':
            self._advance()
        
        return {
            'type': 'expression_statement',
            'expression': expr
        }
    
    def _get_line_content(self, line_num):
        """የተወሰነ መስመር ይዘት ማግኘት"""
        if hasattr(self, 'lexer') and hasattr(self.lexer, 'get_line_content'):
            return self.lexer.get_line_content(line_num)
        return ""
