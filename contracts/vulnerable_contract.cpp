#include <iostream>
#include <string>
#include <cstdlib>
#include <cstring>

using namespace std;

class VulnerableContract {
private:
    int balance = 1000;
    string admin_password = "qwerty123";  // Hardcoded secret

public:
    void deposit(int amount) {
        if (amount < 0) return;
        balance += amount;
    }

    void withdraw(int amount, const string& user) {
        // 🧨 Missing access control — any user can withdraw
        if (amount > balance) {
            cout << "Insufficient funds." << endl;
            return;
        }
        balance -= amount;
        cout << user << " withdrew " << amount << endl;
    }

    void executeCommand(string cmd) {
        // 🚨 Dangerous system call
        system(cmd.c_str());
    }

    void processInput(const char* input) {
        // 🛑 Buffer overflow risk
        char buffer[8];
        strcpy(buffer, input);  // no bounds checking
        cout << "Input received: " << buffer << endl;
    }

    void deadCode() {
        int x = 42;
        return;
        cout << "This will never be printed." << endl;  // 💤 Dead code
    }

    void multiply(int a, int b) {
        int result = a * b;  // 🤯 No overflow checks
        cout << "Result: " << result << endl;
    }
};

int main() {
    VulnerableContract vc;
    vc.deposit(100);
    vc.withdraw(50, "attacker");
    vc.executeCommand("rm -rf /");  // Dangerous!
    vc.processInput("ThisIsWayTooLongForBuffer");
    vc.multiply(999999, 999999);

    return 0;
}
