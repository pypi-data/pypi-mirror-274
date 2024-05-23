def a_1_2():

    print("""
    
    def load_file(filepath):
    
    train_sentences = []
    train_labels = []
    
    with open(filepath, 'r', encoding = 'utf-8') as file:
        sentences = []
        labels = []
        
        for line in file:
            line = line.strip()
            if not line:
                if sentences:
                    
                    train_sentences.append(sentences)
                    train_labels.append(labels)
                    sentences = []
                    labels = []
            else:
                parts = line.split()
                word = parts[0]
                label = parts[-1]
                
                sentences.append(word)
                labels.append(label)
                
    return train_sentences, train_labels
    
    """)