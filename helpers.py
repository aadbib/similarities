'''    Naam: Achraf Adbib
   Opdracht: Similarities(Hacker)  '''


# Import de Enum-class from de enum library
from enum import Enum


class Operation(Enum):
    """Operations"""

    DELETED = 1
    INSERTED = 2
    SUBSTITUTED = 3

    def __str__(self):
        return str(self.name.lower())


def base_matrix(a, b):
    """Calculate and initiliazing a matrix for the base-condition of two given strings"""

    # Empty matrix
    matrix = [[]]

    # First, we need to define the base of the matrix. To do that, we need to
    # make sure that we store the operations from going from string-a to an empty-string,
    # and from an empty-string to string-b
    matrix[0].append((0, None))

    for index, char in enumerate(a):
        cost = index + 1
        matrix.append([(cost, Operation.DELETED)])

    for index, char in enumerate(b):
        cost = index + 1
        matrix[0].append((cost, Operation.INSERTED))

    # Return the base-condition matrix
    return matrix


def deletion(a, matrix_index_a, b, matrix_index_b, matrix):
    """Returns the cost in a tuple for implementing deletion as the last operation"""

    # The cost of deletion is the sum of operations defined by executing the [row - 1][col] operation + the deletion operation itself :)
    # Take the first index, because it's stored as a tuple where the first index is cost and the second the operation
    # And add 1 to the cost to account for the last-operation (deletion)
    cost = matrix[matrix_index_a - 1][matrix_index_b][0] + 1

    # Return the calculated cost and the last operation needed for this algorithm
    return (cost, Operation.DELETED)


def insertion(a, matrix_index_a, b, matrix_index_b, matrix):
    """Returns the cost in a tuple for implementing insertion as the last operation"""

    # The cost of insertion is the sum of operations defined by executing the [row][col - 1] operation + the insertion operation itself
    # Take the first index, because it's stored as a tuple where the first index is cost and the second the operation
    # Finally, add 1 to the cost to account for the last-operation (insertion)
    cost = matrix[matrix_index_a][matrix_index_b - 1][0] + 1

    # Return the calculated cost and the last operation needed for this algorithm
    return (cost, Operation.INSERTED)


def substitution(a, matrix_index_a, b, matrix_index_b, matrix):
    """Returns the cost in a tuple for implementing substituion as the last operation"""

    # The cost of substitution is the (sum of) operations defined by executing the [row - 1][col - 1] operation
    # After that, if the last character of string_a is equal to the last character of string_b, then there is no addtional operation
    # If it's not the same character, then add 1 operation, which is the subtitution operation itself.
    cost = matrix[matrix_index_a - 1][matrix_index_b - 1][0]

    if a[-1] != b[-1]:
        cost += 1

    # Return the calculated cost and the last operation needed for this algorithm
    return (cost, Operation.SUBSTITUTED)


def distances(a, b):
    """Calculate edit distance from a to b"""

    # Initiliaze base-matrix using the function 'base_matrix'
    matrix = base_matrix(a, b)

    # For the index and characters in string_a
    for index_a, char in enumerate(a):

        matrix_index_a = index_a + 1

        # Stores the sub-string of string_a that increments by 1 for each loop
        sub_string_a = a[0:matrix_index_a]

        # For the index and characters in string_b
        for index_b, char in enumerate(b):

            # Variables defining the matrix-index that the string_index of a and b represent in the matrix
            # + 1 Because [0][0] is None/0 in the matrix
            matrix_index_b = index_b + 1

            # Dictionary to store the cost and operations
            cost_collector = {}

            # Stores the sub-string of string_b that increments by 1 for each loop
            sub_string_b = b[0:matrix_index_b]

            # Stores the costs for each operation in a variable and appends them to a dictionary,
            # so that we can extract the lowest cost along with the used operation

            """
            NOTICE: By switching the order of the "appending to the dictionary" code
            you will alter the operation-order displayed on the website-route /score if two operations cost the same
            This is because the min() function takes the latest minimum-value in the dictionary!
            But no worries, the operation-cost will stay the same, and thus they are both correct :)
            """

            # En zo zie je maar weer, er zijn meerdere wegen naar Rome :D
            cost_deletion = deletion(sub_string_a, matrix_index_a, sub_string_b, matrix_index_b, matrix)
            cost_collector[cost_deletion[1]] = cost_deletion[0]

            cost_substitution = substitution(sub_string_a, matrix_index_a, sub_string_b, matrix_index_b, matrix)
            cost_collector[cost_substitution[1]] = cost_substitution[0]

            cost_insertion = insertion(sub_string_a, matrix_index_a, sub_string_b, matrix_index_b, matrix)
            cost_collector[cost_insertion[1]] = cost_insertion[0]

            # Extract the key with the lowest value in the dictionary
            minimum_operator = min(cost_collector, key=cost_collector.get)

            # Extract the lowest value from the dictionary using the key above
            minimum_cost = cost_collector[minimum_operator]

            # Store the lowest cost along with its final operator in a tuple
            min_tuple = (minimum_cost, minimum_operator)

            # Add the tuple to the matrix using the matrix_index_a as the index of the matrix
            # because the j-th characters of b are compared to the i-th characters of a
            matrix[matrix_index_a].append(min_tuple)

    # Return the matrix
    return matrix