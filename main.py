#!/usr/bin/env python3
"""
ዋና የአማርኛ ፕሮግራሚንግ ቋንቋ ፕሮግራም
"""

import sys
import os
import readline  # For command history in interactive mode
import json
from lexer import Lexer
from parser import Parser, ParseError
from interpreter import Interpreter, RuntimeError, Return, Break, Continue

class AmharicProgrammingLanguage:
    def __init__(self):
        self.lexer = Lexer()
        self.parser = None
        self.interpreter = Interpreter()
        self.debug = False
        self.history_file = os.path.expanduser("~/.amharic_history")
        self._setup_history()
    
    def _setup_history(self):
        """የትዕዛዝ ታሪክ ማዘጋጀት"""
        try:
            readline.read_history_file(self.history_file)
        except FileNotFoundError:
            pass
        readline.set_history_length(1000)
    
    def _save_history(self):
        """የትዕዛዝ ታሪክ ማስቀመጥ"""
        try:
            readline.write_history_file(self.history_file)
        except:
            pass
    
    def run(self, code, filename="<stdin>"):
        """ኮድ ማስኬድ"""
        try:
            # 1. ቶከን መፍጠር
            tokens = self.lexer.tokenize(code)
            
            if self.debug:
                print("\n🔤 ቶከኖች:")
                for token in tokens:
                    print(f"  {token}")
                print()
            
            # 2. የኮድ ዛፍ መገንባት
            self.parser = Parser(tokens)
            # Pass lexer to parser for better error messages
            self.parser.lexer = self.lexer
            ast = self.parser.parse()
            
            if self.debug:
                print("🌳 የኮድ ዛፍ:")
                print(json.dumps(ast, indent=2, ensure_ascii=False))
                print()
            
            # 3. ኮድ ማስፈጸም
            if not self.debug:
                print("🚀 ውጤት:")
                print("-" * 30)
            
            self.interpreter.execute(ast)
            
            if not self.debug:
                print("-" * 30)
            
            return True
            
        except ParseError as e:
            print(f"\n❌ {e}")
            if self.debug:
                print("\n📚 የጥሪ ተዋረድ:")
                for frame in self.interpreter.get_call_stack():
                    print(frame)
            return False
        except RuntimeError as e:
            print(f"\n❌ {e}")
            if self.debug:
                print("\n📚 የጥሪ ተዋረድ:")
                for frame in self.interpreter.get_call_stack():
                    print(frame)
            return False
        except NameError as e:
            print(f"\n❌ {e}")
            return False
        except TypeError as e:
            print(f"\n❌ {e}")
            return False
        except ZeroDivisionError as e:
            print(f"\n❌ {e}")
            return False
        except Exception as e:
            print(f"\n❌ ያልተጠበቀ ስህተት በ{filename}: {e}")
            if self.debug:
                import traceback
                traceback.print_exc()
                print("\n📚 የጥሪ ተዋረድ:")
                for frame in self.interpreter.get_call_stack():
                    print(frame)
            return False
    
    def run_file(self, filename):
        """ከፋይል ኮድ ማስኬድ"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                code = f.read()
            
            print(f"📂 ፋይል በማስኬድ ላይ: {filename}")
            return self.run(code, filename)
            
        except FileNotFoundError:
            print(f"❌ ፋይል አልተገኘም: {filename}")
            return False
        except UnicodeDecodeError:
            print(f"❌ ፋይሉ በትክክል አልተፃፈም (UTF-8 ይጠቀሙ)")
            return False
    
    def interactive_shell(self):
        """የቃለ መስተዋወህ ሻል"""
        print("""
🌟 አማርኛ ፕሮግራሚንግ ቋንቋ - የቃለ መስተዋወህ ሻል
የትእዛዝ:
  .ውጣ    - ሻሉን ይዝጉ
  .ረዳት   - እርዳታ አሳይ
  .ነባር   - ነባር ተለዋዋጮች አሳይ
  .ተግባር - ነባር ተግባራት አሳይ
  .ተንሸራታች - የተንሸራታች ሞድ ቀይር
  .ንጹህ    - ስክሪን አጽዳ
  .ታሪክ   - የትዕዛዝ ታሪክ አሳይ
        """)
        
        multiline = False
        buffer = []
        brace_count = 0
        
        while True:
            try:
                if not multiline:
                    prompt = ">>> "
                else:
                    prompt = "... "
                
                line = input(prompt)
                
                # የትእዛዝ ማስተናገድ
                if line.startswith('.') and not multiline:
                    cmd = line[1:].strip()
                    
                    if cmd in ['ውጣ', 'exit', 'quit']:
                        self._save_history()
                        print("👋 በሰላም!")
                        break
                    
                    elif cmd in ['ረዳት', 'help']:
                        self._show_help()
                    
                    elif cmd in ['ነባር', 'vars']:
                        self._show_variables()
                    
                    elif cmd in ['ተግባር', 'functions']:
                        self._show_functions()
                    
                    elif cmd in ['ተንሸራታች', 'debug']:
                        self.debug = not self.debug
                        status = "ተነሳ" if self.debug else "ጠፍቷል"
                        print(f"🔧 የተንሸራታች ሞድ: {status}")
                    
                    elif cmd in ['ንጹህ', 'clear']:
                        os.system('cls' if os.name == 'nt' else 'clear')
                    
                    elif cmd in ['ታሪክ', 'history']:
                        self._show_history()
                    
                    else:
                        print(f"❌ ያልታወቀ ትእዛዝ: {cmd}")
                    
                    continue
                
                # ባዶ መስመር
                if not line and not multiline:
                    continue
                
                # Count braces for multiline input
                brace_count += line.count('{') - line.count('}')
                
                if brace_count > 0 or (line.endswith(':') and not multiline):
                    multiline = True
                    buffer.append(line)
                    continue
                
                if multiline:
                    buffer.append(line)
                    
                    # የባለብዙ መስመር ኮድ መጨረሻ
                    if brace_count <= 0 and not line.endswith(':'):
                        code = '\n'.join(buffer)
                        self.run(code, "<interactive>")
                        multiline = False
                        buffer = []
                        brace_count = 0
                else:
                    # ነጠላ መስመር ኮድ
                    self.run(line, "<interactive>")
            
            except KeyboardInterrupt:
                print("\n🛑 በቁልፍ ተቋርጧል")
                multiline = False
                buffer = []
                brace_count = 0
            except EOFError:
                print("\n👋 በሰላም!")
                self._save_history()
                break
    
    def _show_help(self):
        """እርዳታ ማሳየት"""
        print("""
📚 የአማርኛ ፕሮግራሚንግ ቋንቋ እርዳታ

መሰረታዊ አጻጻፍ:
  ማተም "ሰላም ዓለም!"           # ውጤት ማተም
  ስም = "አበበ"                   # ተለዋዋጭ መፍጠር
  የቁጥር እድሜ = 25               # ከአይነት ጋር መፍጠር
  
ሁኔታዎች:
  ከ እድሜ >= 18 {
      ማተም "አዋቂ"
  } አለባችሁ {
      ማተም "ልጅ"
  }
  
ዑደቶች:
  ለ እኔ በ 1 እስከ 5 {
      ማተም እኔ
  }
  
  በሚታይ እድሜ < 18 {
      ማተም "ጠብቅ..."
      እድሜ = እድሜ + 1
  }
  
ተግባራት:
  ስራ ደምር (ሀ, ለ) {
      መመለስ ሀ + ለ
  }
  ማተም ደምር(5, 3)
  
ዝርዝሮች:
  ዝርዝር ቁጥሮች = [1, 2, 3, 4, 5]
  ማተም ቁጥሮች[0]
  ርዝመት(ቁጥሮች)  # 5 ያሳያል
  
መዝገቦች:
  መዝገብ ሰው = {
      "ስም": "አበበ",
      "እድሜ": 25
  }
  ማተም ሰው["ስም"]
  
ስህተት መያዝ:
  ሞክር {
      x = 10 / 0
  } ያዝ (ስህተት) {
      ማተም "ስህተት ተከስቷል: " + ስህተት
  }
  
ዝግጁ ተግባራት:
  ርዝመት(ነገር)    # የዝርዝር/ጽሁፍ ርዝመት
  አይነት(ነገር)       # የውሂብ አይነት መለየት
  ቁጥር("123")        # ወደ ቁጥር መቀየር
  ጽሁፍ(123)          # ወደ ጽሁፍ መቀየር
        """)
    
    def _show_variables(self):
        """ነባር ተለዋዋጮች ማሳየት"""
        if not self.interpreter.variables:
            print("📭 ምንም ተለዋዋጭ የለም")
            return
        
        print("📊 ነባር ተለዋዋጮች:")
        for name, value in sorted(self.interpreter.variables.items()):
            type_name = type(value).__name__
            if type_name == 'int':
                type_name = 'ቁጥር'
            elif type_name == 'str':
                type_name = 'ጽሁፍ'
            elif type_name == 'list':
                type_name = 'ዝርዝር'
            elif type_name == 'dict':
                type_name = 'መዝገብ'
            elif type_name == 'bool':
                type_name = 'እሴት'
            
            print(f"  {name} ({type_name}) = {repr(value)}")
    
    def _show_functions(self):
        """ነባር ተግባራት ማሳየት"""
        if not self.interpreter.functions:
            print("📭 ምንም ተግባር የለም")
            return
        
        print("🔧 ነባር ተግባራት:")
        for name, func in sorted(self.interpreter.functions.items()):
            params = [p[0] for p in func['parameters']]
            print(f"  {name}({', '.join(params)})")
    
    def _show_history(self):
        """የትዕዛዝ ታሪክ ማሳየት"""
        try:
            history = []
            for i in range(readline.get_current_history_length()):
                history.append(readline.get_history_item(i + 1))
            
            if not history:
                print("📭 ምንም ታሪክ የለም")
                return
            
            print("📜 የትዕዛዝ ታሪክ:")
            for i, cmd in enumerate(history[-20:], 1):  # Show last 20
                print(f"  {i}. {cmd}")
        except:
            print("❌ ታሪክ ማንበብ አልተቻለም")

def main():
    """ዋና የማስኬድ ተግባር"""
    apl = AmharicProgrammingLanguage()
    
    if len(sys.argv) == 1:
        # ያለ ነጋሪት - በቃለ መስተዋወህ ሞድ
        apl.interactive_shell()
    
    elif len(sys.argv) == 2:
        arg = sys.argv[1]
        
        if arg in ["--help", "-h"]:
            print("""
አጠቃቀም:
  aml                             - በቃለ መስተዋወህ ሞድ ማስኬድ
  aml <ፋይል.aml>                  - ፋይል ማስኬድ
  aml --test                       - ሙከራዎችን ማስኬድ
  aml --debug <ፋይል.aml>          - በተንሸራታች ሞድ ማስኬድ
  aml --version                    - ስሪት አሳይ
  aml --help                       - ይህን መልዕክት አሳይ
            
ምሳሌዎች:
  aml hello.aml
  aml --debug example.aml
            """)
        
        elif arg == "--test":
            run_tests()
        
        elif arg in ["--version", "-v"]:
            print("አማርኛ ፕሮግራሚንግ ቋንቋ v2.0.0")
        
        elif arg.endswith('.aml'):
            # ፋይል ማስኬድ
            apl.run_file(arg)
        
        else:
            print(f"❌ የተሳሳተ ፋይል: {arg}")
            print("aml --help ለእርዳታ")
    
    elif len(sys.argv) == 3 and sys.argv[1] == "--debug":
        apl.debug = True
        apl.run_file(sys.argv[2])
    
    else:
        print("❌ የተሳሳተ አጠቃቀም")
        print("aml --help ለእርዳታ")

def run_tests():
    """ሙከራዎችን ማስኬድ"""
    print("🧪 የአማርኛ ፕሮግራሚንግ ቋንቋ ሙከራዎች")
    print("=" * 60)
    
    apl = AmharicProgrammingLanguage()
    apl.debug = True
    
    tests = [
        ("ቀላል ማተም", 'ማተም "ሰላም ዓለም!"'),
        ("ተለዋዋጭ መመደቢያ", 'ስም = "አበበ"\nማተም ስም'),
        ("ሒሳብ", 'ሀ = 10\nለ = 5\nማተም ሀ + ለ'),
        ("የሁኔታ መግለጫ", '''
እድሜ = 20
ከ እድሜ >= 18 {
    ማተም "አዋቂ"
} አለባችሁ {
    ማተም "ልጅ"
}
        '''),
        ("የለ loop", '''
ለ እኔ በ 1 እስከ 3 {
    ማተም እኔ
}
        '''),
        ("ተግባር", '''
ስራ ደምር (ሀ, ለ) {
    መመለስ ሀ + ለ
}
ማተም ደምር(5, 3)
        '''),
        ("ዝርዝር", '''
ዝርዝር ቁጥሮች = [1, 2, 3, 4, 5]
ማተም ቁጥሮች[0]
ማተም ርዝመት(ቁጥሮች)
        '''),
        ("መዝገብ", '''
መዝገብ ሰው = {
    "ስም": "አበበ",
    "እድሜ": 25
}
ማተም ሰው["ስም"]
        '''),
        ("ስህተት መያዝ", '''
ሞክር {
    x = 10 / 0
} ያዝ (ስህተት) {
    ማተም "ስህተት: " + ስህተት
}
        '''),
        ("አመክንዮ ኦፔሬተሮች", '''
ሀ = እውነት
ለ = ሐሰት
ማተም ሀ && ለ
ማተም ሀ || ለ
ማተም !ሀ
        '''),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_code in tests:
        print(f"\n📋 ሙከራ: {test_name}")
        print("-" * 40)
        
        try:
            success = apl.run(test_code, "<test>")
            if success:
                passed += 1
                print(f"  ✅ ተሳክቷል")
            else:
                print(f"  ❌ አልተሳካም")
        except Exception as e:
            print(f"  ❌ ስህተት: {e}")
    
    print(f"\n📊 የሙከራ ውጤት: {passed}/{total} ተሳክተዋል")
    
    if passed == total:
        print("🎉 ሁሉም ሙከራዎች አልፈዋል!")
    else:
        print("⚠️  አንዳንድ ሙከራዎች አልተሳኩም")

if __name__ == "__main__":
    main()
