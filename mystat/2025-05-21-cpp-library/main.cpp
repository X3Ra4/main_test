#include <algorithm>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

class Item {
    std::string title_;
public:
    explicit Item(std::string title) : title_(std::move(title)) {}
    virtual ~Item() = default;
    const std::string& title() const { return title_; }
    virtual void print() const = 0;
};

class Book final : public Item {
    std::string author_;
    int year_;
    bool available_{true};
public:
    Book(std::string title, std::string author, int year)
        : Item(std::move(title)), author_(std::move(author)), year_(year) {}

    bool available() const { return available_; }
    void take() { available_ = false; }
    void give_back() { available_ = true; }

    void print() const override {
        std::cout << title() << " | " << author_ << " | " << year_
                  << " | " << (available_ ? "available" : "borrowed") << '\n';
    }
};

class User {
    std::string name_;
    std::vector<Book*> borrowed_;
public:
    explicit User(std::string name) : name_(std::move(name)) {}
    const std::string& name() const { return name_; }

    bool borrow(Book& book) {
        if (!book.available() || borrowed_.size() == 3) return false;
        borrowed_.push_back(&book);
        book.take();
        return true;
    }

    bool return_book(Book& book) {
        const auto found = std::find(borrowed_.begin(), borrowed_.end(), &book);
        if (found == borrowed_.end()) return false;
        borrowed_.erase(found);
        book.give_back();
        return true;
    }

    void print() const {
        std::cout << name_ << ": " << borrowed_.size() << " books\n";
        for (const auto* book : borrowed_) book->print();
    }
};

class Library {
    // Book addresses stay stable while the vector grows.
    std::vector<std::unique_ptr<Book>> books_;
    std::vector<User> users_;

public:
    Book* find(const std::string& title) const {
        for (const auto& book : books_) if (book->title() == title) return book.get();
        return nullptr;
    }

    void add(std::string title, std::string author, int year) {
        if (find(title)) throw std::invalid_argument("Duplicate title");
        books_.push_back(std::make_unique<Book>(std::move(title), std::move(author), year));
    }

    void register_user(std::string name) {
        if (find_user(name)) throw std::invalid_argument("Duplicate user");
        users_.emplace_back(std::move(name));
    }

    User* find_user(const std::string& name) {
        for (auto& user : users_) if (user.name() == name) return &user;
        return nullptr;
    }

    bool lend(const std::string& name, const std::string& title) {
        auto* user = find_user(name);
        auto* book = find(title);
        return user && book && user->borrow(*book);
    }

    bool accept(const std::string& name, const std::string& title) {
        auto* user = find_user(name);
        auto* book = find(title);
        return user && book && user->return_book(*book);
    }

    void print() const {
        for (const auto& book : books_) book->print();
    }
};

int main() {
    Library library;
    library.add("The Hobbit", "Tolkien", 1937);
    library.add("Dune", "Herbert", 1965);
    library.add("Foundation", "Asimov", 1951);
    library.add("Frankenstein", "Shelley", 1818);
    library.add("Solaris", "Lem", 1961);
    library.register_user("Olena");
    library.register_user("Ihor");
    if (!library.lend("Olena", "Dune") || !library.lend("Olena", "Solaris") ||
        library.lend("Ihor", "Dune")) return 1;
    library.find_user("Olena")->print();
    if (!library.accept("Olena", "Dune") || library.accept("Ihor", "Solaris")) return 1;
    library.print();
    for (std::string command; std::cout << "list | find | loan | return | user | quit: " && std::getline(std::cin, command);) {
        if (command == "quit") break;
        if (command == "list") { library.print(); continue; }
        std::string title, name;
        if (command == "user" || command == "loan" || command == "return") {
            std::cout << "User: "; if (!std::getline(std::cin, name)) break;
        }
        if (command == "find" || command == "loan" || command == "return") {
            std::cout << "Title: "; if (!std::getline(std::cin, title)) break;
        }
        if (command == "find") {
            if (auto* book = library.find(title)) book->print(); else std::cout << "Unknown book\n";
        } else if (command == "user") {
            if (auto* user = library.find_user(name)) user->print(); else std::cout << "Unknown user\n";
        } else if (command == "loan") {
            std::cout << (library.lend(name, title) ? "Borrowed\n" : "Unavailable or limit reached\n");
        } else if (command == "return") {
            std::cout << (library.accept(name, title) ? "Returned\n" : "No matching loan\n");
        }
    }
}
