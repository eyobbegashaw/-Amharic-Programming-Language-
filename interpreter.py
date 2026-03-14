"""
ኢንተርፕሪተር - የአማርኛ ፕሮግራሚንግ ቋንቋ ሶስተኛ ደረጃ ማቀነባበሪያ
ሚና: የኮድ ዛፍን (AST) ማስፈጸም
"""

import sys
import traceback

class RuntimeError(Exception):
    def __init__(self, message, node=None):
        self.message = message
        self.node = node
        self.line_num = node.get('line', -1) if node else -1
        self.column = node.get('column', -1) if node else -1
        super().__init__(self._format_message())
    
    def _format_message(self):
        """ዝርዝር የስህተት መልዕክት ማዘጋጀት"""
        location = f"በምስር {self.line_num}"
        if self.column != -1:
            location += f", አምድ {self.column}"
        return f"❌ {self.message} {location}"

class Return(Exception):
    """የተግባር መመለሻ ልዩ ሁኔታ"""
    def __init__(self, value):
        self.value = value

class Break(Exception):
    """የተው መግለጫ ልዩ ሁኔታ"""
    pass

class Continue(Exception):
    """የቀጥል መግለጫ ልዩ ሁኔታ"""
    pass

class Interpreter:
    def __init__(self):
        self.variables = {}  # ተለዋዋጮች
        self.functions = {}  # ተግባራት
        self.scopes = [{}]   # የተለዋዋጭ ክልል
        self.break_flag = False
        self.continue_flag = False
        self.return_flag = False
        self.call_stack = []  # For better error tracebacks
        
    def execute(self, ast):
        """የኮድ ዛፍ ማስፈጸም"""
        try:
            for node in ast:
                self._execute_node(node)
        except Return as r:
            # Return outside function
            raise RuntimeError("መመለስ ከተግባር ውጭ አይፈቀድም", node)
        except Break:
            raise RuntimeError("ተው ከዑደት ውጭ አይፈቀድም", node)
        except Continue:
            raise RuntimeError("ቀጥል ከዑደት ውጭ አይፈቀድም", node)
    
    def _execute_node(self, node):
        """አንድ ኖድ ማስፈጸም"""
        if node is None:
            return None
        
        # Add to call stack for traceback
        if 'line' in node:
            self.call_stack.append(node)
        
        try:
            node_type = node['type']
            
            if node_type == 'print':
                result = self._execute_print(node)
            elif node_type == 'assignment':
                result = self._execute_assignment(node)
            elif node_type == 'compound_assignment':
                result = self._execute_compound_assignment(node)
            elif node_type == 'declaration':
                result = self._execute_declaration(node)
            elif node_type == 'if':
                result = self._execute_if(node)
            elif node_type == 'for':
                result = self._execute_for(node)
            elif node_type == 'for_traditional':
                result = self._execute_for_traditional(node)
            elif node_type == 'while':
                result = self._execute_while(node)
            elif node_type == 'function':
                result = self._execute_function_declaration(node)
            elif node_type == 'function_call':
                result = self._execute_function_call(node)
            elif node_type == 'return':
                result = self._execute_return(node)
            elif node_type == 'read':
                result = self._execute_read(node)
            elif node_type == 'try_catch':
                result = self._execute_try_catch(node)
            elif node_type == 'list_declaration':
                result = self._execute_list_declaration(node)
            elif node_type == 'dict_declaration':
                result = self._execute_dict_declaration(node)
            elif node_type == 'list_literal':
                result = self._parse_list_literal(node)
            elif node_type == 'dict_literal':
                result = self._parse_dict_literal(node)
            elif node_type == 'binary_operation':
                result = self._execute_binary_operation(node)
            elif node_type == 'unary_operation':
                result = self._execute_unary_operation(node)
            elif node_type == 'expression_statement':
                result = self._evaluate_expression(node['expression'])
            elif node_type in ['number', 'float', 'string', 'boolean']:
                result = node['value']
            elif node_type == 'variable':
                result = self._get_variable(node['name'])
            else:
                raise RuntimeError(f"ያልታወቀ ኖድ አይነት: {node_type}", node)
            
            # Remove from call stack
            if 'line' in node:
                self.call_stack.pop()
            
            return result
            
        except Return as r:
            # Propagate return
            if 'line' in node:
                self.call_stack.pop()
            raise r
        except Break as b:
            if 'line' in node:
                self.call_stack.pop()
            raise b
        except Continue as c:
            if 'line' in node:
                self.call_stack.pop()
            raise c
        except Exception as e:
            # Add context to error
            if 'line' in node:
                self.call_stack.pop()
            
            if not isinstance(e, RuntimeError):
                # Convert to our RuntimeError with context
                raise RuntimeError(str(e), node)
            raise e
    
    def _execute_print(self, node):
        """የማተም መግለጫ ማስፈጸም"""
        values = node.get('values', node.get('value'))
        
        if isinstance(values, list):
            # Print multiple values
            output = []
            for val in values:
                evaluated = self._evaluate_expression(val)
                output.append(str(evaluated))
            print(' '.join(output))
        else:
            # Single value
            value = self._evaluate_expression(values)
            print(value)
    
    def _execute_assignment(self, node):
        """የመመደቢያ መግለጫ ማስፈጸም"""
        var_name = node['variable']
        value = self._evaluate_expression(node['value'])
        
        # Type checking if variable was declared with type
        if var_name in self.variables:
            existing_value = self._get_variable(var_name)
            if isinstance(existing_value, int) and not isinstance(value, (int, float)):
                raise TypeError(f"{var_name} የቁጥር መሆን አለበት", node)
            elif isinstance(existing_value, str) and not isinstance(value, str):
                raise TypeError(f"{var_name} የጽሁፍ መሆን አለበት", node)
            elif isinstance(existing_value, list) and not isinstance(value, list):
                raise TypeError(f"{var_name} የዝርዝር መሆን አለበት", node)
        
        self._set_variable(var_name, value)
    
    def _execute_compound_assignment(self, node):
        """የተደባለቀ መመደቢያ ማስፈጸም (+=, -=, etc.)"""
        var_name = node['variable']
        operator = node['operator']
        value = self._evaluate_expression(node['value'])
        
        current = self._get_variable(var_name)
        
        if operator == '+':
            result = current + value
        elif operator == '-':
            result = current - value
        elif operator == '*':
            result = current * value
        elif operator == '/':
            if value == 0:
                raise ZeroDivisionError("በዜሮ መከፋፈል አይቻልም", node)
            result = current / value
        elif operator == '%':
            result = current % value
        else:
            raise RuntimeError(f"ያልታወቀ ድብልቅ ኦፔሬተር: {operator}", node)
        
        self._set_variable(var_name, result)
    
    def _execute_declaration(self, node):
        """የውሂብ አይነት መግለጫ ማስፈጸም"""
        var_name = node['variable']
        data_type = node['data_type']
        
        # ከሆነ ዋጋ መመደብ
        if node['value']:
            value = self._evaluate_expression(node['value'])
            # የውሂብ አይነት ማረጋገጫ
            if data_type == 'INT':
                if not isinstance(value, (int, float)):
                    raise TypeError(f"{var_name} የቁጥር መሆን አለበት", node)
                value = int(value)  # Convert float to int if needed
            elif data_type == 'STRING' and not isinstance(value, str):
                raise TypeError(f"{var_name} የጽሁፍ መሆን አለበት", node)
        else:
            # ነባሪ ዋጋ
            value = 0 if data_type == 'INT' else ""
        
        self._set_variable(var_name, value)
    
    def _execute_if(self, node):
        """የሁኔታ መግለጫ ማስፈጸም"""
        condition = self._evaluate_expression(node['condition'])
        
        if condition:
            # አዲስ ክልል መፍጠር
            self.scopes.append({})
            try:
                for statement in node['if_body']:
                    self._execute_node(statement)
            finally:
                self.scopes.pop()
        elif node.get('else_body'):
            # አለባችሁ ክፍል
            self.scopes.append({})
            try:
                for statement in node['else_body']:
                    self._execute_node(statement)
            finally:
                self.scopes.pop()
    
    def _execute_for(self, node):
        """የለ loop ማስፈጸም (range-based)"""
        var_name = node['variable']
        start = self._evaluate_expression(node['start'])
        end = self._evaluate_expression(node['end'])
        step = node.get('step')
        if step:
            step = self._evaluate_expression(step)
        else:
            step = 1 if start <= end else -1
        
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
            raise TypeError("የለ loop ቁጥር ይፈልጋል", node)
        
        start = int(start)
        end = int(end)
        step = int(step) if isinstance(step, (int, float)) else 1
        
        # አዲስ ክልል ለloop
        self.scopes.append({})
        
        try:
            if step > 0:
                i = start
                while i <= end:
                    # Check for break/continue
                    if self.break_flag:
                        self.break_flag = False
                        break
                    
                    if self.continue_flag:
                        self.continue_flag = False
                        i += step
                        continue
                    
                    # የloop ተለዋዋጭ መመደብ
                    self._set_variable(var_name, i)
                    
                    # loop አካል ማስፈጸም
                    try:
                        for statement in node['body']:
                            self._execute_node(statement)
                    except Break:
                        self.break_flag = True
                        break
                    except Continue:
                        self.continue_flag = True
                    
                    i += step
            else:
                i = start
                while i >= end:
                    if self.break_flag:
                        self.break_flag = False
                        break
                    
                    if self.continue_flag:
                        self.continue_flag = False
                        i += step
                        continue
                    
                    self._set_variable(var_name, i)
                    
                    try:
                        for statement in node['body']:
                            self._execute_node(statement)
                    except Break:
                        self.break_flag = True
                        break
                    except Continue:
                        self.continue_flag = True
                    
                    i += step
        finally:
            self.scopes.pop()
            self.break_flag = False
            self.continue_flag = False
    
    def _execute_for_traditional(self, node):
        """የለ loop ማስፈጸም (traditional C-style)"""
        var_name = node['variable']
        
        # አዲስ ክልል ለloop
        self.scopes.append({})
        
        try:
            # Initialize
            self._set_variable(var_name, self._evaluate_expression(node['start']))
            
            while self._evaluate_expression(node['condition']):
                # Check for break/continue
                if self.break_flag:
                    self.break_flag = False
                    break
                
                if self.continue_flag:
                    self.continue_flag = False
                    # Execute increment
                    self._evaluate_expression(node['increment'])
                    continue
                
                # loop አካል ማስፈጸም
                try:
                    for statement in node['body']:
                        self._execute_node(statement)
                except Break:
                    self.break_flag = True
                    break
                except Continue:
                    self.continue_flag = True
                
                # Increment
                self._evaluate_expression(node['increment'])
        finally:
            self.scopes.pop()
            self.break_flag = False
            self.continue_flag = False
    
    def _execute_while(self, node):
        """የበሚታይ loop ማስፈጸም"""
        # አዲስ ክልል ለloop
        self.scopes.append({})
        
        try:
            while self._evaluate_expression(node['condition']):
                if self.break_flag:
                    self.break_flag = False
                    break
                
                if self.continue_flag:
                    self.continue_flag = False
                    continue
                
                try:
                    for statement in node['body']:
                        self._execute_node(statement)
                except Break:
                    self.break_flag = True
                    break
                except Continue:
                    self.continue_flag = True
        finally:
            self.scopes.pop()
            self.break_flag = False
            self.continue_flag = False
    
    def _execute_function_declaration(self, node):
        """የተግባር መግለጫ ማስፈጸም"""
        func_name = node['name']
        self.functions[func_name] = node
    
    def _execute_function_call(self, node):
        """የተግባር ጥሪ ማስፈጸም"""
        func_name = node['name']
        
        # Check if it's a built-in function
        if func_name in self._built_in_functions():
            return self._call_built_in(func_name, node)
        
        # Check if function exists
        if func_name not in self.functions:
            raise NameError(f"ተግባር '{func_name}' አልተገኘም", node)
        
        func = self.functions[func_name]
        
        # Evaluate arguments
        args = [self._evaluate_expression(arg) for arg in node['arguments']]
        
        # Check parameter count
        if len(args) != len(func['parameters']):
            raise TypeError(
                f"ተግባር '{func_name}' {len(func['parameters'])} ነጋሪት ይፈልጋል, "
                f"{len(args)} ተሰጥቷል",
                node
            )
        
        # Create new scope for function
        self.scopes.append({})
        
        # Bind parameters
        for (param_name, param_type), arg_value in zip(func['parameters'], args):
            # Type checking if specified
            if param_type == 'INT' and not isinstance(arg_value, (int, float)):
                raise TypeError(f"መለኪያ '{param_name}' የቁጥር መሆን አለበት", node)
            elif param_type == 'STRING' and not isinstance(arg_value, str):
                raise TypeError(f"መለኪያ '{param_name}' የጽሁፍ መሆን አለበት", node)
            
            self._set_variable(param_name, arg_value)
        
        try:
            # Execute function body
            for statement in func['body']:
                self._execute_node(statement)
        except Return as r:
            # Function returned a value
            return r.value
        finally:
            # Remove function scope
            self.scopes.pop()
        
        # If no return statement, return None
        return None
    
    def _built_in_functions(self):
        """ዝግጁ የሆኑ ተግባራት"""
        return {
            'ርዝመት': self._builtin_length,
            'አይነት': self._builtin_type,
            'ቁጥር': self._builtin_int,
            'ጽሁፍ': self._builtin_str,
        }
    
    def _call_built_in(self, func_name, node):
        """ዝግጁ ተግባር ማስፈጸም"""
        args = [self._evaluate_expression(arg) for arg in node['arguments']]
        
        if func_name == 'ርዝመት':
            if len(args) != 1:
                raise TypeError("ርዝመት 1 ነጋሪት ይፈልጋል", node)
            return self._builtin_length(args[0])
        
        elif func_name == 'አይነት':
            if len(args) != 1:
                raise TypeError("አይነት 1 ነጋሪት ይፈልጋል", node)
            return self._builtin_type(args[0])
        
        elif func_name == 'ቁጥር':
            if len(args) != 1:
                raise TypeError("ቁጥር 1 ነጋሪት ይፈልጋል", node)
            return self._builtin_int(args[0])
        
        elif func_name == 'ጽሁፍ':
            if len(args) != 1:
                raise TypeError("ጽሁፍ 1 ነጋሪት ይፈልጋል", node)
            return self._builtin_str(args[0])
    
    def _builtin_length(self, obj):
        """የዝርዝር ወይም የጽሁፍ ርዝመት መመለስ"""
        if isinstance(obj, (list, dict, str)):
            return len(obj)
        raise TypeError(f"ርዝመት ለ{type(obj).__name__} አይሰራም")
    
    def _builtin_type(self, obj):
        """የውሂብ አይነት መመለስ"""
        if isinstance(obj, int):
            return "ቁጥር"
        elif isinstance(obj, float):
            return "አስርዮሽ"
        elif isinstance(obj, str):
            return "ጽሁፍ"
        elif isinstance(obj, bool):
            return "እሴት"
        elif isinstance(obj, list):
            return "ዝርዝር"
        elif isinstance(obj, dict):
            return "መዝገብ"
        return "ያልታወቀ"
    
    def _builtin_int(self, obj):
        """ወደ ቁጥር መቀየር"""
        try:
            return int(obj)
        except (ValueError, TypeError):
            raise TypeError(f"'{obj}' ወደ ቁጥር መቀየር አይቻልም")
    
    def _builtin_str(self, obj):
        """ወደ ጽሁፍ መቀየር"""
        return str(obj)
    
    def _execute_return(self, node):
        """የመመለሻ መግለጫ ማስፈጸም"""
        value = None
        if node['value']:
            value = self._evaluate_expression(node['value'])
        raise Return(value)
    
    def _execute_read(self, node):
        """የማንበብ መግለጫ ማስፈጸም"""
        prompt = node.get('prompt')
        var_name = node.get('variable')
        
        if prompt:
            user_input = input(prompt + " ")
        else:
            user_input = input()
        
        # Try to convert to number if possible
        try:
            if '.' in user_input:
                value = float(user_input)
            else:
                value = int(user_input)
        except ValueError:
            value = user_input
        
        if var_name:
            self._set_variable(var_name, value)
        
        return value
    
    def _execute_try_catch(self, node):
        """የሞክር/ያዝ መግለጫ ማስፈጸም"""
        try:
            self.scopes.append({})
            for statement in node['try_body']:
                self._execute_node(statement)
            self.scopes.pop()
        except Exception as e:
            self.scopes.pop()
            # Enter catch block
            self.scopes.append({})
            
            # If there's an error variable, bind the exception
            if node.get('error_var'):
                self._set_variable(node['error_var'], str(e))
            
            for statement in node['catch_body']:
                self._execute_node(statement)
            
            self.scopes.pop()
    
    def _execute_list_declaration(self, node):
        """የዝርዝር መግለጫ ማስፈጸም"""
        var_name = node['variable']
        
        if node['value']:
            value = self._evaluate_expression(node['value'])
            if not isinstance(value, list):
                value = [value]  # Convert to list if single value
        else:
            value = []
        
        self._set_variable(var_name, value)
    
    def _execute_dict_declaration(self, node):
        """የመዝገብ መግለጫ ማስፈጸም"""
        var_name = node['variable']
        
        if node['value']:
            value = self._evaluate_expression(node['value'])
            if not isinstance(value, dict):
                raise TypeError(f"{var_name} የመዝገብ መሆን አለበት", node)
        else:
            value = {}
        
        self._set_variable(var_name, value)
    
    def _parse_list_literal(self, node):
        """የዝርዝር ቀጥተኛ ዋጋ መተርጎም"""
        elements = []
        for elem in node['elements']:
            elements.append(self._evaluate_expression(elem))
        return elements
    
    def _parse_dict_literal(self, node):
        """የመዝገብ ቀጥተኛ ዋጋ መተርጎም"""
        result = {}
        for key_node, value_node in node['pairs']:
            key = self._evaluate_expression(key_node)
            value = self._evaluate_expression(value_node)
            
            # Only strings and numbers can be keys
            if not isinstance(key, (str, int, float)):
                raise TypeError(f"የመዝገብ ቁልፍ ጽሁፍ ወይም ቁጥር መሆን አለበት: {key}")
            
            result[key] = value
        
        return result
    
    def _execute_binary_operation(self, node):
        """የሂሳብ ስራ ማስፈጸም"""
        left = self._evaluate_expression(node['left'])
        right = self._evaluate_expression(node['right'])
        operator = node['operator']
        
        # Handle logical operators
        if operator in ['and', '&&', 'እና']:
            return self._to_boolean(left) and self._to_boolean(right)
        elif operator in ['or', '||', 'ወይም']:
            return self._to_boolean(left) or self._to_boolean(right)
        
        # Handle list indexing
        if operator == '[]' or (isinstance(left, list) and operator == '['):
            if not isinstance(right, int):
                raise TypeError(f"የዝርዝር ቁጥር ቁጥር መሆን አለበት: {right}", node)
            
            if right < 0 or right >= len(left):
                raise IndexError(f"የዝርዝር ቁጥር ከወሰን ውጭ: {right}", node)
            
            return left[right]
        
        # የሂሳብ ስራዎች
        if operator == '+':
            # ጽሁፍ ተጣምሮ
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            if right == 0:
                raise ZeroDivisionError("በዜሮ መከፋፈል አይቻልም", node)
            return left / right
        elif operator == '%':
            if right == 0:
                raise ZeroDivisionError("በዜሮ ማባዛት አይቻልም", node)
            return left % right
        elif operator == '//':
            if right == 0:
                raise ZeroDivisionError("በዜሮ መከፋፈል አይቻልም", node)
            return left // right
        elif operator == '**':
            return left ** right
        
        # የማነፃፀሪያ ስራዎች
        elif operator == '==':
            return left == right
        elif operator == '!=':
            return left != right
        elif operator == '<':
            return left < right
        elif operator == '>':
            return left > right
        elif operator == '<=':
            return left <= right
        elif operator == '>=':
            return left >= right
        
        else:
            raise RuntimeError(f"ያልታወቀ ኦፔሬተር: {operator}", node)
    
    def _execute_unary_operation(self, node):
        """የአንድነት ኦፔሬተር ማስፈጸም"""
        expr = self._evaluate_expression(node['expr'])
        operator = node['operator']
        
        if operator == '-':
            return -expr
        elif operator in ['!', 'አይደለም']:
            return not self._to_boolean(expr)
        else:
            raise RuntimeError(f"ያልታወቀ አንድነት ኦፔሬተር: {operator}", node)
    
    def _to_boolean(self, value):
        """ወደ እውነት/ሐሰት መቀየር"""
        if isinstance(value, bool):
            return value
        if value is None:
            return False
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return len(value) > 0
        if isinstance(value, (list, dict)):
            return len(value) > 0
        return True
    
    def _evaluate_expression(self, expr):
        """ሒሳባዊ መግለጫ ማስላት"""
        if expr is None:
            return None
        
        if isinstance(expr, dict):
            return self._execute_node(expr)
        else:
            return expr
    
    def _get_variable(self, name):
        """ተለዋዋጭ ዋጋ ማግኘት"""
        # ከአሁኑ ክልል ጀምሮ እስከ ሁሉ ክልል ድረስ መፈለግ
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        
        # ከግለሰባዊ ተለዋዋጭ መፈለግ
        if name in self.variables:
            return self.variables[name]
        
        # Check built-in functions
        if name in self._built_in_functions():
            return self._built_in_functions()[name]
        
        raise NameError(f"ተለዋዋጭ '{name}' አልተገኘም")
    
    def _set_variable(self, name, value):
        """ተለዋዋጭ ዋጋ መመደብ"""
        # አሁን ባለው ክልል ላይ መፃፍ
        self.scopes[-1][name] = value
        
        # እንዲሁም በግለሰባዊ ተለዋዋጭ ውስጥ (ለመድገም)
        self.variables[name] = value
    
    def get_call_stack(self):
        """የጥሪ ተዋረድ ማግኘት"""
        stack = []
        for node in self.call_stack:
            node_type = node.get('type', 'unknown')
            if node_type == 'function_call':
                stack.append(f"  በተግባር '{node['name']}' ውስጥ በምስር {node.get('line', -1)}")
            elif node_type == 'function':
                stack.append(f"  በተግባር '{node['name']}' ውስጥ በምስር {node.get('line', -1)}")
            else:
                stack.append(f"  በምስር {node.get('line', -1)}")
        return stack
