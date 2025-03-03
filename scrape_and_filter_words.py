# scraping the words from the website:

# import requests

# url = 'https://www.mit.edu/~ecprice/wordlist.10000'
# response = requests.get(url)

# if response.status_code == 200:
#     words = response.text.splitlines()

#     with open('words.txt', 'w') as file:
#         for word in words:
#             file.write(word + '\n')
    
#     print("Words have been saved to words.txt")
# else:
#     print(f"Failed to retrieve the page. Status code: {response.status_code}")




# filtering for 5 letter words:

# five_letter_words = []

# with open('words.txt', 'r') as file:
#     for line in file.readlines():
#         word = line.strip()
#         if len(word) == 5:
#             five_letter_words.append(word)

# with open('words.txt', 'w') as file:
#     for word in five_letter_words:
#         file.write(word + '\n')

# print("Filtered 5-letter words have been saved back to words.txt")


