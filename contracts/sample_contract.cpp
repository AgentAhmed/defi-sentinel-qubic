#include <iostream>
#include <string>

int balance = 1000;

void deposit(int amount) {
    if (amount > 0) {
        balance += amount;
        std::cout << "Deposited: " << amount << std::endl;
    }
}

void withdraw(int amount) {
    if (amount <= balance) {
        balance -= amount;
        std::cout << "Withdrawn: " << amount << std::endl;
    } else {
        std::cout << "Insufficient balance!" << std::endl;
    }
}

void transfer(std::string to, int amount) {
    if (amount <= balance && !to.empty()) {
        balance -= amount;
        std::cout << "Transferred " << amount << " to " << to << std::endl;
    } else {
        std::cout << "Transfer failed!" << std::endl;
    }
}

void showBalance() {
    std::cout << "Balance: " << balance << std::endl;
}
