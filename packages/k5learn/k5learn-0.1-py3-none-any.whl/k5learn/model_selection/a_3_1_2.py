def a_3_1_2():


    print("""
    
embedding_dim = 16
hidden_dim = 32

model = BiLSTM_CRF(len(word_to_idx), embedding_dim, hidden_dim, len(tag_to_idx))
optimizer = nn.SGD(model.trainable_params(), learning_rate=0.01, weight_decay=1e-4)
    
    """)