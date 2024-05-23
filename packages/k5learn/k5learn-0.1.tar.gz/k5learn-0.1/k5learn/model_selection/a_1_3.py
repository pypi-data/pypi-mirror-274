def a_1_3():

    print("""
    
    word_to_idx = {}
    word_to_idx['<pad>'] = 0
    for sentences in a:
        for word in sentences:
            if word not in word_to_idx:
                word_to_idx[word] = len(word_to_idx)
                
    
    """)