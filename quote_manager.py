class QuoteManager:
    def __init__(self, quotes_file, last_file):
        self.quotes_file = quotes_file
        self.last_file = last_file

    def get_next_quote(self):
        with open(self.last_file, "r", encoding="utf-8") as file:
            last_number = int(file.read().strip())

        with open(self.quotes_file, "r", encoding="utf-8") as file:
            quotes = file.readlines()

        if last_number < len(quotes):
            quote = quotes[last_number].strip()
            next_number = last_number + 1
        else:
            quote = None
            next_number = last_number

        with open(self.last_file, "w", encoding="utf-8") as file:
            file.write(str(next_number))

        return quote

    def remove_duplicate_quotes(self):
        with open(self.quotes_file, "r", encoding="utf-8") as file:
            unique_quotes = set(file.readlines())

        with open(self.quotes_file, "w", encoding="utf-8") as file:
            file.writelines(unique_quotes)
