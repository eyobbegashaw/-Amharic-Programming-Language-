# አማርኛ ፕሮግራሚንግ ቋንቋ (Amharic Programming Language)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)]()

<p align="center">
  <img src="https://img.shields.io/badge/አማርኛ-Programming%20Language-red" alt="Amharic Programming Language">
</p>

<p align="center">
  <strong>የአማርኛ ቋንቋ ተናጋሪዎች በቀላሉ ፕሮግራም መጻፍ የሚችሉበት የፕሮግራሚንግ ቋንቋ</strong>
  <br>
  <em>A programming language designed for Amharic speakers to write code in their native language</em>
</p>

---

## 📌 የማከማቻ ስም (Repository Name)

**`amharic-programming-language`**

```bash
git clone https://github.com/yourusername/amharic-programming-language.git
cd amharic-programming-language
```

---

## 🌟 መግለጫ (Overview)

**አማርኛ ፕሮግራሚንግ ቋንቋ** በአማርኛ ቋንቋ ኮድ መጻፍ የሚያስችል የፕሮግራሚንግ ቋንቋ ነው። ይህ ቋንቋ በተለይ አማርኛ ተናጋሪዎች ፕሮግራሚንግ በቀላሉ እንዲማሩ እና እንዲጠቀሙ ለማስቻል ታስቦ የተዘጋጀ ነው።

The **Amharic Programming Language** allows developers to write code using Amharic keywords and syntax, making programming more accessible to Amharic speakers.

---

## ✨ ባህርያት (Features)

### 🔤 ሙሉ የአማርኛ ቁልፍ ቃላት
```javascript
ማተም "ሰላም ዓለም!"          // Print statement
ከ እድሜ >= 18 { ... }        // If condition
ለ እኔ በ 1 እስከ 5 { ... }      // For loop
ስራ ደምር (ሀ, ለ) { ... }      // Function definition
```

### 📊 የውሂብ አይነቶች (Data Types)
- **የቁጥር** (Integer)
- **የጽሁፍ** (String)
- **ዝርዝር** (List/Array)
- **መዝገብ** (Dictionary)
- **እውነት/ሐሰት** (Boolean)

### 🎯 የላቁ ባህርያት (Advanced Features)
- ✅ ተግባራዊ ፕሮግራሚንግ (Functional Programming)
- ✅ የስህተት አያያዝ (Try-Catch Error Handling)
- ✅ ባለብዙ ክልል ተለዋዋጮች (Scoped Variables)
- ✅ ዝግጁ ተግባራት (Built-in Functions)
- ✅ በቃለ መስተዋወህ ሻል (Interactive Shell)

---

## 🚀 መጫን (Installation)

### ቅድመ ሁኔታ (Prerequisites)
- Python 3.7 ወይም ከዚያ በላይ
- pip (Python package manager)

### መጫኛ ደረጃዎች (Installation Steps)

```bash
# 1. ማከማቻውን ያውርዱ (Clone the repository)
git clone https://github.com/yourusername/amharic-programming-language.git
cd amharic-programming-language

# 2. ፋይሎቹን ይመልከቱ (Make the main file executable)
chmod +x main.py

# 3. (አማራጭ) ሊንክ ይፍጠሩ (Optional: Create a symbolic link)
ln -s $(pwd)/main.py /usr/local/bin/aml
```

---

## 📝 አጠቃቀም (Usage)

### በቃለ መስተዋወህ ሻል (Interactive Shell)
```bash
python main.py
# ወይም (or)
./main.py
```

### ፋይል ማስኬድ (Run a File)
```bash
python main.py ፋይል.aml
python main.py examples/hello.aml
```

### በተንሸራታች ሞድ (Debug Mode)
```bash
python main.py --debug ፋይል.aml
```

### ሙከራዎችን ማስኬድ (Run Tests)
```bash
python main.py --test
```

### እርዳታ ማግኘት (Get Help)
```bash
python main.py --help
```

---

## 💡 ምሳሌዎች (Examples)

### 1. ቀላል ፕሮግራም (Hello World)
```javascript
ማተም "ሰላም ዓለም!"
```

### 2. ተለዋዋጮች እና ሒሳብ (Variables & Math)
```javascript
የቁጥር ሀ = 10
የቁጥር ለ = 5
ማተም "ድምር: " + (ሀ + ለ)
ማተም "ቅንስ: " + (ሀ - ለ)
ማተም "ውጤት: " + (ሀ * ለ)
```

### 3. የሁኔታ መግለጫ (If Statement)
```javascript
እድሜ = 18

ከ እድሜ >= 18 {
    ማተም "እንኳን ደህና መጣህ! አዋቂ ነህ"
} አለባችሁ {
    ማተም "ይቅርታ፣ ገና ልጅ ነህ"
}
```

### 4. የለ Loop (For Loop)
```javascript
ለ ቁጥር በ 1 እስከ 5 {
    ማተም "ቁጥር: " + ቁጥር
}

// በደረጃ (with step)
ለ እኔ በ 0 እስከ 10 ደረጃ 2 {
    ማተም "እኔ: " + እኔ
}
```

### 5. በሚታይ Loop (While Loop)
```javascript
ተቆጣጣሪ = 1
በሚታይ ተቆጣጣሪ <= 3 {
    ማተም "ዙር: " + ተቆጣጣሪ
    ተቆጣጣሪ = ተቆጣጣሪ + 1
}
```

### 6. ተግባራት (Functions)
```javascript
ስራ ደምር (ሀ, ለ) {
    መመለስ ሀ + ለ
}

ስራ አማካይ (ቁጥሮች) {
    ድምር = 0
    ለ እኔ በ 0 እስከ ርዝመት(ቁጥሮች) - 1 {
        ድምር = ድምር + ቁጥሮች[እኔ]
    }
    መመለስ ድምር / ርዝመት(ቁጥሮች)
}

ማተም ደምር(10, 5)        // 15
ማተም አማካይ([10, 20, 30])  // 20
```

### 7. ዝርዝሮች (Lists)
```javascript
ዝርዝር ፍራፍሬ = ["ሙዝ", "ብርቱካን", "ማንጎ"]
ማተም ፍራፍሬ[0]        // ሙዝ
ማተም ርዝመት(ፍራፍሬ)    // 3

// ዝርዝር መቀየር
ፍራፍሬ[1] = "ፖም"
ማተም ፍራፍሬ
```

### 8. መዝገቦች (Dictionaries)
```javascript
መዝገብ ተማሪ = {
    "ስም": "አበበ በላቸው",
    "እድሜ": 20,
    "ክፍል": "12ኛ"
}

ማተም ተማሪ["ስም"]      // አበበ በላቸው
ማተም ተማሪ["እድሜ"]     // 20
```

### 9. የስህተት አያያዝ (Error Handling)
```javascript
ሞክር {
    x = 10 / 0
} ያዝ (ስህተት) {
    ማተም "ስህተት ተከስቷል: " + ስህተት
}
```

### 10. ውስብስብ ምሳሌ (Complex Example)
```javascript
// የተማሪ ውጤት አስሊ
ስራ አስላውጤት (ውጤቶች) {
    ድምር = 0
    ብዛት = ርዝመት(ውጤቶች)
    
    ለ እኔ በ 0 እስከ ብዛት - 1 {
        ድምር = ድምር + ውጤቶች[እኔ]
    }
    
    አማካይ = ድምር / ብዛት
    
    ከ አማካይ >= 80 {
        መመለስ "እጅግ በጣም ጥሩ"
    } አለባችሁ ከ አማካይ >= 60 {
        መመለስ "ጥሩ"
    } አለባችሁ ከ አማካይ >= 50 {
        መመለስ "አጥጋቢ"
    } አለባችሁ {
        መመለስ "አልተሳካም"
    }
}

// ውጤቶች
የተማሪ_ውጤት = [85, 92, 78, 88, 70]
ውጤት = አስላውጤት(የተማሪ_ውጤት)
ማተም "የተማሪው ውጤት: " + ውጤት
```

---

## 🎮 በቃለ መስተዋወህ ሻል ትእዛዞች (Interactive Shell Commands)

| ትእዛዝ | ትርጉም | Description |
|--------|---------|-------------|
| `.ውጣ` | ሻሉን ይዝጉ | Exit the shell |
| `.ረዳት` | እርዳታ አሳይ | Show help |
| `.ነባር` | ነባር ተለዋዋጮች አሳይ | Show existing variables |
| `.ተግባር` | ነባር ተግባራት አሳይ | Show existing functions |
| `.ተንሸራታች` | የተንሸራታች ሞድ ቀይር | Toggle debug mode |
| `.ንጹህ` | ስክሪን አጽዳ | Clear screen |
| `.ታሪክ` | የትዕዛዝ ታሪክ አሳይ | Show command history |

---

## 🏗️ የፕሮጀክት መዋቅር (Project Structure)

```
amharic-programming-language/
│
├── main.py                 # ዋና ፕሮግራም (Main program)
├── lexer.py                # ሌክሳር - ቶከን መፍጠሪያ (Lexer - Tokenizer)
├── parser.py               # ፓርሰር - የኮድ ዛፍ ገንቢ (Parser - AST Builder)
├── interpreter.py          # ኢንተርፕሪተር - ኮድ አስፈጻሚ (Interpreter)
│
├── examples/               # ምሳሌዎች (Example programs)
│   ├── hello.aml
│   ├── math.aml
│   ├── functions.aml
│   └── ...
│
├── tests/                  # ሙከራዎች (Test files)
├── docs/                   # ሰነዶች (Documentation)
└── README.md               # ይህ ፋይል (This file)
```

---

## 🔧 የቴክኖሎጂ ቁልል (Technology Stack)

- **Python 3.7+** - ዋና ፕሮግራሚንግ ቋንቋ (Core programming language)
- **ከምንም ውጫዊ ቤተ-መጻሕፍት ነፃ** (No external dependencies)
- **የዩኒኮድ ድጋፍ** (Full Unicode support for Amharic characters)

---

## 📊 የአፈጻጸም (Performance)

ቋንቋው በሚከተሉት ላይ ተፈትኗል (The language has been tested on):
- ✅ ቀላል ስሌቶች (Simple calculations)
- ✅ የውሂብ መዋቅሮች (Data structures)
- ✅ ተደጋጋሚ ተግባራት (Recursive functions)
- ✅ ውስብስብ አልጎሪዝም (Complex algorithms)

---

## 🤝 አስተዋጽኦ ማድረጊያ (Contributing)

አስተዋጽኦ ማድረግ የሚፈልጉ ከሆነ፡-

1. ፎርክ ያድርጉት (Fork the repository)
2. አዲስ ቅርንጫፍ ይፍጠሩ (Create a new branch)
   ```bash
   git checkout -b feature/አዲስ-ባህርይ
   ```
3. ለውጦችዎን ይፈጽሙ (Commit your changes)
   ```bash
   git commit -m "አዲስ ባህርይ ጨመርኩ"
   ```
4. ይግፉ (Push)
   ```bash
   git push origin feature/አዲስ-ባህርይ
   ```
5. ፑል ሪኬስት ይክፈቱ (Open a Pull Request)

---

## 📜 ፈቃድ (License)

MIT License

Copyright (c) 2024 አማርኛ ፕሮግራሚንግ ቋንቋ

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...

---

## 📞 ድጋፍ (Support)

- 📧 ኢሜይል: [email@example.com](mailto:email@example.com)
- 🐦 ተሌግራም: [@amharic_programming](https://t.me/amharic_programming)
- 💬 ውይይት ቡድን: [Telegram Group](https://t.me/amharic_programming_group)

---

## 🙏 ምስጋና (Acknowledgments)

- ለአማርኛ ቋንቋ ተናጋሪዎች ሁሉ (To all Amharic speakers)
- ለፕሮግራሚንግ ቋንቋ አፍቃሪዎች (To programming language enthusiasts)
- ለኦፕን ሶርስ ማህበረሰብ (To the open source community)

---

## 📈 የወደፊት እቅዶች (Future Plans)

- [ ] ፋይል ሲስተም ኦፕሬሽኖች (File system operations)
- [ ] ኔትወርክ ፕሮግራሚንግ (Network programming)
- [ ] GUI ፕሮግራሚንግ (GUI programming)
- [ ] ኦጄክት ኦረንትድ ፕሮግራሚንግ (Object-oriented programming)
- [ ] ማጠናቀሪያ (Compiler/JIT compilation)

---

<p align="center">
  <strong>አማርኛን በኮድ እንጻፍ! አማርኛን በቴክኖሎጂ እናሳድግ!</strong>
  <br>
  <em>Write code in Amharic! Advance Amharic in technology!</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/አማርኛ-ሶፍትዌር-blue" alt="Amharic Software">
  <img src="https://img.shields.io/badge/Ethiopia-Programming-green" alt="Ethiopia Programming">
  <img src="https://img.shields.io/badge/Language-Amharic-orange" alt="Amharic Language">
</p>

---
