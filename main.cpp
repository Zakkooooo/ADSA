#include <iostream>
#include <array>
#include <string>

using std::array;
using std::string;
using std::cin;
using std::cout;

struct Slot {
    // 'N' = never used, 'O' = occupied, 'T' = tombstone
    char   st  = 'N';
    string key {};
};

static array<Slot, 26> tab;

// map last char to index 0..25
int hashIndex(const string& s) { 
    return s.back() - 'a'; 
}

// search returns index if found, otherwise -1.
int searchKey(const string& s) {
    int i = hashIndex(s), left = 26;
    while (left--){
        auto& t = tab[i];
        if (t.st == 'O' && t.key == s) 
            return i;
        if (t.st == 'N') 
            return -1;
        i = (i + 1 == 26) ? 0 : i + 1;
    }
    return -1;
}

// insert in the first slot ('N' or 'T') only if absent
void insertKey(const string& s) {
    if (searchKey(s) != -1) 
        return;
    int i = hashIndex(s), left = 26;
    while (left--) {
        auto& t = tab[i];
        if (t.st != 'O'){ t.st = 'O'; t.key = s; 
            return; }
        i = i + 1; if (i == 26) i = 0;
    }
}

// delete by marking tombstone if found
void deleteKey(const string& s) {
    int i = searchKey(s);
    if (i != -1) tab[i].st = 'T';
}

int main() {
    string token;
    while (cin >> token) {
        // skip invalid tokens
        if (token.size() < 2) continue;
        // parse operation and key
        char operation = token[0];   // 'A' or 'D'
        string word = token.substr(1);
        // apply operation
        if (operation == 'A') {
            insertKey(word);
        } else if (operation == 'D') {
            deleteKey(word);
        }
    }

    // print occupied keys in a..z order
    bool first = true;
    for (int index = 0; index < 26; ++index) {
        if (tab[index].st == 'O'){
            if (!first) cout << ' ';
            cout << tab[index].key;
            first = false;
        }
    }
    // newline and exit
    cout << '\n';
    return 0;
}
