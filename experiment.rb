23.times { |i| puts "cnvrg_linechart_LossLog value: '#{"%f" % (1/((i+1)**2).to_f).to_s}'" }
puts "==="
puts "==="
puts "==="
sleep 1
50.times { |i| puts "cnvrg_linechart_AccuracyLog value: '#{"%f" % (i**2 * 0.000001).to_s}'"}
100.times { |i| puts "cnvrg_linechart_Event group: 'ts' value: '#{"%f" % (i**2 * 0.000004).to_s}'"}
120.times { |i| puts "cnvrg_linechart_Event group: 'epochs' value: '#{"%f" % (i**2 * 0.000005).to_s}'"}

puts "cnvrg_tag_Accuracy: 0.9766"
puts "cnvrg_tag_Algorithm: NeuralNetworks"
puts "cnvrg_tag_Architecture: RNN (LSTM)"
puts "cnvrg_tag_FeaturesDim:200"                                                
puts "cnvrg_tag_BatchSize:32"
puts "cnvrg_tag_epochs:10" 
puts "cnvrg_tag_WordEmbedding:FastText" 

puts "============================"                                             
puts "Loading model"                                                            
                                                                                
keras_lines = ["Train on 2394 samples, validate on 1027 samples", "Epoch 1/10", 
                              "2394/2394 [==============================] - 0s - loss: 0.6898 - acc: 0.5455 - val_loss: 0.6835 - val_acc: 0.5716",
                                             "Epoch 2/10", "2394/2394 [==============================] - 0s - loss: 0.6879 - acc: 0.5522 - val_loss: 0.6901 - val_acc: 0.5522",
                                                            "Epoch 3/10", "2394/2394 [==============================] - 0s - loss: 0.5555 - acc: 0.6000 - val_loss: 0.6000 - val_acc: 0.6000",
                                                                           "Epoch 4/10", "2394/2394 [==============================] - 0s - loss: 0.5444 - acc: 0.6777 - val_loss: 0.5800 - val_acc: 0.6777",
                                                                                          "Epoch 5/10", "2394/2394 [==============================] - 0s - loss: 0.4555 - acc: 0.7777 - val_loss: 0.5444 - val_acc: 0.7777",
                                                                                                         "Epoch 6/10", "2394/2394 [==============================] - 0s - loss: 0.4220 - acc: 0.8000 - val_loss: 0.5222 - val_acc: 0.8000",
                                                                                                                        "Epoch 7/10", "2394/2394 [==============================] - 0s - loss: 0.4000 - acc: 0.8200 - val_loss: 0.4344 - val_acc: 0.8200",
                                                                                                                                       "Epoch 8/10", "2394/2394 [==============================] - 0s - loss: 0.3600 - acc: 0.8100 - val_loss: 0.3333 - val_acc: 0.8100",
                                                                                                                                                      "Epoch 9/10", "2394/2394 [==============================] - 0s - loss: 0.3685 - acc: 0.9000 - val_loss: 0.2323 - val_acc: 0.9000",
                                                                                                                                                                     "Epoch 10/10", "2394/2394 [==============================] - 0s - loss: 0.357 - acc: 0.9700 - val_loss: 0.1414 - val_acc: 0.9700",
                                                                                                                                                                                    "1027/1027 [==============================] - 0s"]               
                                                                                
                                                                                
keras_lines.each do |l|                                                         
      puts l                                                                      
end   
`cp ../image1.png .`                                                           
#
