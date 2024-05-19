def main(message):
    result = fr"""
        {message}
           \
            \
              ^__^
              (oo)\_______
              (__)\       )\/\
                  ||----w |
                  ||     ||
    """
    print(result)

if __name__ == "__main__":
    message = input()
    main(message)
