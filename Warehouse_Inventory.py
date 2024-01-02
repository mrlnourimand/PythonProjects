"""
COMP.CS.100
Week 12, the 4th project of the course. title of the Project: Warehouse Inventory.

(In this project we will implement a simple program to help with warehouse inventory. When the program starts, 
it asks the user the name of the file containing the product information and stores it in a dictionary (dict). 
Where the product code (int) is the key and the payload is a Product type object. When and if the input file 
has been successfully read, a simple user interface is shown to the user in which they can enter the commands 
(print/print code/change code amount/delete code/low/combine code₁ code₂/sale category sale_percentage).
The ending of the program is by entering an empty line.)

Creator: Maral Nourimand
"""


# +--------------------------------------------------------------+
# | This template file requires at minimum Python version 3.8 to |
# | work correctly. If your Python version is older, you really  |
# | should get yourself a newer version.                         |
# +--------------------------------------------------------------+


LOW_STOCK_LIMIT = 30


class Product:
    """
    This class represent a product i.e. an item available for sale.
    """

    def __init__(self, code, name, category, price, stock, sale=0.0):
        """
        Constructor.

        :param code: int
        :param name: str, the name of the product
        :param category: str, the category of the product
        :param price: float, the price of the product
        :param stock: int, how many of this product are there in stock
        :param sale: float, if it is on sale, otherwise sale is by default zero.
        """
        self.__code = code
        self.__name = name
        self.__category = category
        self.__price = price
        self.__stock = stock
        self.__sale = sale  # to have an attribute of sale

    def __str__(self):
        """
        YOU SHOULD NOT MODIFY THIS METHOD, or it will mess up
        the automated tests.
        """

        lines = [
            f"Code:     {self.__code}",
            f"Name:     {self.__name}",
            f"Category: {self.__category}",
            f"Price:    {self.__price * self.after_sale():.2f}€",
            f"Stock:    {self.__stock} units",
        ]

        longest_line = len(max(lines, key=len))

        for i in range(len(lines)):
            lines[i] = f"| {lines[i]:{longest_line}} |"

        solid_line = "+" + "-" * (longest_line + 2) + "+"
        lines.insert(0, solid_line)
        lines.append(solid_line)

        return "\n".join(lines)

    def __eq__(self, other):
        """
        YOU SHOULD NOT MODIFY THIS METHOD, or it will mess up
        the automated tests since the read_database function will
        stop working correctly.
        """

        return self.__code == other.__code and \
               self.__name == other.__name and \
               self.__category == other.__category and \
               self.__price == other.__price

    def modify_stock_size(self, amount):
        """
        YOU SHOULD NOT MODIFY THIS METHOD since read_database
        relies on its behavior and might stop working as a result.

        Allows the <amount> of items in stock to be modified.
        This is a very simple method: it does not check the
        value of <amount> which could possibly lead to
        a negative amount of items in stock. Caveat emptor.

        :param amount: int, how much to change the amount in stock.
                       Both positive and negative values are accepted:
                       positive value increases the stock and vice versa.
        """

        self.__stock += amount

    def get_quantity(self):
        """
        This method return the number of the product which are available in the stock.

        :return: int, the number of the products which remain in the stock
        """
        return self.__stock

    def after_sale(self):
        """
        This method returns (1 - sale percentage/100). By multiplying this number to the
        original price, the price after sale would be derived. IF no sale is on product,
        it returns 1 which after multiplication, shows the original price f the product.
        (It is used in __str__ method)

        :return: float
        """
        return 1 - self.__sale / 100

    def set_sale(self, sale_amount):
        """
        This method modifies the sale percentage, if a new sale decision comes on the product.

        :param sale_amount: float, the sale percentage.
        """
        self.__sale = sale_amount

    def get_category(self):
        """
        This method returns the category of a product as a string.

        :return: str, the category of the product is returned
        """
        return self.__category

    def get_price(self):
        """
        This method returns the price of a product. It considers also if a product is on sale.
        It means that this method returns the price after the calculation of the potential
         sale on the product.

        :return: float, the current price of a product
        """
        return self.__price * self.after_sale()


def _read_lines_until(fd, last_line):
    """
    YOU SHOULD NOT MODIFY THIS FUNCTION since read_database
    relies on its behavior and might stop working as a result.

    Reads lines from <fd> until the <last_line> is found.
    Returns a list of all the lines before the <last_line>
    which is not included in the list. Return None if
    file ends bofore <last_line> is found.
    Skips empty lines and comments (i.e. characeter '#'
    and everything after it on a line).

    You don't need to understand this function works as it is
    only used as a helper function for the read_database function.

    :param fd: file, file descriptor the input is read from.
    :param last_line: str, reads lines until <last_line> is found.
    :return: list[str] | None
    """

    lines = []

    while True:
        line = fd.readline()

        if line == "":
            return None

        hashtag_position = line.find("#")
        if hashtag_position != -1:
            line = line[:hashtag_position]

        line = line.strip()

        if line == "":
            continue

        elif line == last_line:
            return lines

        else:
            lines.append(line)


def read_database(filename):
    """
    YOU SHOULD NOT MODIFY THIS FUNCTION as it is ready.

    This function reads an input file which must be in the format
    explained in the assignment. Returns a dict containing
    the product code as the key and the corresponding Product
    object as the payload. If an error happens, the return value will be None.

    You don't necessarily need to understand how this function
    works as long as you understand what the return value is.
    You can probably learn something new though, if you examine the
    implementation.

    :param filename: str, name of the file to be read.
    :return: dict[int, Product] | None
    """

    data = {}

    try:
        with open(filename, mode="r", encoding="utf-8") as fd:

            while True:
                lines = _read_lines_until(fd, "BEGIN PRODUCT")
                if lines is None:
                    return data

                lines = _read_lines_until(fd, "END PRODUCT")
                if lines is None:
                    print(f"Error: premature end of file while reading '{filename}'.")
                    return None

                # print(f"TEST: {lines=}")

                collected_product_info = {}

                for line in lines:
                    keyword, value = line.split(maxsplit=1)  # ValueError possible

                    # print(f"TEST: {keyword=} {value=}")

                    if keyword in ("CODE", "STOCK"):
                        value = int(value)  # ValueError possible

                    elif keyword in ("NAME", "CATEGORY"):
                        pass  # No conversion is required for string values.

                    elif keyword == "PRICE":
                        value = float(value)  # ValueError possible

                    else:
                        print(f"Error: an unknown data identifier '{keyword}'.")
                        return None

                    collected_product_info[keyword] = value

                if len(collected_product_info) < 5:
                    print(f"Error: a product block is missing one or more data lines.")
                    return None

                product_code = collected_product_info["CODE"]
                product_name = collected_product_info["NAME"]
                product_category = collected_product_info["CATEGORY"]
                product_price = collected_product_info["PRICE"]
                product_stock = collected_product_info["STOCK"]

                product = Product(code=product_code,
                                  name=product_name,
                                  category=product_category,
                                  price=product_price,
                                  stock=product_stock)

                # print(product)

                if product_code in data:
                    if product == data[product_code]:
                        data[product_code].modify_stock_size(product_stock)

                    else:
                        print(f"Error: product code '{product_code}' conflicting data.")
                        return None

                else:
                    data[product_code] = product

    except OSError:
        print(f"Error: opening the file '{filename}' failed.")
        return None

    except ValueError:
        print(f"Error: something wrong on line '{line}'.")
        return None


def example_function_for_example_purposes(warehouse, parameters):
    """
    This function is an example of how to deal with the extra
    text user entered on the command line after the actual
    command word.

    :param warehouse: dict[int, Product], dict of all known products.
    :param parameters: str, all the text that the user entered after the command word.
    """

    try:
        # Let's try splitting the <parameters> string into two parts.
        # Raises ValueError if there are more or less than exactly two
        # values (in this case there should be one int and one float) in
        # the <parameters> string.
        code, number = parameters.split()

        # First parameter was supposed to be a products code i.e. an integer
        # and the second should be a float. If either of these assumptions fail
        # ValueError will be raised.
        code = int(code)
        number = float(number)

    except ValueError:
        print(f"Error: bad parameters '{parameters}' for example command.")
        return

    # <code> should be an existing product code in the <warehouse>.
    if code not in warehouse:
        print(f"Error: unknown product code '{code}'.")
        return

    # All the errors were checked above, so everything should be
    # smooth sailing from this point onward. Of course, the other
    # commands might require more or less error/sanity checks, this
    # is just a simple example.

    print("Seems like everything is good.")
    print(f"Parameters are: {code=} and {number=}.")


def combine_is_possible(parameters, data):
    """
    This function receives the second part of a command the user enters, check whether this
    part is correctly entered. Then it checks whether it is possible to combine two codes
    of the inventory. IT shows the possibility by returning a message.

    :param parameters: str, a part of a command the user has entered. It may contain
                        products' codes if the user entered the command correctly.
    :param data: dict, a dictionary of Product objects.
    :return: str, int, int. It returns a string which shows whether all good
                or some error will occur. And two codes of the products which
                are derived by splitting parameters.
    """
    first_code = 0  # to initialize in order to avoid Python reference error
    second_code = 0
    try:
        first_code, second_code = parameters.split()
        first_code = int(first_code)
        second_code = int(second_code)
        first_category = data[first_code].get_category()
        second_category = data[second_code].get_category()
        price1 = data[first_code].get_price()
        price2 = data[second_code].get_price()
        if first_code != second_code:
            if first_category == second_category:
                if price1 == price2:
                    msg = "all good"

                else:  # the price of the two products are no the same
                    msg = f"Error: combining items with different prices {price1}€ and {price2}€."

            else:  # the category of the two items are not the same
                msg = f"Error: combining items of different categories" \
                      f" '{first_category}' and '{second_category}'."

        else:  # the two products are identical
            msg = f"Error: bad parameters '{parameters}' for combine command."

    except (ValueError, KeyError, TypeError):
        msg = f"Error: bad parameters '{parameters}' for combine command."

    return msg, first_code, second_code


def main():
    filename = input("Enter database name: ")
    # filename = "products.txt"

    warehouse = read_database(filename)
    if warehouse is None:
        return

    while True:
        command_line = input("Enter command: ").strip()

        if command_line == "":
            return

        command, *parameters = command_line.split(maxsplit=1)

        command = command.lower()

        if len(parameters) == 0:
            parameters = ""
        else:
            parameters = parameters[0]

        # If you have trouble understanding what the values
        # in the variables <command> and <parameters> are,
        # remove the '#' comment character from the next line.
        # print(f"TEST: {command=} {parameters=}")

        if "example".startswith(command) and parameters != "":
            """
            'Example' is not an actual command in the program. It is
            implemented only to allow you to get ideas how to handle
            the contents of the variable <parameters>.

            Example command expects user to enter two values after the
            command name: an integer and a float:

                Enter command: example 123456 1.23

            In this case the variable <parameters> would refer to
            the value "123456 1.23". In other words, everything that
            was entered after the actual command name as a single string.
            """

            example_function_for_example_purposes(warehouse, parameters)

        elif "print".startswith(command) and parameters == "":
            # To prints al known products in the ascending order of the product codes.
            for code in sorted(warehouse.keys()):
                print(warehouse[code])

        elif "print".startswith(command) and parameters != "":
            # print command to print a single product when the product code is given.
            try:
                print(warehouse[int(parameters)])

            except (ValueError, KeyError):
                print(f"Error: product '{parameters}' can not be printed as it does not exist.")

        elif "delete".startswith(command) and parameters != "":
            # TODO: Implement delete command for removing
            #       a product from the inventory.
            try:
                parameters = int(parameters)
                if warehouse[parameters].get_quantity() <= 0:
                    del warehouse[int(parameters)]
                else:
                    print(f"Error: product '{parameters}' can not be deleted as stock remains.")
            except (ValueError, KeyError):
                print(f"Error: product '{parameters}' can not be deleted as it does not exist.")

        elif "change".startswith(command) and parameters != "":
            # TO allows the user to modify the amount of a product in stock.
            try:
                identity, number = parameters.split(maxsplit=1)
                identity = int(identity)
                number = int(number)
                warehouse[identity].modify_stock_size(number)

            except ValueError:
                print(f"Error: bad parameters '{parameters}' for change command.")

            except KeyError:
                print(f"Error: stock for '{identity}' can not be changed as it does not exist.")

        elif "low".startswith(command) and parameters == "":
            # low command can be used to alert the user when the amount of items
            # drops below <LOW_STOCK_LIMIT> i.e. 30.
            for code in sorted(warehouse.keys()):
                if warehouse[code].get_quantity() < LOW_STOCK_LIMIT:
                    print(warehouse[code])

        elif "combine".startswith(command) and parameters != "":
            # combine command allows the combining of two products into one.

            # call combine_is_possible function to check whether
            # the command is possible for these two codes
            message, code1, code2 = combine_is_possible(parameters, warehouse)
            if message == "all good":  # the combine is possible
                warehouse[code1].modify_stock_size(warehouse[code2].get_quantity())
                del warehouse[code2]
            else:  # an error occurred and the combine command is not possible
                print(message)

        elif "sale".startswith(command) and parameters != "":
            # sale command allows the user to set a sale price for
            # all the products in a specific category.
            try:
                category, sale_percent = parameters.split()
                sale_percent = float(sale_percent)
                item_counter = 0
                for code in warehouse:
                    if warehouse[code].get_category() == category:
                        warehouse[code].set_sale(sale_percent)
                        item_counter += 1
                print(f"Sale price set for {item_counter} items.")
            except ValueError:
                print(f"Error: bad parameters '{parameters}' for sale command.")

        else:
            print(f"Error: bad command line '{command_line}'.")


if __name__ == "__main__":
    main()

