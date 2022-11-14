def main():
    # Bring paa
    number_of_questions = 20
    # category = input("Enter category: ")
    number_of_heads = int(input("Enter number of headings: "))
    while number_of_heads <= 8:
        number_of_heads = int(input("Must be larger than 8. \nEnter number of headings: "))
    number_of_questions = number_of_heads * 2
    print('\tIntroduction')
    for index_1, i in enumerate(range(0, 6, 2)):
        print(f'1, index={index_1}, i={i}, {i+1}')

    print('\tVideo')

    for index_1, i in enumerate(range(6, 10, 2)):
        print(f'2, index={index_1}, i={i}, {i+1}')

    print('\tImage 1')

    for index_1, i in enumerate(range(10, 16, 2)):
        print(f'3, index={index_1}, i={i}, {i+1}')

    print('\tImage 2')

    for index_1, i in enumerate(range(16, number_of_questions, 2)):

        if i == number_of_questions-2:
            print(f'4, index={index_1}, i={i}, {i+1}, conclusion')
        else:
            print(f'4, index={index_1}, i={i}, {i+1}, before conclusion')


if __name__ == '__main__':
    main()