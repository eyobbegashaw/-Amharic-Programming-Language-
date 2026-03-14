"""
ሌክሳር - የአማርኛ ፕሮግራሚንግ ቋንቋ የመጀመሪያ ደረጃ ማቀነባበሪያ
ሚና: ፅሁፍን ወደ ማይቀየሩ ክፍሎች (ቶከኖች) መከፋፈል
"""

class Lexer:
    def __init__(self):
        # የአማርኛ ቁልፍ ቃላት
        self.keywords = {
            # መሰረታዊ ቁልፍ ቃላት
            'ማተም': 'PRINT',
            'ከ': 'IF',
            'አለባችሁ': 'ELSE',
            'ለ': 'FOR',
            'በሚታይ': 'WHILE',
            
            # የውሂብ አይነቶች
            'የቁጥር': 'INT',
            'የጽሁፍ': 'STRING',
            'እውነት': 'TRUE',
            'ሐሰት': 'FALSE',
            
            # ተግባራት
            'ስራ': 'FUNCTION',
            'መመለስ': 'RETURN',
            
            # መሰረታዊ ተግባራት
            'አንብብ': 'READ',
            'ደብቅ': 'IMPORT',
            
            # የመቆጣጠሪያ ፍሰት
            'ተው': 'BREAK',
            'ቀጥል': 'CONTINUE',
            
            # አዲስ ቁልፍ ቃላት
            'ሞክር': 'TRY',
            'ያዝ': 'CATCH',
            'ዝርዝር': 'LIST',
            'መዝገብ': 'DICT',
            'ርዝመት': 'LENGTH',
            'አይነት': 'TYPE_OF',
        }
        
        # ኦፔሬተሮች
        self.operators = {
            '+': 'PLUS',
            '-': 'MINUS',
            '*': 'MULTIPLY',
            '/': 'DIVIDE',
            '=': 'EQUALS',
            '==': 'EQUALS_EQUALS',
            '!=': 'NOT_EQUALS',
            '<': 'LESS_THAN',
            '>': 'GREATER_THAN',
            '<=': 'LESS_EQUAL',
            '>=': 'GREATER_EQUAL',
            '&&': 'AND',
            '||': 'OR',
            '!': 'NOT',
            '&': 'BIT_AND',
            '|': 'BIT_OR',
            '^': 'BIT_XOR',
            '<<': 'LEFT_SHIFT',
            '>>': 'RIGHT_SHIFT',
            '%': 'MODULO',
            '**': 'POWER',
            '//': 'FLOOR_DIVIDE',
            '+=': 'PLUS_EQUALS',
            '-=': 'MINUS_EQUALS',
            '*=': 'MULTIPLY_EQUALS',
            '/=': 'DIVIDE_EQUALS',
        }
        
        # ሌሎች ምልክቶች
        self.symbols = {
            '(': 'LEFT_PAREN',
            ')': 'RIGHT_PAREN',
            '{': 'LEFT_BRACE',
            '}': 'RIGHT_BRACE',
            '[': 'LEFT_BRACKET',
            ']': 'RIGHT_BRACKET',
            ',': 'COMMA',
            ';': 'SEMICOLON',
            ':': 'COLON',
            '.': 'DOT',
            '->': 'ARROW',
        }
    
    def tokenize(self, code):
        """ፅሁፍን ወደ ቶከን መቀየር"""
        tokens = []
        current_token = ''
        line_num = 1
        pos = 0
        column = 1
        self.code_lines = code.split('\n')
        
        while pos < len(code):
            char = code[pos]
            start_column = column
            
            # አዲስ መስመር
            if char == '\n':
                line_num += 1
                column = 1
                pos += 1
                continue
            
            # ባዶ ቦታ (የቶከን መጨረሻ)
            if char.isspace():
                if current_token:
                    tokens.append(self._create_token(current_token, line_num, start_column))
                    current_token = ''
                column += 1
                pos += 1
                continue
            
            # ኦፔሬተር (ባለ ሁለት ምልክት ከሆነ መፈተሽ)
            if char in '+-*/=!<>&|%':
                if current_token:
                    tokens.append(self._create_token(current_token, line_num, start_column))
                    current_token = ''
                
                # ለባለ ሁለት ምልክት ኦፔሬተር መፈተሽ
                if pos + 1 < len(code):
                    two_char = char + code[pos + 1]
                    three_char = two_char + code[pos + 2] if pos + 2 < len(code) else ''
                    
                    if three_char in self.operators:
                        tokens.append(('OPERATOR', three_char, line_num, column))
                        pos += 3
                        column += 3
                        continue
                    elif two_char in self.operators:
                        tokens.append(('OPERATOR', two_char, line_num, column))
                        pos += 2
                        column += 2
                        continue
                
                tokens.append(('OPERATOR', char, line_num, column))
                pos += 1
                column += 1
                continue
            
            # ምልክቶች
            if char in self.symbols:
                if current_token:
                    tokens.append(self._create_token(current_token, line_num, start_column))
                    current_token = ''
                
                # Check for two-character symbols
                if pos + 1 < len(code) and char + code[pos + 1] in self.symbols:
                    two_char = char + code[pos + 1]
                    tokens.append(('SYMBOL', two_char, line_num, column))
                    pos += 2
                    column += 2
                else:
                    tokens.append(('SYMBOL', char, line_num, column))
                    pos += 1
                    column += 1
                continue
            
            # ገለልተኛ ጽሁፍ (በ" " ወይም ' ')
            if char == '"' or char == "'":
                if current_token:
                    tokens.append(self._create_token(current_token, line_num, start_column))
                    current_token = ''
                
                quote_char = char
                start_pos = pos
                pos += 1
                column += 1
                string_content = ''
                escaped = False
                
                # የጽሁፍ መጨረሻ እስኪገኝ ድረስ
                while pos < len(code):
                    if not escaped and code[pos] == quote_char:
                        pos += 1
                        column += 1
                        break
                    
                    if not escaped and code[pos] == '\\':
                        escaped = True
                        pos += 1
                        column += 1
                        continue
                    
                    string_content += code[pos]
                    escaped = False
                    pos += 1
                    column += 1
                else:
                    raise SyntaxError(f"ላልተጠናቀቀ ጽሁፍ በምስር {line_num}, አምድ {column}")
                
                tokens.append(('STRING', string_content, line_num, start_column))
                continue
            
            # ቁጥሮች
            if char.isdigit() or (char == '.' and pos + 1 < len(code) and code[pos + 1].isdigit()):
                current_token += char
                pos += 1
                column += 1
                
                # ነጠላ ነጥብ ለአስርዮሽ ቁጥሮች
                if char == '.':
                    while pos < len(code) and code[pos].isdigit():
                        current_token += code[pos]
                        pos += 1
                        column += 1
                else:
                    # ሙሉ ቁጥር ማግኘት
                    while pos < len(code) and (code[pos].isdigit() or code[pos] == '.'):
                        if code[pos] == '.':
                            # ከአስርዮሽ በፊት ነጥብ ካለ ማረጋገጥ
                            if '.' in current_token:
                                break
                        current_token += code[pos]
                        pos += 1
                        column += 1
                
                continue
            
            # ፊደላት (አማርኛ ጨምሮ)
            if char.isalpha() or char == '_' or self._is_amharic_char(char):
                current_token += char
                pos += 1
                column += 1
                
                # ሙሉ ቃል ማግኘት
                while pos < len(code) and (code[pos].isalnum() or 
                                           code[pos] == '_' or 
                                           self._is_amharic_char(code[pos])):
                    current_token += code[pos]
                    pos += 1
                    column += 1
                
                continue
            
            # ኮሜንት (ማስተባበር)
            if char == '#':
                # እስከ መስመር መጨረሻ ድረስ ዝለል
                while pos < len(code) and code[pos] != '\n':
                    pos += 1
                    column += 1
                continue
            
            # ሌላ ማንኛውም
            current_token += char
            pos += 1
            column += 1
        
        # የመጨረሻ ቶከን
        if current_token:
            tokens.append(self._create_token(current_token, line_num, column))
        
        # የመጨረሻ ምልክት
        tokens.append(('EOF', '', line_num, column))
        
        return tokens
    
    def _create_token(self, token_text, line_num, column):
        """የቶከን አይነት መወሰን"""
        # ቁልፍ ቃል መሆኑን ይፈትሽ
        if token_text in self.keywords:
            return ('KEYWORD', self.keywords[token_text], line_num, column)
        
        # ኦፔሬተር መሆኑን ይፈትሽ
        if token_text in self.operators:
            return ('OPERATOR', token_text, line_num, column)
        
        # ቁጥር መሆኑን ይፈትሽ
        if self._is_number(token_text):
            if '.' in token_text:
                return ('FLOAT', float(token_text), line_num, column)
            else:
                return ('INTEGER', int(token_text), line_num, column)
        
        # ተለዋዋጭ ስም መሆኑን ይፈትሽ
        if self._is_valid_identifier(token_text):
            return ('IDENTIFIER', token_text, line_num, column)
        
        # ያልታወቀ
        return ('UNKNOWN', token_text, line_num, column)
    
    def _is_amharic_char(self, char):
        """አማርኛ ፊደል መሆኑን ይፈትሽ"""
        # የአማርኛ የዩኒኮድ ክልል
        return ('\u1200' <= char <= '\u137F')
    
    def _is_number(self, text):
        """ቁጥር መሆኑን ይፈትሽ"""
        try:
            if '.' in text:
                float(text)
            else:
                int(text)
            return True
        except ValueError:
            return False
    
    def _is_valid_identifier(self, text):
        """የተለዋዋጭ ስም መሆኑን ይፈትሽ"""
        if not text:
            return False
        
        # የመጀመሪያ ፊደል ፊደል ወይም አማርኛ መሆን አለበት
        first_char = text[0]
        if not (first_char.isalpha() or first_char == '_' or 
                self._is_amharic_char(first_char)):
            return False
        
        # ሁሉም ቁምፊዎች ትክክለኛ መሆን አለባቸው
        for char in text[1:]:
            if not (char.isalnum() or char == '_' or 
                    self._is_amharic_char(char)):
                return False
        
        return True
    
    def get_line_content(self, line_num):
        """የተወሰነ መስመር ይዘት ማግኘት"""
        if hasattr(self, 'code_lines') and 0 < line_num <= len(self.code_lines):
            return self.code_lines[line_num - 1]
        return ""
